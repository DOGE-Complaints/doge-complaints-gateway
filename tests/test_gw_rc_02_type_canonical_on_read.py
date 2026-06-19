"""STORY-GW-RC-02 acceptance: canonical issue type on read path."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.projection.read_type_telemetry import reset_unknown_issue_type_log_state
from tests.req39_contract_helpers import PolicyVersion, sqlite_store_factory

Backend = Literal["memory", "sqlite"]


def _legacy_lowercase_payload() -> dict[str, object]:
    return {
        "type": "improvement",
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
    store = sqlite_store_factory(tmp_path / f"gw-rc-02-{backend}.sqlite")
    yield store
    store.db.connection.close()


def test_store_get_list_canonicalizes_legacy_lowercase_type(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="gw-rc-02-legacy-type",
        status="PUBLISHED",
        payload=_legacy_lowercase_payload(),
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections()
    issue = next(item for item in listed if item["id"] == "gw-rc-02-legacy-type")
    assert issue["type"] == "IMPROVEMENT"

    fetched = projection_store.get_projection("gw-rc-02-legacy-type")
    assert fetched is not None
    assert fetched["type"] == "IMPROVEMENT"


def test_store_type_filter_matches_legacy_lowercase_payload(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="legacy-type-filter",
        status="PUBLISHED",
        payload=_legacy_lowercase_payload(),
        policy_version=PolicyVersion,
    )
    projection_store.save_projection(
        issue_id="incident-type",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "incident"},
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections(issue_type="IMPROVEMENT")
    ids = {str(item["id"]) for item in listed}
    assert ids == {"legacy-type-filter"}


def test_store_unknown_type_defaults_to_improvement(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="unknown-type",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "custom_anomaly"},
        policy_version=PolicyVersion,
    )
    fetched = projection_store.get_projection("unknown-type")
    assert fetched is not None
    assert fetched["type"] == "IMPROVEMENT"


def test_unknown_type_anomaly_file_log_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    reset_unknown_issue_type_log_state()
    monkeypatch.setenv("LOG_DEBUG_DIR", str(tmp_path))
    store = InMemoryIssueProjectionStore()
    store.save_projection(
        issue_id="unknown-a",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "custom_anomaly"},
        policy_version=PolicyVersion,
    )
    store.get_projection("unknown-a")
    store.save_projection(
        issue_id="unknown-b",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "custom_anomaly"},
        policy_version=PolicyVersion,
    )
    store.get_projection("unknown-b")

    log_path = tmp_path / "unknown_issue_types.jsonl"
    assert log_path.is_file()
    lines = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == 1
    assert lines[0]["raw_type"] == "custom_anomaly"
    assert lines[0]["normalized_to"] == "IMPROVEMENT"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch.setenv("SERVICE_API_TOKEN", "gw-rc-02-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_http_list_get_canonicalizes_legacy_lowercase_type(client: TestClient) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="gw-rc-02-http-legacy",
        status="PUBLISHED",
        payload=_legacy_lowercase_payload(),
        policy_version=PolicyVersion,
    )

    list_response = client.get("/tallinn/issues")
    assert list_response.status_code == 200
    issues = list_response.json()["data"]["issues"]
    match = next(item for item in issues if item["id"] == "gw-rc-02-http-legacy")
    assert match["type"] == "IMPROVEMENT"

    get_response = client.get("/tallinn/issues/gw-rc-02-http-legacy")
    assert get_response.status_code == 200
    issue = get_response.json()["data"]["issue"]
    assert issue["type"] == "IMPROVEMENT"


def test_http_type_filter_matches_legacy_lowercase_payload(client: TestClient) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="http-legacy-type",
        status="PUBLISHED",
        payload=_legacy_lowercase_payload(),
        policy_version=PolicyVersion,
    )
    store.save_projection(
        issue_id="http-incident-type",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "incident"},
        policy_version=PolicyVersion,
    )

    response = client.get("/tallinn/issues", params={"type": "IMPROVEMENT"})
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert "http-legacy-type" in ids
    assert "http-incident-type" not in ids


def test_http_type_filter_accepts_lowercase_query_param(client: TestClient) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="http-legacy-query",
        status="PUBLISHED",
        payload=_legacy_lowercase_payload(),
        policy_version=PolicyVersion,
    )
    store.save_projection(
        issue_id="http-incident-query",
        status="PUBLISHED",
        payload={**_legacy_lowercase_payload(), "type": "incident"},
        policy_version=PolicyVersion,
    )

    response = client.get("/tallinn/issues", params={"type": "improvement"})
    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["data"]["issues"]}
    assert "http-legacy-query" in ids
    assert "http-incident-query" not in ids
