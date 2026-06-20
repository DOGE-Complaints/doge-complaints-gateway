"""STORY-GW-RC-05 acceptance: canonical issue status on read path."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest

from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.projection.enums import DOGEIssueStatus
from core.projection.read_filters import canonicalize_status_on_read
from core.projection.read_status_telemetry import reset_unknown_issue_status_log_state
from tests.req39_contract_helpers import PolicyVersion, sqlite_store_factory

Backend = Literal["memory", "sqlite"]

_VALID_STATUSES = frozenset(status.value for status in DOGEIssueStatus)


def _sample_payload() -> dict[str, object]:
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
    store = sqlite_store_factory(tmp_path / f"gw-rc-05-{backend}.sqlite")
    yield store
    store.db.connection.close()


def test_canonicalize_status_promoted_alias() -> None:
    assert canonicalize_status_on_read("promoted", log_unknown=False) == "PUBLISHED"
    assert canonicalize_status_on_read("PROMOTED", log_unknown=False) == "PUBLISHED"


def test_canonicalize_status_board_vocab_passthrough() -> None:
    for value in _VALID_STATUSES:
        assert canonicalize_status_on_read(value, log_unknown=False) == value


def test_canonicalize_status_unknown_defaults_to_published() -> None:
    reset_unknown_issue_status_log_state()
    assert canonicalize_status_on_read("archived", log_unknown=False) == "PUBLISHED"


def test_store_get_list_canonicalizes_legacy_promoted_status(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="gw-rc-05-legacy-status",
        status="promoted",
        payload=_sample_payload(),
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections()
    issue = next(item for item in listed if item["id"] == "gw-rc-05-legacy-status")
    assert issue["status"] == "PUBLISHED"
    assert issue["status"] in _VALID_STATUSES

    fetched = projection_store.get_projection("gw-rc-05-legacy-status")
    assert fetched is not None
    assert fetched["status"] == "PUBLISHED"


def test_store_status_filter_matches_legacy_promoted_row(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    projection_store.save_projection(
        issue_id="legacy-promoted-filter",
        status="promoted",
        payload=_sample_payload(),
        policy_version=PolicyVersion,
    )
    projection_store.save_projection(
        issue_id="published-row",
        status="PUBLISHED",
        payload=_sample_payload(),
        policy_version=PolicyVersion,
    )
    listed = projection_store.list_projections(status=["PUBLISHED"])
    ids = {str(item["id"]) for item in listed}
    assert ids == {"legacy-promoted-filter", "published-row"}
