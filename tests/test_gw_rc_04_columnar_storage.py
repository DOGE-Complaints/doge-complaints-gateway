"""STORY-GW-RC-04 T11: columnar storage round-trip and legacy fallback tests."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Literal

import pytest

from core.infrastructure.db_sqlite import SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.projection.columnar_storage import assemble_public_issue_from_storage_row
from tests.req39_contract_helpers import PolicyVersion, sqlite_store_factory

Backend = Literal["memory", "sqlite"]

_CONTRACT_KEYS = (
    "id",
    "status",
    "type",
    "labels",
    "title",
    "summary",
    "description",
    "institution",
    "geo",
    "original_locale",
    "arweave_txid",
    "image_txid",
    "image_hash",
)


def _full_columnar_payload() -> dict[str, object]:
    return {
        "type": "INCIDENT",
        "labels": ["infra", "roads"],
        "title": {"en": "Title", "et": "Pealkiri", "ru": "Заголовок"},
        "summary": {"en": "Summary", "et": "Kokkuvõte"},
        "description": {"en": "Description line"},
        "institution": {"en": "Tallinn City"},
        "geo": {"district": "põhjatallinn", "lat": 59.44, "lon": 24.75, "country": "EE"},
        "original_locale": ["et", "en"],
        "arweave_txid": "tx-abc",
        "image_txid": "img-tx",
        "image_hash": "hash123",
    }


@pytest.fixture(params=["memory", "sqlite"])
def projection_store(
    request: pytest.FixtureRequest, tmp_path: Path
) -> Iterator[InMemoryIssueProjectionStore | SqliteIssueProjectionStore]:
    backend: Backend = request.param
    if backend == "memory":
        yield InMemoryIssueProjectionStore()
        return
    store = sqlite_store_factory(tmp_path / f"gw-rc-04-{backend}.sqlite")
    yield store
    store.db.connection.close()


def test_columnar_round_trip_save_and_get_full_contract(
    projection_store: InMemoryIssueProjectionStore | SqliteIssueProjectionStore,
) -> None:
    payload = _full_columnar_payload()
    projection_store.save_projection(
        issue_id="gw-rc-04-roundtrip",
        status="PUBLISHED",
        payload=payload,
        policy_version=PolicyVersion,
    )
    for issue in (
        projection_store.get_projection("gw-rc-04-roundtrip"),
        next(
            item
            for item in projection_store.list_projections()
            if item["id"] == "gw-rc-04-roundtrip"
        ),
    ):
        assert issue is not None
        assert issue["id"] == "gw-rc-04-roundtrip"
        assert issue["status"] == "PUBLISHED"
        assert issue["type"] == "INCIDENT"
        for key in _CONTRACT_KEYS:
            assert key in issue
        assert issue["labels"] == ["infra", "roads"]
        assert issue["title"]["en"] == "Title"
        assert issue["geo"] == payload["geo"]
        assert issue["original_locale"] == ["et", "en"]
        assert issue["arweave_txid"] == "tx-abc"


def test_legacy_payload_json_fallback_when_columnar_row_empty() -> None:
    """Simulates pre-migration row: empty columnar fields, body only in legacy blob."""
    row = {
        "issue_id": "legacy-fallback-1",
        "status": "PUBLISHED",
        "created_at": "2026-01-01T00:00:00+00:00",
        "issue_type": None,
        "labels_json": "[]",
        "title_json": "{}",
        "summary_json": "{}",
        "description_json": "{}",
        "institution_json": None,
        "geo_json": None,
        "original_locale_json": "[]",
        "arweave_txid": None,
        "image_txid": None,
        "image_hash": None,
    }
    legacy_payload = {
        "type": "improvement",
        "labels": ["legacy"],
        "title": {"en": "Legacy title"},
        "summary": {"en": "Legacy summary"},
        "description": {"en": "Legacy description"},
        "geo": {"country": "EE"},
    }
    issue = assemble_public_issue_from_storage_row(
        row,
        legacy_payload_json=legacy_payload,
    )
    assert issue["id"] == "legacy-fallback-1"
    assert issue["status"] == "PUBLISHED"
    assert issue["type"] == "IMPROVEMENT"
    assert issue["labels"] == ["legacy"]
    assert issue["title"]["en"] == "Legacy title"
    geo = issue.get("geo")
    assert isinstance(geo, dict)
    assert geo.get("country") == "EE"
