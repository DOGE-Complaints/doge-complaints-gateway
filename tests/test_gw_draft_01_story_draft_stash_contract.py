"""GW-DRAFT-01: story draft stash contract (POST/GET /story-drafts)."""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN, GAUTH_TEST_USER_TOKEN
from core.identity.introspection_result import IntrospectionResult
from core.identity.me_client import IdentityMeClient
from tests.intake_v2_fixtures import valid_v2_intake_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "86400")
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"}


def _browser_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {GAUTH_TEST_USER_TOKEN}"}


def _patch_active_me(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fetch_me(self: IdentityMeClient, bearer_token: str) -> IntrospectionResult:
        _ = bearer_token
        return IntrospectionResult(active=True, sub="draft01-reader", phone_verified=True)

    monkeypatch.setattr(IdentityMeClient, "fetch_me", _fetch_me)


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


def test_get_story_drafts_returns_saved_payload(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_active_me(monkeypatch)
    payload = _valid_draft_payload()
    create_response = client.post(
        "/story-drafts",
        json=payload,
        headers=_service_headers(),
    )
    draft_id = create_response.json()["data"]["draft_id"]

    get_response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )

    assert get_response.status_code == 200
    body = get_response.json()
    assert body["data"]["schema_version"] == payload["schema_version"]
    assert body["data"]["submitter"] == payload["submitter"]
    assert body["data"]["narrative"]["original_text"] == payload["narrative"]["original_text"]


def test_get_story_drafts_unknown_id_returns_404(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_active_me(monkeypatch)
    response = client.get(
        "/story-drafts/unknown-draft-id-xyz",
        headers=_browser_headers(),
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"


def test_get_story_drafts_expired_draft_returns_404(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "1")
    _clear_api_dependencies_cache()
    _patch_active_me(monkeypatch)

    create_response = client.post(
        "/story-drafts",
        json=_valid_draft_payload(),
        headers=_service_headers(),
    )
    draft_id = create_response.json()["data"]["draft_id"]
    time.sleep(1.1)

    get_response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )
    assert get_response.status_code == 404
