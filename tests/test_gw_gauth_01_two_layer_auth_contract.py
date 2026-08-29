"""GW-GAUTH-01: service-layer auth on public-content write paths (GW-DRAFT-04 service-only)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN, GAUTH_TEST_USER_TOKEN, gauth_intake_headers
from tests.intake_v2_fixtures import valid_v2_stash_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_stash_payload() -> dict[str, Any]:
    return valid_v2_stash_payload(
        narrative={
            "original_text": "Pothole on main street.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Pothole"},
            "description": {"et": "d", "ru": "d", "en": "Pothole on main street."},
        },
    )


def test_story_drafts_stash_without_service_token_rejected(client: TestClient) -> None:
    response = client.post(
        "/story-drafts",
        json=_valid_stash_payload(),
        headers={"X-User-Token": GAUTH_TEST_USER_TOKEN},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert "service" in body["error"]["message"].lower()


def test_story_drafts_stash_service_only_accepted(client: TestClient) -> None:
    response = client.post(
        "/story-drafts",
        json=_valid_stash_payload(),
        headers={
            "Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}",
            "idempotency-key": "gauth-contract-ok",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["draft_id"]


def test_story_drafts_stash_rejects_submitter_in_payload(client: TestClient) -> None:
    payload = _valid_stash_payload()
    payload["submitter"] = {
        "external_user_id": "should-not-be-here",
        "identity_issuer": "https://idp.example.com/eid",
    }
    response = client.post(
        "/story-drafts",
        json=payload,
        headers={"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"},
    )
    assert response.status_code in {400, 422}


def test_story_drafts_stash_rejects_when_service_token_env_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SERVICE_API_TOKEN", raising=False)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/story-drafts",
                json=_valid_stash_payload(),
                headers=gauth_intake_headers(),
            )
    finally:
        _clear_api_dependencies_cache()
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_tallinn_issues_post_requires_service_auth(client: TestClient) -> None:
    bare = client.post("/node/issues", json={"title": "test"})
    assert bare.status_code == 401
    with_service = client.post(
        "/node/issues",
        json={"title": "test"},
        headers={"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"},
    )
    assert with_service.status_code in {200, 201, 202, 400, 422}
