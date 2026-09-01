"""GW-SSR-27: geo precision index + GPT instance territory pack contract."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.cluster.types import ClusterLens
from core.domain import StoryGeoSnapshot
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.intake import IntakeValidationError
from core.intake.contracts import _parse_geo_detail_block, geo_detail_has_values
from core.projection.extraction_policy import build_projection_input_from_draft
from core.projection.i18n import I18nText
from core.projection.input import ProjectionInput
from core.projection.mapper import project_distinct_issue
from core.schema import SchemaRef, UnsupportedVersionError
from core.schema.contracts import GEO_PRECISION_LEVELS, GPT_INSTANCE_RULE_TYPES
from core.schema.resolver import resolve_pack
from tests.intake_v2_fixtures import make_story_record

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"
_MIGRATION = Path("supabase/migrations/20260901_1315_gw_ssr_27_stories_geo_detail_level.sql")


def test_clusterlens_baseline_unchanged() -> None:
    assert len(ClusterLens) == 10
    assert "admin_id" in GPT_INSTANCE_RULE_TYPES
    assert "admin_token" in GPT_INSTANCE_RULE_TYPES
    assert "bbox" in GPT_INSTANCE_RULE_TYPES
    assert "region" in GEO_PRECISION_LEVELS


def test_legal_and_mobility_absent_geo_blocks() -> None:
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    mobility = resolve_pack(
        SchemaRef("mobility_observation", "v1"), packs_root=PACKS_ROOT
    )
    assert legal.geo_model is None
    assert legal.gpt_instance_territory is None
    assert mobility.geo_model is None
    assert mobility.gpt_instance_territory is None


def test_tallinn_loader_geo_blocks() -> None:
    tallinn = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert tallinn.geo_model is not None
    assert set(tallinn.geo_model.precision_levels) == set(GEO_PRECISION_LEVELS)
    assert tallinn.geo_model.default_precision_inference == "from_address_depth"
    assert tallinn.gpt_instance_territory is not None
    assert tallinn.gpt_instance_territory.enabled is True
    assert len(tallinn.gpt_instance_territory.rules) == 1
    rule = tallinn.gpt_instance_territory.rules[0]
    assert rule.type == "admin_token"
    assert rule.level == "settlement"
    assert rule.value == "tallinn"


def test_invalid_geo_model_level_fails(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    manifest["geo_model"] = {
        "precision_levels": ["region", "not_a_level"],
    }
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="unknown geo_model precision level"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_parse_geo_detail_detail_level_valid_and_invalid() -> None:
    ok = _parse_geo_detail_block({"detail_level": "region"})
    assert ok.detail_level == "region"
    assert geo_detail_has_values(ok) is True
    with pytest.raises(IntakeValidationError, match="detail_level"):
        _parse_geo_detail_block({"detail_level": "planet"})


def test_sqlite_roundtrip_detail_level() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    repo = SqliteStoryRepository(db)
    geo = StoryGeoSnapshot(
        normalized_label="Tallinn",
        latitude=59.437,
        longitude=24.7536,
        confidence=0.9,
        provider="client",
        admin_settlement="tallinn",
        detail_level="settlement",
    )
    record = make_story_record(story_id="ssr27-level", geo=geo)
    repo.save_story(record)
    loaded = repo.get_story(record.story_id)
    assert loaded is not None and loaded.geo is not None
    assert loaded.geo.detail_level == "settlement"


def test_projection_detail_level_without_coords() -> None:
    data = ProjectionInput(
        issue_id="iss-region",
        status="PUBLISHED",
        issue_type="IMPROVEMENT",
        labels=("waste",),
        title=I18nText(et="t", ru="t", en="t"),
        summary=None,
        description=I18nText(et="d", ru="d", en="d"),
        geo_admin_region="harju",
        geo_detail_level="region",
    )
    issue = project_distinct_issue(data)
    assert issue.geo is not None
    assert "lat" not in issue.geo
    assert "lon" not in issue.geo
    assert issue.geo["detail_level"] == "region"
    assert issue.geo["region"] == "harju"
    assert "street" not in issue.geo
    assert "house" not in issue.geo


def test_build_projection_input_propagates_detail_level() -> None:
    from core.projection.extraction_policy import StoryProjectionDraft

    draft = StoryProjectionDraft(
        issue_type="IMPROVEMENT",
        labels=("waste",),
        title=I18nText(et="t", ru="t", en="t"),
        summary=I18nText(et="s", ru="s", en="s"),
        description=I18nText(et="d", ru="d", en="d"),
        policy_version="test",
    )
    geo = StoryGeoSnapshot(
        normalized_label="x",
        latitude=1.0,
        longitude=2.0,
        confidence=1.0,
        provider="client",
        detail_level="house",
    )
    pin = build_projection_input_from_draft(
        issue_id="iss-house",
        draft=draft,
        geo_snapshot=geo,
    )
    assert pin.geo_detail_level == "house"
    issue = project_distinct_issue(pin)
    assert issue.geo is not None
    assert issue.geo["detail_level"] == "house"
    assert issue.geo["lat"] == 1.0


def test_payload_schema_has_detail_level() -> None:
    schema = json.loads(
        (PACKS_ROOT / "tallinn_civic" / "v1" / "payload.schema.json").read_text(
            encoding="utf-8"
        )
    )
    detail = schema["properties"]["geo"]["properties"]["detail_level"]
    assert detail["type"] == "string"
    assert set(detail["enum"]) == set(GEO_PRECISION_LEVELS)


def test_migration_sql_on_disk() -> None:
    text = _MIGRATION.read_text(encoding="utf-8")
    assert "geo_detail_level" in text
    # SSR-24 columns stay out of this migration file.
    assert "geo_street" not in text
