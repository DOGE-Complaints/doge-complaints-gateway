from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION

REQUIRED_SPA_KEYS = frozenset({"id", "status", "type", "labels", "title", "summary", "description"})


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
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
    story_1 = _create_story(
        client,
        external_user_id="e2e-user-1",
        text="Road lights are broken and unsafe for pedestrians in district A.",
    )
    story_2 = _create_story(
        client,
        external_user_id="e2e-user-2",
        text="Infrastructure outage continues for second day in district A.",
    )

    response = client.post(
        "/issues",
        json={
            "cluster_id": "cluster-e2e-1",
            "story_ids": [story_1, story_2],
            "readiness_score": 90,
            "title": "District A safety and infrastructure outage",
        },
        headers={"x-trace-id": "trace-e2e-happy"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["trace_id"] == "trace-e2e-happy"
    assert payload["data"]["issue_id"]
    assert payload["data"]["status"] == "promoted"
    assert payload["data"]["policy_version"] == "m2.spa_issue_derivation.v1"
    projection = payload["data"]["projection"]
    assert REQUIRED_SPA_KEYS.issubset(projection.keys())
    assert projection["id"] == payload["data"]["issue_id"]


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


def test_e2e_rejects_create_issue_on_gate_failure(client: TestClient) -> None:
    story_1 = _create_story(
        client,
        external_user_id="e2e-user-3",
        text="Single story is not enough for promotion gate baseline.",
    )
    story_2 = _create_story(
        client,
        external_user_id="e2e-user-4",
        text="Second story exists but readiness score is still too low.",
    )

    response = client.post(
        "/issues",
        json={
            "cluster_id": "cluster-e2e-2",
            "story_ids": [story_1, story_2],
            "readiness_score": 10,
            "title": "Low-readiness candidate should fail",
        },
        headers={"x-trace-id": "trace-e2e-gate-fail"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-e2e-gate-fail"
    assert payload["error"]["code"] == "DOMAIN_ERROR"
    assert "Promotion gates failed" in payload["error"]["message"]
