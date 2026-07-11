"""GW-PUBLIC-01 (M-5): regression guard — public read routes stay open; write routes stay closed."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN
from tests.intake_v2_fixtures import valid_v2_intake_payload

_FORBIDDEN_READ_STATUSES = frozenset({401, 403})


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "86400")
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _valid_draft_payload() -> dict[str, Any]:
    return valid_v2_intake_payload()


def _save_projection(issue_id: str) -> None:
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    store.save_projection(
        issue_id=issue_id,
        status="PUBLISHED",
        payload={
            "id": issue_id,
            "status": "PUBLISHED",
            "type": "INCIDENT",
            "labels": ["infrastructure"],
            "title": {"et": "t", "ru": "t", "en": "Public regression"},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "d", "ru": "d", "en": "d"},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


def test_gw_public_01_t01_list_without_auth_returns_200(client: TestClient) -> None:
    response = client.get("/tallinn/issues")
    assert response.status_code == 200
    assert response.status_code not in _FORBIDDEN_READ_STATUSES
    assert "issues" in response.json()["data"]


def test_gw_public_01_t02_get_by_id_unknown_without_auth_not_401(
    client: TestClient,
) -> None:
    response = client.get("/tallinn/issues/gw-public-01-nonexistent")
    assert response.status_code == 404
    assert response.status_code not in _FORBIDDEN_READ_STATUSES


def test_gw_public_01_t02_get_by_id_known_without_auth_returns_200(
    client: TestClient,
) -> None:
    issue_id = "gw-public-01-known-issue"
    _save_projection(issue_id)
    response = client.get(f"/tallinn/issues/{issue_id}")
    assert response.status_code == 200
    assert response.status_code not in _FORBIDDEN_READ_STATUSES
    assert response.json()["data"]["issue"]["id"] == issue_id


def test_gw_public_01_t03_post_story_drafts_without_service_token_401(
    client: TestClient,
) -> None:
    response = client.post("/story-drafts", json=_valid_draft_payload())
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.gauth_raw_client()
def test_gw_public_01_t04_post_tallinn_issues_without_service_token_401(
    client: TestClient,
) -> None:
    response = client.post("/tallinn/issues", json={"title": "regression probe"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
