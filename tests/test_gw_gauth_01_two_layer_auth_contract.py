"""GW-GAUTH-01: two-layer auth contract on public-content write paths (stub user gate → GAUTH-02)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN, GAUTH_TEST_USER_TOKEN, gauth_intake_headers
from tests.intake_v2_fixtures import valid_v2_intake_payload


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


def _valid_intake_payload() -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "gauth-contract-user",
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


def test_intake_without_service_token_rejected_not_noop(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers={"X-User-Token": GAUTH_TEST_USER_TOKEN},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert "service" in body["error"]["message"].lower()


def test_intake_service_only_without_user_token_rejected(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers={"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"
    assert "user" in body["error"]["message"].lower()


def test_intake_with_service_and_user_token_accepted(client: TestClient) -> None:
    response = client.post(
        "/intake/stories",
        json=_valid_intake_payload(),
        headers=gauth_intake_headers(extra={"idempotency-key": "gauth-contract-ok"}),
    )
    assert response.status_code == 202
    assert response.json()["data"]["story_id"]


def test_service_only_does_not_create_story_for_arbitrary_submitter(
    client: TestClient,
) -> None:
    """Service trust alone must not pass verify-gated intake (user layer stub)."""
    payload = _valid_intake_payload()
    payload["submitter"]["external_user_id"] = "arbitrary-untrusted-user"
    response = client.post(
        "/intake/stories",
        json=payload,
        headers={"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"},
    )
    assert response.status_code == 401
    assert "error" in response.json()


def test_intake_rejects_when_service_token_env_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SERVICE_API_TOKEN", raising=False)
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
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
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_tallinn_issues_post_requires_two_layer_auth(client: TestClient) -> None:
    bare = client.post("/tallinn/issues", json={"title": "test"})
    assert bare.status_code == 401
    service_only = client.post(
        "/tallinn/issues",
        json={"title": "test"},
        headers={"Authorization": f"Bearer {GAUTH_TEST_SERVICE_TOKEN}"},
    )
    assert service_only.status_code == 401
