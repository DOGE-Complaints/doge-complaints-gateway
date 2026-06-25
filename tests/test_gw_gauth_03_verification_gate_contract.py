"""GW-GAUTH-03: phone_verified gate + verification_required (403, OAUTH-04)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.config import load_config_from_env
from core.identity.introspection_client import (
    IdentityIntrospectionClient,
    IdentityIntrospectionError,
    IntrospectionResult,
)
from core.identity.verification_gate import (
    VerificationGateOutcome,
    evaluate_verification_gate,
)
from core.identity.verify_url import build_verify_url
from tests.conftest import (
    GAUTH_TEST_IDENTITY_SERVICE_TOKEN,
    GAUTH_TEST_IDENTITY_URL,
    GAUTH_TEST_SERVICE_TOKEN,
    GAUTH_TEST_USER_TOKEN,
    gauth_intake_headers,
)
from tests.intake_v2_fixtures import valid_v2_intake_payload

GAUTH_TEST_SPA_VERIFY_BASE = "https://spa.test"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_INTROSPECT_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("IDENTITY_SERVICE_TOKEN", GAUTH_TEST_IDENTITY_SERVICE_TOKEN)
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_intake_payload() -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "gauth03-user",
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
) -> None:
    def _introspect(self: IdentityIntrospectionClient, user_token: str) -> IntrospectionResult:
        _ = user_token
        if error is not None:
            raise error
        assert result is not None
        return result

    monkeypatch.setattr(IdentityIntrospectionClient, "introspect", _introspect)


def _story_count() -> int:
    repo = get_api_dependencies().story_intake_service.repository
    return len(repo.list_stories())


def test_build_verify_url_from_spa_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
    config = load_config_from_env()
    assert build_verify_url(config) == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify"
    assert (
        build_verify_url(config, return_context="intake")
        == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify?context=intake"
    )


def test_evaluate_verification_gate_branches() -> None:
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", phone_verified=True)
        )
        is VerificationGateOutcome.ALLOW
    )
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", phone_verified=False)
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )
    assert (
        evaluate_verification_gate(IntrospectionResult(active=False))
        is VerificationGateOutcome.UNAUTHORIZED
    )


def test_verified_introspection_allows_intake(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _story_count()
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(active=True, sub="verified-sub", phone_verified=True),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth03-verified"}),
    )
    assert response.status_code == 202
    assert response.json()["data"]["story_id"]
    assert _story_count() == before + 1


def test_unverified_returns_403_verification_required_oauth04(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _story_count()
    _patch_introspect(
        monkeypatch,
        result=IntrospectionResult(active=True, sub="unverified-sub", phone_verified=False),
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(
            user_token="eyJhbGciOiJub25lIn0.eyJwaG9uZV92ZXJpZmllZCI6dHJ1ZX0."
        ),
    )
    assert response.status_code == 403
    body = response.json()
    assert body["error"]["code"] == "VERIFICATION_REQUIRED"
    details = body["error"]["details"]
    assert details["error"] == "verification_required"
    assert details["verify_url"] == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify"
    assert "reason" in details
    assert _story_count() == before


def test_inactive_token_returns_401_not_verification_required(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _story_count()
    _patch_introspect(monkeypatch, result=IntrospectionResult(active=False))
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(),
    )
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert body["error"]["details"].get("error") != "verification_required"
    assert _story_count() == before


def test_identity_down_returns_503_not_verification_required(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _story_count()
    _patch_introspect(
        monkeypatch, error=IdentityIntrospectionError("Identity introspection timed out.")
    )
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(),
    )
    assert response.status_code == 503
    body = response.json()
    assert body["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert body["error"]["details"].get("error") != "verification_required"
    assert _story_count() == before


def test_missing_identity_config_returns_503_not_verification_required(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("IDENTITY_INTROSPECT_URL", raising=False)
    monkeypatch.delenv("IDENTITY_SERVICE_TOKEN", raising=False)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as client:
            before = _story_count()
            response = client.post(
                "/intake/stories",
                json=_valid_intake_payload(),
                headers=gauth_intake_headers(),
            )
    finally:
        _clear_api_dependencies_cache()
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert _story_count() == before
