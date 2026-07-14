"""GW-CAB-01: GET /story-activity user-scoped list + metrics."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import InMemoryIssueStoryLinkStore
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN, GAUTH_TEST_USER_TOKEN
from tests.intake_v2_fixtures import make_story_record


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


def _user_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {GAUTH_TEST_USER_TOKEN}"}


def _patch_me_sub(monkeypatch: pytest.MonkeyPatch, sub: str) -> None:
    from core.identity.introspection_result import IntrospectionResult
    from core.identity.me_client import IdentityMeClient

    def _fetch_me(self: IdentityMeClient, bearer_token: str) -> IntrospectionResult:
        _ = bearer_token
        return IntrospectionResult(active=True, sub=sub, phone_verified=True)

    monkeypatch.setattr(IdentityMeClient, "fetch_me", _fetch_me)


def _story_repo():
    return get_api_dependencies().story_intake_service.repository


def _projection_store():
    store = get_api_dependencies().issue_projection_read_store
    assert hasattr(store, "save_projection")
    return store


def _link_store() -> InMemoryIssueStoryLinkStore:
    store = get_api_dependencies().issue_create_service.issue_story_link_store
    assert isinstance(store, InMemoryIssueStoryLinkStore)
    return store


def _save_projection(*, issue_id: str, status: str) -> None:
    _projection_store().save_projection(
        issue_id=issue_id,
        status=status,
        payload={
            "id": issue_id,
            "status": status,
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": "t", "ru": "t", "en": "Cabinet test"},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "d", "ru": "d", "en": "d"},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


def test_gw_cab_01_missing_bearer_returns_401(client: TestClient) -> None:
    response = client.get("/story-activity")
    assert response.status_code == 401


def test_gw_cab_01_empty_activity_for_user(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_me_sub(monkeypatch, "cab-user-empty")
    response = client.get("/story-activity", headers=_user_headers())
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["metrics"] == {"submitted": 0, "published": 0, "under_review": 0}
    assert data["stories"] == []


def test_gw_cab_01_scoping_isolates_users(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _story_repo()
    repo.save_story(
        make_story_record(
            story_id="cab-story-a",
            submitter_external_user_id="cab-user-a",
            created_at=datetime(2026, 7, 10, 12, 0, tzinfo=UTC),
        )
    )
    repo.save_story(
        make_story_record(
            story_id="cab-story-b",
            submitter_external_user_id="cab-user-b",
            created_at=datetime(2026, 7, 11, 12, 0, tzinfo=UTC),
        )
    )
    _patch_me_sub(monkeypatch, "cab-user-a")
    response = client.get("/story-activity", headers=_user_headers())
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["metrics"]["submitted"] == 1
    assert len(data["stories"]) == 1
    assert data["stories"][0]["story_id"] == "cab-story-a"


def test_gw_cab_01_metrics_and_status_mapping(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _story_repo()
    repo.save_story(
        make_story_record(
            story_id="cab-pub",
            submitter_external_user_id="cab-user-metrics",
            lifecycle_status=StoryLifecycleStatus.CLUSTERED,
        )
    )
    repo.save_story(
        make_story_record(
            story_id="cab-review",
            submitter_external_user_id="cab-user-metrics",
        )
    )
    repo.save_story(
        make_story_record(
            story_id="cab-nolink",
            submitter_external_user_id="cab-user-metrics",
        )
    )
    links = _link_store()
    links.save_issue_story_links(
        issue_id="issue-cab-pub",
        cluster_id="cluster-1",
        story_ids=("cab-pub",),
    )
    links.save_issue_story_links(
        issue_id="issue-cab-review",
        cluster_id="cluster-2",
        story_ids=("cab-review",),
    )
    _save_projection(issue_id="issue-cab-pub", status="PUBLISHED")
    _save_projection(issue_id="issue-cab-review", status="IN_REVIEW")

    _patch_me_sub(monkeypatch, "cab-user-metrics")
    response = client.get("/story-activity", headers=_user_headers())
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["metrics"] == {"submitted": 3, "published": 1, "under_review": 2}
    by_id = {row["story_id"]: row["status"] for row in data["stories"]}
    assert by_id["cab-pub"] == "published"
    assert by_id["cab-review"] == "under_review"
    assert by_id["cab-nolink"] == "under_review"
    for row in data["stories"]:
        assert row["status"] in {"published", "under_review"}
        assert "created_at" in row


def test_gw_cab_01_response_has_no_issue_details(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_me_sub(monkeypatch, "cab-user-empty")
    response = client.get("/story-activity", headers=_user_headers())
    body = response.json()
    assert "issues" not in body["data"]
    assert "pagination" not in body["data"]
