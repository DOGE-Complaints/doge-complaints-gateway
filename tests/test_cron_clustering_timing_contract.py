"""REQ-41 GAP-41-02: full-stack cron timing via ASGI lifespan (CT-01..03)."""

from __future__ import annotations

import time
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.intake_v2_fixtures import intake_payload_simple
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


def _projection_count() -> int:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    return len(store.list_projections())


def _cron_client(monkeypatch: pytest.MonkeyPatch, *, cron_enabled: bool) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch.setenv("CLUSTER_CRON_INTERVAL_S", "1")
    monkeypatch.setenv("CLUSTER_CRON_ENABLED", "true" if cron_enabled else "false")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _intake_pair(client: TestClient, *, prefix: str) -> None:
    for suffix in ("a", "b"):
        payload = intake_payload_simple(
            external_user_id=f"cron-timing-{prefix}-{suffix}",
            original_text=f"Pavement damage cron timing {prefix} {suffix} Kalamaja",
            title_en=f"Cron {prefix} {suffix}",
        )
        payload["narrative"]["location_query"] = "Kalamaja, Tallinn"
        response = post_intake_via_story_drafts(
        client,
            json=payload,
            headers={"idempotency-key": f"cron-{prefix}-{suffix}"},
        )
        assert response.status_code == 202, response.text


@pytest.fixture()
def cron_enabled_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    yield from _cron_client(monkeypatch, cron_enabled=True)


@pytest.fixture()
def cron_disabled_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    yield from _cron_client(monkeypatch, cron_enabled=False)


def test_ct01_cron_creates_issue_after_interval(cron_enabled_client: TestClient) -> None:
    """CT-01: after interval with 2 stories, projections contain at least one issue."""
    assert _projection_count() == 0
    started = time.monotonic()
    _intake_pair(cron_enabled_client, prefix="ct01")
    time.sleep(1.5)
    elapsed = time.monotonic() - started
    assert _projection_count() >= 1
    assert elapsed < 5.0, f"CT-01 exceeded 5s budget ({elapsed:.2f}s)"


def test_ct02_before_interval_no_issue_yet(cron_enabled_client: TestClient) -> None:
    """CT-02: before first cron tick, no issue in projection store."""
    _intake_pair(cron_enabled_client, prefix="ct02")
    time.sleep(0.3)
    assert _projection_count() == 0


def test_ct03_cron_disabled_does_not_cluster(cron_disabled_client: TestClient) -> None:
    """CT-03: with CLUSTER_CRON_ENABLED=false, no issue after waiting."""
    _intake_pair(cron_disabled_client, prefix="ct03")
    time.sleep(1.5)
    assert _projection_count() == 0
