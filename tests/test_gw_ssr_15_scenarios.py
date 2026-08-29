"""GW-SSR-15: civic / pack / Pulse≠Issues / dual + public path / legacy 404."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.cluster import ClusterLens
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryRepository,
)
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN
from tests.test_gw_ssr_04_schema_driven_cluster_lens import _pack_story
from tests.test_gw_ssr_10_orchestrator_dual import (
    _dual_bound_story,
    _dual_orchestrator,
    _lenses_for,
    _write_dual_legal_root,
)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _save_civic_projection(issue_id: str) -> None:
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
            "title": {"et": "t", "ru": "t", "en": "Civic unbound"},
            "summary": {"et": "s", "ru": "s", "en": "s"},
            "description": {"et": "d", "ru": "d", "en": "d"},
        },
        policy_version="m3.doge_issue_derivation.v1",
    )


def test_ssr15_civic_unbound_lists_on_node_issues(client: TestClient) -> None:
    _save_civic_projection("ssr15-civic-unbound")
    response = client.get("/node/issues")
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert any(row["id"] == "ssr15-civic-unbound" for row in issues)
    civic = next(row for row in issues if row["id"] == "ssr15-civic-unbound")
    assert "structured_payload" not in civic


def test_ssr15_pack_bound_card_on_same_node_issues(client: TestClient) -> None:
    orchestrator = get_api_dependencies().story_cluster_orchestrator
    for sid in ("ssr15-p1", "ssr15-p2", "ssr15-p3"):
        orchestrator.story_repository.save_story(
            _pack_story(sid, office_id="ssr15-station")
        )
    created = orchestrator.process_all_pending()
    assert created
    response = client.get("/node/issues")
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert issues
    assert all("structured_payload" not in row for row in issues)


def test_ssr15_pulse_and_emerging_are_not_issues(client: TestClient) -> None:
    pulse = client.get("/node/network-pulse")
    emerging = client.get("/node/emerging-signals")
    issues = client.get("/node/issues")
    assert pulse.status_code == 200
    assert emerging.status_code == 200
    assert issues.status_code == 200
    assert "issues" not in pulse.json()["data"]
    assert "signals" in emerging.json()["data"]
    assert "issues" in issues.json()["data"]
    assert "signals" not in issues.json()["data"]


def test_ssr15_legacy_tallinn_issues_is_404(client: TestClient) -> None:
    response = client.get("/tallinn/issues")
    assert response.status_code == 404
    assert response.status_code not in {200, 301, 302}


def test_ssr15_dual_membership_and_same_public_path(
    client: TestClient, tmp_path: Path
) -> None:
    packs = _write_dual_legal_root(tmp_path)
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_dual_bound_story("ssr15-d1"))
    orchestrator = _dual_orchestrator(stories, store, packs)
    orchestrator.process_story("ssr15-d1")
    lenses = _lenses_for(store, "ssr15-d1")
    assert ClusterLens.CIVIC_DOMAIN_MICRO.value in lenses
    assert "police_station" in lenses
    _save_civic_projection("ssr15-dual-public")
    response = client.get("/node/issues")
    assert response.status_code == 200
    assert any(
        row["id"] == "ssr15-dual-public" for row in response.json()["data"]["issues"]
    )
