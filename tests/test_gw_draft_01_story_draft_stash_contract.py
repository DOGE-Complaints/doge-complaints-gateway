"""GW-DRAFT-01: story draft stash contract (POST/GET /story-drafts)."""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN
from tests.intake_v2_fixtures import valid_v2_intake_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "86400")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"}


def _valid_draft_payload() -> dict[str, Any]:
    return valid_v2_intake_payload()


def test_post_story_drafts_returns_draft_id_without_creating_story(
    client: TestClient,
) -> None:
    deps = get_api_dependencies()
    stories_before = len(deps.story_intake_service.repository.list_stories())

    response = client.post(
        "/story-drafts",
        json=_valid_draft_payload(),
        headers=_service_headers(),
    )

    assert response.status_code == 201
    body = response.json()
    assert "draft_id" in body["data"]
    assert body["data"]["draft_id"]
    stories_after = len(deps.story_intake_service.repository.list_stories())
    assert stories_after == stories_before


def test_post_story_drafts_requires_service_token(client: TestClient) -> None:
    response = client.post("/story-drafts", json=_valid_draft_payload())
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_post_story_drafts_rejects_invalid_service_token(client: TestClient) -> None:
    response = client.post(
        "/story-drafts",
        json=_valid_draft_payload(),
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_post_story_drafts_returns_400_for_invalid_contract(client: TestClient) -> None:
    invalid_payload = _valid_draft_payload()
    invalid_payload.pop("narrative")

    response = client.post(
        "/story-drafts",
        json=invalid_payload,
        headers=_service_headers(),
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"


def test_get_story_drafts_returns_saved_payload(client: TestClient) -> None:
    payload = _valid_draft_payload()
    create_response = client.post(
        "/story-drafts",
        json=payload,
        headers=_service_headers(),
    )
    draft_id = create_response.json()["data"]["draft_id"]

    get_response = client.get(f"/story-drafts/{draft_id}")

    assert get_response.status_code == 200
    body = get_response.json()
    assert body["data"]["schema_version"] == payload["schema_version"]
    assert body["data"]["submitter"] == payload["submitter"]
    assert body["data"]["narrative"]["original_text"] == payload["narrative"]["original_text"]


def test_get_story_drafts_unknown_id_returns_404(client: TestClient) -> None:
    response = client.get("/story-drafts/unknown-draft-id-xyz")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"


def test_get_story_drafts_expired_draft_returns_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "1")
    _clear_api_dependencies_cache()

    create_response = client.post(
        "/story-drafts",
        json=_valid_draft_payload(),
        headers=_service_headers(),
    )
    draft_id = create_response.json()["data"]["draft_id"]
    time.sleep(1.1)

    get_response = client.get(f"/story-drafts/{draft_id}")
    assert get_response.status_code == 404
