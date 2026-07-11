from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.intake import INTAKE_SCHEMA_VERSION
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
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _payload(user: str, text: str) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": user, "identity_issuer": "https://idp.example.com/eid"},
        "narrative": {
            "original_text": text,
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Create story fullpath"},
            "description": {"et": "d", "ru": "d", "en": text},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "broken_infrastructure", "safety"],
        },
        "origin": {"source": "tc_p0_03"},
    }


def test_e2e_create_story_fullpath_with_idempotency_and_materialization(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload_user_1 = _payload("fullpath-user-1", "Street lights are broken in district B.")
    payload_user_2 = _payload("fullpath-user-2", "Street lights are broken in district B.")
    draft_id = stash_story_draft(
        client,
        payload_user_1,
        headers={"idempotency-key": "tc-p0-03-idem-1"},
    )
    patch_identity_me_verified(monkeypatch, sub=submitter_external_id(payload_user_1))
    response_1 = submit_story_draft(
        client, draft_id, headers={"x-trace-id": "trace-fullpath-1"}
    )
    response_2 = submit_story_draft(
        client, draft_id, headers={"x-trace-id": "trace-fullpath-2"}
    )
    response_3 = post_intake_via_story_drafts(
        client,
        json=payload_user_2,
        headers={"x-trace-id": "trace-fullpath-3", "idempotency-key": "tc-p0-03-idem-2"},
        monkeypatch=monkeypatch,
    )

    assert response_1.status_code == 202
    assert response_2.status_code == 202
    assert response_3.status_code == 202

    payload_1 = response_1.json()
    payload_2 = response_2.json()
    payload_3 = response_3.json()
    story_id_1 = payload_1["data"]["story_id"]
    story_id_2 = payload_2["data"]["story_id"]
    story_id_3 = payload_3["data"]["story_id"]

    assert story_id_1 == story_id_2
    assert story_id_1 != story_id_3
    assert payload_1["trace_id"] == "trace-fullpath-1"
    assert payload_2["trace_id"] == "trace-fullpath-2"
    assert payload_3["trace_id"] == "trace-fullpath-3"

    deps = get_api_dependencies()
    deps.story_cluster_orchestrator.process_all_pending()
    issue_create = deps.story_cluster_orchestrator.issue_create_service

    projection_store = issue_create.issue_projection_store
    assert projection_store is not None
    projection_rows = getattr(projection_store, "_rows")
    assert projection_rows

    embedding_store = issue_create.issue_projection_embedding_store
    assert embedding_store is not None
    embedding_rows = getattr(embedding_store, "_rows")
    assert embedding_rows
    assert embedding_rows[0]["embedding_policy_version"] == "m3.doge_issue_embedding_policy.v1"

    link_store = issue_create.issue_story_link_store
    assert link_store is not None
    link_rows = getattr(link_store, "_rows")
    assert link_rows
    _, linked_story_ids = next(iter(link_rows.values()))
    assert len(linked_story_ids) >= 2


def test_e2e_create_story_fullpath_rejects_invalid_payload(client: TestClient) -> None:
    response = post_intake_via_story_drafts(
        client,
        json={
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "bad", "identity_issuer": "https://idp.example.com/eid"},
        },
        headers={"x-trace-id": "trace-fullpath-bad"},
    )
    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-fullpath-bad"
    assert payload["error"]["code"] == "DOMAIN_ERROR"
