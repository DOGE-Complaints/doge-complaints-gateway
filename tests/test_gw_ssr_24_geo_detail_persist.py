"""GW-SSR-24: persist StoryGeoSnapshot address depth + omit-probe + lifecycle."""

from __future__ import annotations

import inspect
from pathlib import Path

from core.application import StoryIntakeService
from core.cluster.types import ClusterLens
from core.domain import StoryGeoSnapshot, StoryLifecycleStatus
from core.geo.intake_merge import merge_client_geo_detail, mirror_geo_to_payload
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure.db_supabase import (
    _STORY_SELECT_FIELDS,
    _story_select_fields_for_db,
    SupabaseDatabase,
)
from core.infrastructure.repositories import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake.contracts import GeoDetail, GeoDetailAddress
from tests.intake_v2_fixtures import make_story_record

_MIGRATION = Path("supabase/migrations/20260830_2100_gw_ssr_24_stories_geo_detail.sql")
_DETAIL_COLS = frozenset(SupabaseDatabase._STORIES_GEO_DETAIL_COLUMNS)


def test_clusterlens_still_ten_members() -> None:
    assert len(ClusterLens) == 10


def test_migration_sql_on_disk() -> None:
    text = _MIGRATION.read_text(encoding="utf-8")
    for col in _DETAIL_COLS:
        assert col in text


def _snapshot(**overrides: object) -> StoryGeoSnapshot:
    base = dict(
        normalized_label="Pikk 12, Tallinn",
        latitude=59.437,
        longitude=24.7536,
        confidence=0.9,
        provider="client",
        admin_district="kesklinn",
        admin_settlement="tallinn",
        admin_region="harju maakond",
        admin_country="EE",
        street="Pikk",
        house="12",
        address_line="Pikk, 12",
    )
    base.update(overrides)
    return StoryGeoSnapshot(**base)  # type: ignore[arg-type]


def test_sqlite_roundtrip_street_house_coords() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    record = make_story_record(story_id="ssr24-street", geo=_snapshot())
    repo.save_story(record)
    loaded = repo.get_story(record.story_id)
    assert loaded is not None and loaded.geo is not None
    assert loaded.geo.street == "Pikk"
    assert loaded.geo.house == "12"
    assert loaded.geo.latitude == 59.437
    assert loaded.geo.admin_district == "kesklinn"


def test_sqlite_roundtrip_house_range() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    geo = _snapshot(house=None, house_range="10-14", address_line="Pikk, 10-14")
    record = make_story_record(story_id="ssr24-range", geo=geo)
    repo.save_story(record)
    loaded = repo.get_story(record.story_id)
    assert loaded is not None and loaded.geo is not None
    assert loaded.geo.house_range == "10-14"
    assert loaded.geo.house is None


def test_sqlite_roundtrip_houses() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    geo = _snapshot(house=None, houses=("3", "5", "7"), address_line="Pikk, 3, 5, 7")
    record = make_story_record(story_id="ssr24-houses", geo=geo)
    repo.save_story(record)
    loaded = repo.get_story(record.story_id)
    assert loaded is not None and loaded.geo is not None
    assert loaded.geo.houses == ("3", "5", "7")


def test_advance_preserves_geo_depth() -> None:
    repo = InMemoryStoryRepository()
    service = StoryIntakeService(
        repository=repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    accepted = make_story_record(
        story_id="ssr24-advance",
        lifecycle_status=StoryLifecycleStatus.ACCEPTED,
        geo=_snapshot(),
    )
    repo.save_story(accepted)
    advanced = service.advance_story_readiness(
        story_id="ssr24-advance", narrative_complete=True
    )
    assert advanced.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
    assert advanced.geo is not None
    assert advanced.geo.street == "Pikk"
    assert advanced.geo.house == "12"
    assert advanced.geo.houses == ()


def test_required_columns_ready_omits_geo_detail() -> None:
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for col in _DETAIL_COLS:
        assert col not in source


def test_omit_probe_cuts_geo_detail_when_false() -> None:
    class _Probe:
        def stories_geo_admin_columns_ready(self) -> bool:
            return True

        def stories_binding_columns_ready(self) -> bool:
            return True

        def stories_geo_detail_columns_ready(self) -> bool:
            return False

    omitted = _story_select_fields_for_db(_Probe())  # type: ignore[arg-type]
    parts = {part.strip() for part in omitted.split(",") if part.strip()}
    assert _DETAIL_COLS.isdisjoint(parts)
    ready = _STORY_SELECT_FIELDS
    for col in _DETAIL_COLS:
        assert col in ready


def test_merge_writes_street_on_snapshot() -> None:
    provider = StoryGeoSnapshot(
        normalized_label="Tallinn, EE",
        latitude=59.437,
        longitude=24.7536,
        confidence=0.8,
        provider="stub",
        admin_settlement="tallinn",
        admin_country="EE",
    )
    detail = GeoDetail(address=GeoDetailAddress(street="Pikk", house="12"))
    merged = merge_client_geo_detail(provider, detail, merge=True)
    assert merged is not None
    assert merged.street == "Pikk"
    assert merged.house == "12"
    assert merged.address_line == "Pikk, 12"


def test_mirror_payload_from_snapshot_depth() -> None:
    payload: dict[str, object] = {}
    geo = _snapshot()
    mirror_geo_to_payload(payload, geo=geo, detail=None)
    assert payload["geo"]["street"] == "Pikk"
    assert payload["geo"]["house"] == "12"
