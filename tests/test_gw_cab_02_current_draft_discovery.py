"""GW-CAB-02: GET /story-drafts/current user-scoped draft discovery."""

from __future__ import annotations

import time
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.domain import StoryDraftRecord
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN
from tests.intake_v2_fixtures import valid_v2_stash_payload
from tests.story_draft_intake_helpers import (
    browser_auth_headers,
    patch_identity_me_verified,
    stash_story_draft,
    submit_story_draft,
)


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


def _valid_stash_payload() -> dict[str, Any]:
    return valid_v2_stash_payload()


def test_gw_cab_02_current_missing_bearer_returns_401(client: TestClient) -> None:
    response = client.get("/story-drafts/current")
    assert response.status_code == 401


def test_gw_cab_02_current_null_when_no_pending_draft(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-user-empty")
    response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert response.status_code == 200
    assert response.json()["data"] is None


def test_gw_cab_02_association_on_read_enables_current(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-user-a")
    draft_id = stash_story_draft(client, _valid_stash_payload())
    read_response = client.get(
        f"/story-drafts/{draft_id}",
        headers=browser_auth_headers(),
    )
    assert read_response.status_code == 200

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    data = current_response.json()["data"]
    assert data is not None
    assert data["draft_id"] == draft_id
    assert data["last_edited_at"]


def test_gw_cab_02_cross_device_current_without_second_read(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-cross-device")
    draft_id = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )

    patch_identity_me_verified(monkeypatch, sub="cab02-cross-device")
    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"]["draft_id"] == draft_id


def test_gw_cab_02_isolation_user_b_does_not_see_user_a_draft(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    draft_id = stash_story_draft(client, _valid_stash_payload())
    patch_identity_me_verified(monkeypatch, sub="cab02-owner-a")
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )

    patch_identity_me_verified(monkeypatch, sub="cab02-owner-b")
    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"] is None


def test_gw_cab_02_first_wins_owner_preserved_when_user_b_reads_same_draft_id(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """G2: user-B read of known draft_id must not hijack ownership from user-A (first-wins)."""
    draft_id = stash_story_draft(client, _valid_stash_payload())
    patch_identity_me_verified(monkeypatch, sub="cab02-first-wins-a")
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )

    patch_identity_me_verified(monkeypatch, sub="cab02-first-wins-b")
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )
    assert client.get("/story-drafts/current", headers=browser_auth_headers()).json()["data"] is None

    patch_identity_me_verified(monkeypatch, sub="cab02-first-wins-a")
    current_a = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_a.status_code == 200
    data = current_a.json()["data"]
    assert data is not None
    assert data["draft_id"] == draft_id


def test_gw_cab_02_latest_non_expired_by_created_at(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-latest-user")
    draft_old = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_old}", headers=browser_auth_headers()).status_code
        == 200
    )
    draft_new = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_new}", headers=browser_auth_headers()).status_code
        == 200
    )

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"]["draft_id"] == draft_new


def test_gw_cab_02_expired_draft_excluded_from_current(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "1")
    _clear_api_dependencies_cache()
    patch_identity_me_verified(monkeypatch, sub="cab02-expired-user")
    draft_id = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )
    time.sleep(1.1)

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"] is None


def test_gw_cab_02_submitted_draft_excluded_from_current(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-submit-user", phone_verified=True)
    draft_id = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )
    submit_response = submit_story_draft(client, draft_id)
    assert submit_response.status_code in {200, 202}

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"] is None


def test_gw_cab_02_last_edited_at_equals_updated_at(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    patch_identity_me_verified(monkeypatch, sub="cab02-updated-at-user")
    draft_id = stash_story_draft(client, _valid_stash_payload())
    assert (
        client.get(f"/story-drafts/{draft_id}", headers=browser_auth_headers()).status_code
        == 200
    )

    deps = get_api_dependencies()
    record = deps.story_draft_repository.get_draft(draft_id)
    assert record is not None
    assert record.updated_at == record.created_at

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    data = current_response.json()["data"]
    assert data["last_edited_at"] == record.updated_at.isoformat()


def test_gw_cab_02_manual_expired_association_excluded(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Expired row remains in draft_owner but join/TTL excludes it from current."""
    patch_identity_me_verified(monkeypatch, sub="cab02-manual-expired")
    deps = get_api_dependencies()
    now = datetime.now(UTC)
    expired_record = StoryDraftRecord(
        draft_id="cab02-expired-manual",
        payload=_valid_stash_payload(),
        created_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
        updated_at=now - timedelta(hours=2),
    )
    deps.story_draft_repository.save_draft(expired_record)
    deps.draft_owner_repository.set_owner("cab02-expired-manual", "cab02-manual-expired")

    current_response = client.get("/story-drafts/current", headers=browser_auth_headers())
    assert current_response.status_code == 200
    assert current_response.json()["data"] is None
