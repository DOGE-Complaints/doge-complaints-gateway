from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _intake_payload(index: int) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": f"opaque-user-{index}"},
        "narrative": {
            "original_text": f"Street lights issue report #{index} near district center.",
            "language": "en",
            "title_hint": f"Street lights #{index}",
        },
    }


def _create_story(client: TestClient, *, index: int) -> str:
    response = client.post(
        "/intake/stories",
        json=_intake_payload(index),
        headers={"x-trace-id": f"trace-intake-{index}"},
    )
    assert response.status_code == 200
    return str(response.json()["data"]["story_id"])


def test_create_issue_returns_stable_envelope_and_projection(client: TestClient) -> None:
    story_a = _create_story(client, index=1)
    story_b = _create_story(client, index=2)

    response = client.post(
        "/issues",
        json={
            "cluster_id": "cluster-demo-1",
            "story_ids": [story_a, story_b],
            "readiness_score": 85,
            "title": "Street lights outage in district",
        },
        headers={"x-trace-id": "trace-issue-create-200"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["trace_id"] == "trace-issue-create-200"
    assert payload["data"]["issue_id"]
    assert payload["data"]["status"] == "promoted"
    assert payload["data"]["policy_version"] == "m2.spa_issue_derivation.v1"
    projection = payload["data"]["projection"]
    assert {"id", "status", "type", "labels", "title", "summary", "description"}.issubset(
        projection.keys()
    )


def test_create_issue_returns_400_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        "/issues",
        json={"cluster_id": "", "story_ids": [], "readiness_score": "high", "title": ""},
        headers={"x-trace-id": "trace-issue-create-400"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["trace_id"] == "trace-issue-create-400"
    assert payload["error"]["code"] == "DOMAIN_ERROR"


def test_create_issue_returns_400_for_unknown_story_id(client: TestClient) -> None:
    response = client.post(
        "/issues",
        json={
            "cluster_id": "cluster-demo-2",
            "story_ids": ["missing-story-1", "missing-story-2"],
            "readiness_score": 90,
            "title": "Unknown story linkage",
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == "DOMAIN_ERROR"
    assert "Unknown story_id" in payload["error"]["message"]
