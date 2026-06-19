"""STORY-GW-RC-01 acceptance: column-as-truth merge on read path."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Literal

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from tests.req39_contract_helpers import PolicyVersion, sqlite_store_factory

Backend = Literal["memory", "sqlite"]


def _incomplete_payload() -> dict[str, object]:
    return {
        "type": "IMPROVEMENT",
        "labels": ["infra"],
        "title": {"et": "t", "ru": "t", "en": "t"},
        "summary": {"et": "s", "ru": "s", "en": "s"},
        "description": {"et": "d", "ru": "d", "en": "d"},
    }


@pytest.fixture(params=["memory", "sqlite"])
def projection_store(
    request: pytest.FixtureRequest, tmp_path: Path
) -> Iterator[InMemoryIssueProjectionStore | SqliteIssueProjectionStore]:
    backend: Backend = request.param
    if backend == "memory":
        yield InMemoryIssueProjectionStore()
        return
    store = sqlite_store_factory(tmp_path / f"gw-rc-01-{backend}.sqlite")
    yield store
    store.db.connection.close()


def test_store_get_list_merge_incomplete_payload(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="gw-rc-incomplete",
        status="PUBLISHED",
        payload=_incomplete_payload(),
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections()
    assert len(listed) == 1
    issue = listed[0]
    assert issue["id"] == "gw-rc-incomplete"
    assert issue["status"] == "PUBLISHED"
    assert "created_at" in issue

    fetched = projection_store.get_projection("gw-rc-incomplete")
    assert fetched is not None
    assert fetched["id"] == "gw-rc-incomplete"
    assert fetched["status"] == "PUBLISHED"
    assert "created_at" in fetched


def test_store_status_filter_uses_column_not_payload(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="col-published",
        status="PUBLISHED",
        payload={**_incomplete_payload(), "status": "DRAFT"},
        policy_version=PolicyVersion,
    )
    projection_store.save_projection(
        issue_id="col-draft",
        status="DRAFT",
        payload={**_incomplete_payload(), "status": "PUBLISHED"},
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections(status=["PUBLISHED"])
    ids = {str(item["id"]) for item in listed}
    assert ids == {"col-published"}


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch.setenv("SERVICE_API_TOKEN", "gw-rc-01-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_http_list_get_merge_incomplete_payload(client: TestClient) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="gw-rc-http-incomplete",
        status="PUBLISHED",
        payload=_incomplete_payload(),
        policy_version=PolicyVersion,
    )

    list_response = client.get("/tallinn/issues")
    assert list_response.status_code == 200
    issues = list_response.json()["data"]["issues"]
    match = next(item for item in issues if item["id"] == "gw-rc-http-incomplete")
    assert match["status"] == "PUBLISHED"
    assert "created_at" in match

    get_response = client.get("/tallinn/issues/gw-rc-http-incomplete")
    assert get_response.status_code == 200
    issue = get_response.json()["data"]["issue"]
    assert issue["id"] == "gw-rc-http-incomplete"
    assert issue["status"] == "PUBLISHED"
    assert "created_at" in issue


def test_http_status_filter_uses_column_not_payload(client: TestClient) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="http-col-published",
        status="PUBLISHED",
        payload={**_incomplete_payload(), "status": "DRAFT"},
        policy_version=PolicyVersion,
    )
    store.save_projection(
        issue_id="http-col-draft",
        status="DRAFT",
        payload={**_incomplete_payload(), "status": "PUBLISHED"},
        policy_version=PolicyVersion,
    )

    response = client.get("/tallinn/issues", params={"status": "PUBLISHED"})
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert "http-col-published" in ids
    assert "http-col-draft" not in ids


def test_store_created_at_fallback_from_updated_at_when_column_missing() -> None:
    store = InMemoryIssueProjectionStore()
    store.save_projection(
        issue_id="no-created-at-col",
        status="PUBLISHED",
        payload=_incomplete_payload(),
        policy_version=PolicyVersion,
    )
    assert store._rows is not None
    row = store._rows["no-created-at-col"]
    updated_at = row["updated_at"]
    assert isinstance(updated_at, datetime)
    del row["created_at"]

    listed = store.list_projections()
    issue = next(item for item in listed if item["id"] == "no-created-at-col")
    assert issue["created_at"] == updated_at.isoformat()

    fetched = store.get_projection("no-created-at-col")
    assert fetched is not None
    assert fetched["created_at"] == updated_at.isoformat()
