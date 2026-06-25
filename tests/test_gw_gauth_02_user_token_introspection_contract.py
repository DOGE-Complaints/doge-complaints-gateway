"""GW-GAUTH-02: identity introspection client and verify-gated user gate."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.identity.introspection_client import (
    IdentityIntrospectionClient,
    IdentityIntrospectionError,
    IntrospectionResult,
    _parse_introspection_body,
)
from tests.conftest import (
    GAUTH_TEST_IDENTITY_SERVICE_TOKEN,
    GAUTH_TEST_IDENTITY_URL,
    GAUTH_TEST_SERVICE_TOKEN,
    GAUTH_TEST_USER_TOKEN,
    gauth_intake_headers,
)
from tests.intake_v2_fixtures import valid_v2_intake_payload


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_INTROSPECT_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("IDENTITY_SERVICE_TOKEN", GAUTH_TEST_IDENTITY_SERVICE_TOKEN)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_intake_payload() -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "payload-submitter-id",
            "identity_issuer": "https://idp.example.com/eid",
        },
        narrative={
            "original_text": "Pothole on main street.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Pothole"},
            "description": {"et": "d", "ru": "d", "en": "Pothole on main street."},
        },
    )


def _patch_introspect(
    monkeypatch: pytest.MonkeyPatch,
    *,
    result: IntrospectionResult | None = None,
    error: Exception | None = None,
) -> list[str]:
    seen_tokens: list[str] = []

    def _introspect(self: IdentityIntrospectionClient, user_token: str) -> IntrospectionResult:
        seen_tokens.append(user_token)
        if error is not None:
            raise error
        assert result is not None
        return result

    monkeypatch.setattr(IdentityIntrospectionClient, "introspect", _introspect)
    return seen_tokens


def test_parse_introspection_body_active_verified() -> None:
    parsed = _parse_introspection_body(
        {"active": True, "sub": "user-42", "phone_verified": True}
    )
    assert parsed.active is True
    assert parsed.sub == "user-42"
    assert parsed.phone_verified is True


def test_parse_introspection_body_inactive() -> None:
    parsed = _parse_introspection_body({"active": False})
    assert parsed.active is False
    assert parsed.sub is None


def test_introspect_client_posts_form_with_service_bearer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    class _FakeResponse:
        status_code = 200

        @staticmethod
        def json() -> dict[str, Any]:
            return {"active": True, "sub": "sub-1", "phone_verified": False}

    class _FakeClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _ = args, kwargs

        def __enter__(self) -> _FakeClient:
            return self

        def __exit__(self, *args: Any) -> None:
            _ = args

        def post(self, url: str, **kwargs: Any) -> _FakeResponse:
            captured["url"] = url
            captured.update(kwargs)
            return _FakeResponse()

    monkeypatch.setattr(httpx, "Client", _FakeClient)
    client = IdentityIntrospectionClient(
        introspect_url=f"{GAUTH_TEST_IDENTITY_URL}/oauth/introspect",
        service_token=GAUTH_TEST_IDENTITY_SERVICE_TOKEN,
        timeout_s=5.0,
    )
    result = client.introspect("user-access-token")
    assert result.active is True
    assert result.sub == "sub-1"
    assert result.phone_verified is False
    assert captured["url"] == f"{GAUTH_TEST_IDENTITY_URL}/oauth/introspect"
    assert captured["data"] == {"token": "user-access-token"}
    assert captured["headers"]["Authorization"] == (
        f"Bearer {GAUTH_TEST_IDENTITY_SERVICE_TOKEN}"
    )


def test_active_verified_introspection_allows_intake(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen = _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(active=True, sub="introspected-sub", phone_verified=True),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth02-active"}),
    )
    assert response.status_code == 202
    assert seen == [GAUTH_TEST_USER_TOKEN]


def test_inactive_token_rejected_fail_closed(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_introspect(monkeypatch, result=IntrospectionResult(active=False))
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(),
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_identity_down_rejected_fail_closed(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _patch_introspect(
        monkeypatch, error=IdentityIntrospectionError("Identity introspection timed out.")
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(),
    )
    assert response.status_code == 401
    assert "introspection" in response.json()["error"]["message"].lower()


def test_phone_verified_comes_from_identity_not_payload_jwt(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Status must not be inferred from user token body — only identity JSON."""
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(active=True, sub="from-identity", phone_verified=False),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(
            user_token="eyJhbGciOiJub25lIn0.eyJwaG9uZV92ZXJpZmllZCI6dHJ1ZX0."
        ),
    )
    assert response.status_code == 202


def test_missing_identity_config_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("IDENTITY_INTROSPECT_URL", raising=False)
    monkeypatch.delenv("IDENTITY_SERVICE_TOKEN", raising=False)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/intake/stories",
                json=_valid_intake_payload(),
                headers=gauth_intake_headers(),
            )
    finally:
        _clear_api_dependencies_cache()
    assert response.status_code == 401
    assert "not configured" in response.json()["error"]["message"].lower()
