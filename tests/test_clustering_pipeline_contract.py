"""REQ-39 Zone J: clustering pipeline stitch (orchestrator → doge_issues)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from tests.intake_v2_fixtures import intake_payload_simple


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _projection_store():
    store = get_api_dependencies().issue_create_service.issue_projection_store
    assert store is not None
    return store


def _intake_story(client: TestClient, *, suffix: str) -> None:
    payload = intake_payload_simple(
        external_user_id=f"req39-j-user-{suffix}",
        original_text=f"Broken pavement contract test {suffix} Kalamaja district",
        title_en=f"J test {suffix}",
    )
    payload["narrative"]["location_query"] = "Kalamaja, Tallinn"
    response = client.post("/intake/stories", json=payload)
    assert response.status_code == 202, response.text


def test_j01_cluster_below_min_size_does_not_create_issue(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "3")
    _clear_api_dependencies_cache()
    _intake_story(client, suffix="a")
    _intake_story(client, suffix="b")
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    assert _projection_store().list_projections() == []


def test_j02_cluster_at_min_size_creates_issue(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    _clear_api_dependencies_cache()
    _intake_story(client, suffix="single")
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    assert len(_projection_store().list_projections()) >= 1


def test_j03_new_issue_has_m3_policy_version(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'j03.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    _intake_story(client, suffix="policy")
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()
    store = _projection_store()
    assert isinstance(store, SqliteIssueProjectionStore)
    cursor = store.db.connection.execute(
        "SELECT policy_version FROM doge_issues"
    )
    versions = [str(row[0]) for row in cursor.fetchall()]
    assert versions
    assert all(v == "m3.doge_issue_derivation.v1" for v in versions)


def test_j04_clustering_idempotent_no_duplicate_issues(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    _clear_api_dependencies_cache()
    _intake_story(client, suffix="idem-1")
    orchestrator = get_api_dependencies().story_cluster_orchestrator
    orchestrator.process_all_pending()
    first_ids = [str(item["id"]) for item in _projection_store().list_projections()]
    orchestrator.process_all_pending()
    second_ids = [str(item["id"]) for item in _projection_store().list_projections()]
    assert first_ids
    assert len(second_ids) == len(set(second_ids))
