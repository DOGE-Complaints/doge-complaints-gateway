"""GW-DRAFT-02: browser submit + phone_verified gate (POST /story-drafts/{id}/submit)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.identity.introspection_result import IntrospectionResult
from core.identity.me_client import IdentityMeClient, IdentityMeError
from tests.conftest import (
    GAUTH_TEST_IDENTITY_URL,
    GAUTH_TEST_SERVICE_TOKEN,
    GAUTH_TEST_USER_TOKEN,
)
from tests.intake_v2_fixtures import valid_v2_intake_payload

GAUTH_TEST_SPA_VERIFY_BASE = "https://spa.test"
VERIFIED_SUB = "draft02-verified-sub"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
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
    return valid_v2_intake_payload(
        submitter={
            "external_user_id": "claimed-draft-submitter",
            "identity_issuer": "https://idp.example.com/eid",
        },
    )


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


def _story_count() -> int:
    return len(get_api_dependencies().story_intake_service.repository.list_stories())


def _latest_story_submitter_external_id() -> str:
    stories = get_api_dependencies().story_intake_service.repository.list_stories()
    assert stories
    return stories[-1].submitter_external_user_id


def test_verified_browser_submit_returns_202_and_authoritative_submitter(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    before = _story_count()
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub=VERIFIED_SUB, phone_verified=True
        ),
    )

    response = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )

    assert response.status_code == 202
    assert response.json()["data"]["story_id"]
    assert _story_count() == before + 1
    assert _latest_story_submitter_external_id() == VERIFIED_SUB


def test_unverified_returns_403_verification_required(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    before = _story_count()
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub="unverified-sub", phone_verified=False
        ),
    )

    response = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )

    assert response.status_code == 403
    body = response.json()
    assert body["error"]["code"] == "VERIFICATION_REQUIRED"
    details = body["error"]["details"]
    assert details["error"] == "verification_required"
    assert details["verify_url"] == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify"
    assert _story_count() == before
    assert get_api_dependencies().story_draft_repository.get_draft(draft_id) is not None


def test_missing_bearer_returns_401(client: TestClient) -> None:
    draft_id = _stash_draft(client)
    before = _story_count()

    response = client.post(f"/story-drafts/{draft_id}/submit")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
    assert _story_count() == before


def test_inactive_token_returns_401(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    before = _story_count()
    _patch_fetch_me(monkeypatch, result=IntrospectionResult(active=False))

    response = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
    assert _story_count() == before


def test_identity_me_down_returns_503(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    before = _story_count()
    _patch_fetch_me(
        monkeypatch, error=IdentityMeError("Identity /me timed out.")
    )

    response = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert _story_count() == before


def test_repeat_submit_is_idempotent(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = _stash_draft(client)
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub=VERIFIED_SUB, phone_verified=True
        ),
    )

    first = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )
    assert first.status_code == 202
    story_id = first.json()["data"]["story_id"]
    before = _story_count()

    second = client.post(
        f"/story-drafts/{draft_id}/submit",
        headers=_browser_headers(),
    )

    assert second.status_code == 202
    assert second.json()["data"]["story_id"] == story_id
    assert _story_count() == before
    assert get_api_dependencies().story_draft_repository.get_draft(draft_id) is None


def test_unknown_draft_returns_404(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    before = _story_count()
    _patch_fetch_me(
        monkeypatch,
        result=IntrospectionResult(
            active=True, sub=VERIFIED_SUB, phone_verified=True
        ),
    )

    response = client.post(
        "/story-drafts/unknown-draft-id-xyz/submit",
        headers=_browser_headers(),
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"
    assert _story_count() == before
