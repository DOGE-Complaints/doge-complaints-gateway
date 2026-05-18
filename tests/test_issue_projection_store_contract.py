"""REQ-39 Zone L: IssueProjectionReadStore protocol contract (InMemory + SQLite)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest

from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from tests.req39_contract_helpers import (
    PolicyVersion,
    inmemory_store_factory,
    projection_payload,
    sqlite_store_factory,
)

Backend = Literal["memory", "sqlite"]


@pytest.fixture(params=["memory", "sqlite"])
def projection_store(
    request: pytest.FixtureRequest, tmp_path: Path
) -> Iterator[InMemoryIssueProjectionStore | SqliteIssueProjectionStore]:
    backend: Backend = request.param
    if backend == "memory":
        yield inmemory_store_factory()
        return
    db_path = tmp_path / f"zone-l-{backend}.sqlite"
    store = sqlite_store_factory(db_path)
    yield store
    store.db.connection.close()


def test_l01_save_get_roundtrip(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    payload = projection_payload(
        "test-001",
        geo={"district": "põhja-tallinn", "lat": 59.44, "lon": 24.75},
    )
    projection_store.save_projection(
        issue_id="test-001",
        status="PUBLISHED",
        payload=payload,
        policy_version=PolicyVersion,
    )
    result = projection_store.get_projection("test-001")
    assert result is not None
    assert result["id"] == "test-001"
    assert result["status"] == "PUBLISHED"
    geo = result.get("geo")
    assert isinstance(geo, dict)
    assert geo.get("district") == "põhja-tallinn"


def test_l02_list_by_status_excludes_other_statuses(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="pub-1",
        status="PUBLISHED",
        payload=projection_payload("pub-1", status="PUBLISHED"),
        policy_version=PolicyVersion,
    )
    projection_store.save_projection(
        issue_id="draft-1",
        status="DRAFT",
        payload=projection_payload("draft-1", status="DRAFT"),
        policy_version=PolicyVersion,
    )
    result = projection_store.list_projections(status=["PUBLISHED"])
    ids = {str(item["id"]) for item in result}
    assert "pub-1" in ids
    assert "draft-1" not in ids


def test_l03_list_no_filters_returns_all(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    for index in range(3):
        issue_id = f"id-{index}"
        projection_store.save_projection(
            issue_id=issue_id,
            status="PUBLISHED",
            payload=projection_payload(issue_id),
            policy_version=PolicyVersion,
        )
    result = projection_store.list_projections()
    assert len(result) == 3


def test_l04_get_nonexistent_returns_none(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    assert projection_store.get_projection("nonexistent-id") is None
