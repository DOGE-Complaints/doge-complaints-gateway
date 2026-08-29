"""GW-SSR-08 T03: tallinn_civic pack load + exact membership from payload."""

from __future__ import annotations

from pathlib import Path

from core.domain import StoryLifecycleStatus
from core.schema import (
    LocalSchemaRuntime,
    SchemaPackClusterEngine,
    SchemaRef,
    pack_cluster_id,
    promotion_gate_policy_from_pack,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

ENVELOPE_SIGNALS = {
    "civic_domain": "transport",
    "failure_pattern": "broken_infrastructure",
    "civic_weight": "recurring_issue",
    "desired_outcome": "better_maintenance",
    "affected_group": "residents",
    "service_object": "tram_line",
    "need": "unknown",
    "ecosystem_signal": "unknown",
    "canonical_type": "complaint",
}


def _runtime() -> LocalSchemaRuntime:
    return LocalSchemaRuntime(packs_root=PACKS_ROOT)


def _engine() -> SchemaPackClusterEngine:
    return SchemaPackClusterEngine(_runtime())


def _payload(*, include_geo: bool = True) -> dict:
    out: dict = {"signals": dict(ENVELOPE_SIGNALS)}
    if include_geo:
        out["geo"] = {"district": "kesklinn"}
    return out


def _pack_story(story_id: str, payload: dict | None = None) -> object:
    return make_story_record(
        story_id=story_id,
        narrative_original_text="Pothole on the tram line.",
        submitter_external_user_id=f"user-{story_id}",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="Tram pothole"),
        narrative_description=narrative_dict(en="Recurring pothole on the tram line."),
        schema_id="tallinn_civic",
        bound_schema_version="v1",
        structured_payload=payload if payload is not None else _payload(),
    )


def test_tallinn_civic_pack_resolves() -> None:
    ctx = _runtime().resolve(SchemaRef("tallinn_civic", "v1"))
    assert ctx.ref.schema_id == "tallinn_civic"
    assert ctx.ref.schema_version == "v1"
    lens_ids = {lens.lens_id for lens in ctx.exact_lenses}
    assert "civic_domain_micro" in lens_ids
    assert "composite_primary_micro" in lens_ids
    composite = next(lens for lens in ctx.exact_lenses if lens.lens_id == "composite_primary_micro")
    assert composite.source_fields == ("signals.civic_domain", "signals.failure_pattern")


def test_json_schema_covers_map_dotted_paths() -> None:
    ctx = _runtime().resolve(SchemaRef("tallinn_civic", "v1"))
    signals = ctx.payload_schema["properties"]["signals"]["properties"]
    for key in (
        "civic_domain",
        "failure_pattern",
        "civic_weight",
        "desired_outcome",
        "affected_group",
        "service_object",
        "need",
        "ecosystem_signal",
        "canonical_type",
    ):
        assert key in signals
    assert "district" in ctx.payload_schema["properties"]["geo"]["properties"]
    _runtime().validate(ctx, _payload())


def test_readiness_knobs_come_from_pack_file_not_civic_defaults() -> None:
    ctx = _runtime().resolve(SchemaRef("tallinn_civic", "v1"))
    policy = ctx.exact_lenses[0].readiness_policy
    assert policy.min_readiness_score == 35
    assert policy.min_stories == 3
    assert policy.require_actionable_canonical_type is False
    mapped = promotion_gate_policy_from_pack(policy)
    assert mapped.min_readiness_score == 35
    assert mapped.min_stories == 3
    assert mapped.require_actionable_canonical_type is False


def test_two_stories_same_payload_share_cluster_id() -> None:
    engine = _engine()
    a = _pack_story("tc-a")
    b = _pack_story("tc-b")
    ma = {m.lens: m for m in engine.memberships_for_story(a)}
    mb = {m.lens: m for m in engine.memberships_for_story(b)}
    assert ma["civic_domain_micro"].cluster_id == mb["civic_domain_micro"].cluster_id
    assert ma["civic_domain_micro"].cluster_id == pack_cluster_id(
        schema_id="tallinn_civic",
        lens_id="civic_domain_micro",
        field_tokens=("transport",),
    )
    assert ma["civic_domain_micro"].lens == "civic_domain_micro"
    assert ma["composite_primary_micro"].cluster_id == pack_cluster_id(
        schema_id="tallinn_civic",
        lens_id="composite_primary_micro",
        field_tokens=("transport", "broken_infrastructure"),
    )
    assert "|" in ma["composite_primary_micro"].cluster_id


def test_missing_geo_district_skips_geo_lens() -> None:
    engine = _engine()
    story = _pack_story("tc-nogeo", payload=_payload(include_geo=False))
    memberships = engine.memberships_for_story(story)
    lenses = {m.lens for m in memberships}
    assert "geographic_district_micro" not in lenses
    assert "civic_domain_micro" in lenses
