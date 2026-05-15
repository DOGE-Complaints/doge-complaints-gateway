from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.intake import INTAKE_SCHEMA_VERSION
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict


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
            "title": {"et": "t", "ru": "t", "en": "Story package issue tracking"},
            "description": {"et": "d", "ru": "d", "en": text},
            "canonical_type": "infrastructure",
            "canonical_labels": ["roads", "broken_infrastructure"],
        },
    }


def test_story_package_issue_tracking_materialization_and_audit(client: TestClient) -> None:
    response_a = client.post(
        "/intake/stories",
        json=_payload("tracking-user-1", "Water supply issue in district C keeps repeating."),
    )
    response_b = client.post(
        "/intake/stories",
        json=_payload("tracking-user-2", "Water supply issue in district C keeps repeating."),
    )
    assert response_a.status_code == 202
    assert response_b.status_code == 202

    story_id_a = response_a.json()["data"]["story_id"]
    story_id_b = response_b.json()["data"]["story_id"]

    deps = get_api_dependencies()
    deps.story_cluster_orchestrator.process_all_pending()
    issue_create = deps.story_cluster_orchestrator.issue_create_service

    # Projection and link rows confirm materialized issue creation.
    projection_store = issue_create.issue_projection_store
    assert projection_store is not None
    projection_rows = getattr(projection_store, "_rows")
    assert projection_rows
    issue_id = next(iter(projection_rows.keys()))

    link_store = issue_create.issue_story_link_store
    assert link_store is not None
    link_rows = getattr(link_store, "_rows")
    assert issue_id in link_rows
    _, linked_story_ids = link_rows[issue_id]
    assert set(linked_story_ids) >= {story_id_a, story_id_b}

    # Promotion audit trail is expected for auto-approve flow.
    audit_log = issue_create.promotion_service.audit_log
    audit_entries = getattr(audit_log, "_entries")
    assert issue_id in audit_entries
    entries = audit_entries[issue_id]
    assert entries
    assert entries[-1].rationale == "http_create_issue_auto_promote"
