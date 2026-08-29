"""REQ-41 GAP-41-03: concurrent intake contract (CC-01..02)."""

from __future__ import annotations

from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from tests.intake_v2_fixtures import intake_payload_simple
from tests.story_draft_intake_helpers import (
    patch_identity_me_verified,
    post_intake_via_story_drafts,
    stash_story_draft,
    submit_story_draft,
    submitter_external_id,
)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_CRON_ENABLED", "false")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _post_intake(
    client: TestClient,
    *,
    worker_id: int,
    idempotency_key: str | None = None,
) -> tuple[int, str | None]:
    key = idempotency_key or f"cc-worker-{worker_id}"
    payload = intake_payload_simple(
        external_user_id=f"cc-user-{worker_id}",
        original_text=f"Concurrent intake worker {worker_id} Kalamaja district",
        title_en=f"CC {worker_id}",
    )
    payload["narrative"]["location_query"] = "Kalamaja, Tallinn"
    response = post_intake_via_story_drafts(
        client,
        json=payload,
        headers={"idempotency-key": key},
    )
    story_id = None
    if response.status_code == 202:
        story_id = response.json()["data"]["story_id"]
    return response.status_code, story_id


def test_cc01_parallel_intake_returns_five_unique_story_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CC-01: five parallel intakes → five unique story_ids."""
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_CRON_ENABLED", "false")
    last_error: AssertionError | None = None
    for _ in range(3):
        _clear_api_dependencies_cache()
        suffix = uuid4().hex
        try:
            with TestClient(app) as fresh_client:
                with ThreadPoolExecutor(max_workers=5) as pool:
                    futures = [
                        pool.submit(
                            _post_intake,
                            fresh_client,
                            worker_id=i,
                            idempotency_key=f"cc-worker-{suffix}-{i}",
                        )
                        for i in range(5)
                    ]
                    results = [future.result() for future in as_completed(futures)]
            statuses, story_ids = zip(*results, strict=True)
            assert all(status == 202 for status in statuses)
            assert len(story_ids) == 5
            assert len(set(story_ids)) == 5
            return
        except AssertionError as exc:
            last_error = exc
        finally:
            _clear_api_dependencies_cache()
    assert last_error is not None
    raise last_error


def test_cc02_parallel_same_idempotency_key_creates_one_story(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CC-02: parallel submit replay on one draft → one story."""
    payload = intake_payload_simple(
        external_user_id="cc-shared-user",
        original_text="Concurrent shared draft Kalamaja district",
        title_en="CC shared",
    )
    payload["narrative"]["location_query"] = "Kalamaja, Tallinn"

    for _ in range(3):
        _clear_api_dependencies_cache()
        with TestClient(app) as fresh_client:
            shared_draft_id = stash_story_draft(
                fresh_client,
                payload,
                headers={"idempotency-key": "cc-shared-idempotency"},
            )
            patch_identity_me_verified(monkeypatch, sub=submitter_external_id(payload))

            def _submit() -> tuple[int, str | None]:
                response = submit_story_draft(fresh_client, shared_draft_id)
                story_id = None
                if response.status_code == 202:
                    story_id = response.json()["data"]["story_id"]
                return response.status_code, story_id

            with ThreadPoolExecutor(max_workers=5) as pool:
                futures = [pool.submit(_submit) for _ in range(5)]
                results = [future.result() for future in as_completed(futures)]
        statuses, story_ids = zip(*results, strict=True)
        assert all(status == 202 for status in statuses)
        assert len(set(story_ids)) == 1
