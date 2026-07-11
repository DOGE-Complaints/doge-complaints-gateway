"""GW-DRAFT-02 audit G1: GET /story-drafts/{id} browser session auth."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.identity.introspection_result import IntrospectionResult
from core.identity.me_client import IdentityMeClient, IdentityMeError
from tests.conftest import (
    GAUTH_TEST_IDENTITY_URL,
    GAUTH_TEST_SERVICE_TOKEN,
    GAUTH_TEST_USER_TOKEN,
)
from tests.intake_v2_fixtures import valid_v2_stash_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "86400")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"}


def _browser_headers(*, token: str = GAUTH_TEST_USER_TOKEN) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _valid_draft_payload() -> dict[str, Any]:
    return valid_v2_stash_payload()


def _patch_fetch_me(
    monkeypatch: pytest.MonkeyPatch,
    *,
    result: IntrospectionResult | None = None,
    error: Exception | None = None,
) -> None:
    def _fetch_me(self: IdentityMeClient, bearer_token: str) -> IntrospectionResult:
        _ = bearer_token
        if error is not None:
            raise error
        assert result is not None
        return result

    monkeypatch.setattr(IdentityMeClient, "fetch_me", _fetch_me)


def _stash_draft(client: TestClient) -> str:
    response = client.post(
        "/story-drafts",
        json=_valid_draft_payload(),
        headers=_service_headers(),
    )
    assert response.status_code == 201
    return response.json()["data"]["draft_id"]


def test_get_without_bearer_returns_401(client: TestClient) -> None:
    draft_id = _stash_draft(client)
    response = client.get(f"/story-drafts/{draft_id}")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_get_inactive_session_returns_401(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    _patch_fetch_me(monkeypatch, result=IntrospectionResult(active=False))

    response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_get_identity_me_down_returns_503(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    _patch_fetch_me(
        monkeypatch, error=IdentityMeError("Identity /me timed out.")
    )

    response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"


def test_get_unverified_phone_still_returns_200(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """GET requires active session only — no phone_verified gate (mvp §4)."""
    payload = _valid_draft_payload()
    draft_id = _stash_draft(client)
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub="unverified-reader", phone_verified=False
        ),
    )

    response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["narrative"]["original_text"] == payload["narrative"]["original_text"]


def test_get_verified_session_returns_200(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = _valid_draft_payload()
    draft_id = _stash_draft(client)
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub="verified-reader", phone_verified=True
        ),
    )

    response = client.get(
        f"/story-drafts/{draft_id}",
        headers=_browser_headers(),
    )

    assert response.status_code == 200
    assert response.json()["data"]["schema_version"] == payload["schema_version"]


def test_missing_identity_config_returns_503(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("IDENTITY_BASE_URL", raising=False)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as test_client:
            draft_id = _stash_draft(test_client)
            response = test_client.get(
                f"/story-drafts/{draft_id}",
                headers=_browser_headers(),
            )
    finally:
        _clear_api_dependencies_cache()

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
