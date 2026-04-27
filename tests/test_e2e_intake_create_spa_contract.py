from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.intake import INTAKE_SCHEMA_VERSION

REQUIRED_SPA_KEYS = frozenset({"id", "status", "type", "labels", "title", "summary", "description"})


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


def _intake_payload(external_user_id: str, text: str) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": external_user_id},
        "narrative": {
            "original_text": text,
            "language": "en",
            "title_hint": "Issue report",
        },
    }


def _create_story(client: TestClient, *, external_user_id: str, text: str) -> str:
    response = client.post("/intake/stories", json=_intake_payload(external_user_id, text))
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["schema_version"] == "m2.story_intake_response.v1"
    return str(payload["data"]["story_id"])


def test_e2e_intake_create_issue_to_spa_contract_happy_path(client: TestClient) -> None:
    _create_story(
        client,
        external_user_id="e2e-user-1",
        text="Road lights are broken and unsafe for pedestrians in district A.",
    )
    _create_story(
        client,
        external_user_id="e2e-user-2",
        text="Road lights are broken and unsafe for pedestrians in district A.",
    )
    deps = get_api_dependencies()
    issue_create = deps.story_cluster_orchestrator.issue_create_service
    projection_store = issue_create.issue_projection_store
    assert projection_store is not None
    rows = getattr(projection_store, "_rows")
    assert rows
    issue_id, first = next(iter(rows.items()))
    projection = first["payload"]
    assert REQUIRED_SPA_KEYS.issubset(projection.keys())
    embedding_store = issue_create.issue_projection_embedding_store
    assert embedding_store is not None
    embedding_rows = getattr(embedding_store, "_rows")
    assert embedding_rows
    assert embedding_rows[0]["embedding_policy_version"] == "m2.issue_embedding_policy.v1"
    link_store = issue_create.issue_story_link_store
    assert link_store is not None
    link_rows = getattr(link_store, "_rows")
    assert issue_id in link_rows
    _, linked_story_ids = link_rows[issue_id]
    assert len(linked_story_ids) == 2


def test_e2e_rejects_invalid_intake_payload(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json={
            "schema_version": "m2.story_intake_envelope.v1",
            "submitter": {"external_user_id": "bad"},
            # narrative intentionally missing
        },
        headers={"x-trace-id": "trace-e2e-intake-bad"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-e2e-intake-bad"
    assert payload["error"]["code"] == "DOMAIN_ERROR"


def test_e2e_story_first_boundary_and_min_stories_gate(client: TestClient) -> None:
    _create_story(
        client,
        external_user_id="e2e-user-3",
        text="Single story is not enough for promotion gate baseline.",
    )
    deps = get_api_dependencies()
    projection_store = deps.story_cluster_orchestrator.issue_create_service.issue_projection_store
    assert projection_store is not None
    rows_before = getattr(projection_store, "_rows")
    assert rows_before == {}

    response = client.post("/issues", json={"cluster_id": "manual"})
    assert response.status_code == 404
