"""STORY-GW-RC-03 acceptance: contract guarantee on read for incomplete legacy payload."""

from __future__ import annotations
from tests.civic_pack_overrides import monkeypatch_civic_knobs

from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.projection.enums import DOGEIssueStatus
from tests.req39_contract_helpers import PolicyVersion, sqlite_store_factory

Backend = Literal["memory", "sqlite"]

_CONTRACT_KEYS = ("id", "status", "type", "labels", "title", "summary", "description")
_VALID_STATUSES = frozenset(status.value for status in DOGEIssueStatus)


def _incomplete_legacy_payload() -> dict[str, object]:
    """No id/status in payload; lowercase type (live legacy shape)."""
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
    store = sqlite_store_factory(tmp_path / f"gw-rc-03-{backend}.sqlite")
    yield store
    store.db.connection.close()


def test_store_contract_guarantee_incomplete_legacy_payload(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="gw-rc-03-contract",
        status="PUBLISHED",
        payload=_incomplete_legacy_payload(),
        policy_version=PolicyVersion,
    )
    for issue in (
        next(item for item in projection_store.list_projections() if item["id"] == "gw-rc-03-contract"),
        projection_store.get_projection("gw-rc-03-contract"),
    ):
        assert issue is not None
        assert issue["id"] == "gw-rc-03-contract"
        assert issue["status"] == "PUBLISHED"
        assert issue["status"] in _VALID_STATUSES
        assert issue["type"] == "IMPROVEMENT"
        assert "created_at" in issue
        for key in _CONTRACT_KEYS:
            assert key in issue


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=int("1"), readiness_threshold=int("1"))
    monkeypatch.setenv("SERVICE_API_TOKEN", "gw-rc-03-test-token")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_http_list_get_contract_guarantee_incomplete_legacy_payload(
    client: TestClient,
) -> None:
    store = get_api_dependencies().issue_projection_read_store
    store.save_projection(
        issue_id="gw-rc-03-http-contract",
        status="PUBLISHED",
        payload=_incomplete_legacy_payload(),
        policy_version=PolicyVersion,
    )

    list_response = client.get("/node/issues")
    assert list_response.status_code == 200
    issue = next(
        item
        for item in list_response.json()["data"]["issues"]
        if item["id"] == "gw-rc-03-http-contract"
    )
    assert issue["status"] == "PUBLISHED"
    assert issue["type"] == "IMPROVEMENT"
    assert "created_at" in issue
    for key in _CONTRACT_KEYS:
        assert key in issue

    get_response = client.get("/node/issues/gw-rc-03-http-contract")
    assert get_response.status_code == 200
    fetched = get_response.json()["data"]["issue"]
    assert fetched["id"] == "gw-rc-03-http-contract"
    assert fetched["status"] == "PUBLISHED"
    assert fetched["type"] == "IMPROVEMENT"
    for key in _CONTRACT_KEYS:
        assert key in fetched
