"""GW-SSR-25: civic snapshot-depth regression + pack exact membership on geo.*."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from core.cluster import ClusteringEngine, ClusterLens, StoryProfileSignals
from core.cluster.engine import cluster_key_for_lens
from core.cluster.types import ClusterLens as ClusterLensEnum
from core.domain import StoryGeoSnapshot, StoryLifecycleStatus
from core.geo.scope import geo_filter_bucket
from core.schema import LocalSchemaRuntime, SchemaPackClusterEngine, SchemaRef, pack_cluster_id
from core.schema.contracts import ExactLensBlock, ReadinessPolicy
from tests.intake_v2_fixtures import make_story_record

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def _snapshot(**overrides: object) -> StoryGeoSnapshot:
    base: dict[str, object] = dict(
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
        houses=(),
        address_line="Pikk, 12",
    )
    base.update(overrides)
    return StoryGeoSnapshot(**base)  # type: ignore[arg-type]


def test_clusterlens_still_ten_members() -> None:
    assert len(ClusterLensEnum) == 10


def test_civic_geo_filter_bucket_uses_admin_not_street() -> None:
    geo = _snapshot(street="Lai", house="3", houses=("3", "5"))
    assert geo_filter_bucket(geo, "district") == "geo:district:kesklinn"
    assert "pikk" not in geo_filter_bucket(geo, "district")
    assert "lai" not in geo_filter_bucket(geo, "district")


def test_civic_unlabeled_geo_stays_agnostic() -> None:
    assert geo_filter_bucket(None, "district") == "geo:agnostic"


def test_civic_missing_admin_stays_unknown_with_snapshot_depth() -> None:
    geo = _snapshot(admin_district=None, street="Pikk", house="12", houses=("12",))
    assert geo_filter_bucket(geo, "district") == "geo:unknown"


def test_civic_cluster_key_ignores_street_houses() -> None:
    signals = {"civic_domain": "roads"}
    a = StoryProfileSignals("a", signals, geo=_snapshot(street="Pikk", house="12"))
    b = StoryProfileSignals("b", signals, geo=_snapshot(street="Lai", house="3", houses=("3",)))
    key_a = cluster_key_for_lens(a, ClusterLens.CIVIC_DOMAIN_MICRO, geo_filter="district")
    key_b = cluster_key_for_lens(b, ClusterLens.CIVIC_DOMAIN_MICRO, geo_filter="district")
    assert key_a == key_b
    assert "geo:district:kesklinn" in key_a


def test_civic_engine_membership_stable_with_snapshot_depth() -> None:
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        geo_filter="district",
        id_algorithm="sha256",
    )
    signals = {
        "civic_domain": "roads",
        "failure_pattern": "broken_infrastructure",
        "civic_weight": "recurring_issue",
        "desired_outcome": "safer_space",
        "affected_group": "general_public",
        "geographic_district": "unknown",
    }
    profiles = (
        StoryProfileSignals("s1", signals, geo=_snapshot(street="Pikk", house="12")),
        StoryProfileSignals("s2", signals, geo=_snapshot(street="Lai", house="99")),
    )
    memberships = engine.memberships(profiles)
    lens = ClusterLens.CIVIC_DOMAIN_MICRO.value
    assert memberships["s1"][lens] == memberships["s2"][lens]


def _pack_engine() -> SchemaPackClusterEngine:
    return SchemaPackClusterEngine(LocalSchemaRuntime(packs_root=PACKS_ROOT))


def _tallinn_story(story_id: str, *, district: str, street: str) -> object:
    return make_story_record(
        story_id=story_id,
        schema_id="tallinn_civic",
        bound_schema_version="v1",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        structured_payload={"geo": {"district": district, "street": street}},
        geo=_snapshot(admin_district=district, street=street),
    )


def test_pack_exact_membership_on_geo_district() -> None:
    engine = _pack_engine()
    a = _tallinn_story("t1", district="kesklinn", street="Pikk")
    b = _tallinn_story("t2", district="kesklinn", street="Lai")
    ma = engine.memberships_for_story(a)
    mb = engine.memberships_for_story(b)
    geo_memberships = [m for m in ma if m.lens == "geographic_district_micro"]
    assert len(geo_memberships) == 1
    assert geo_memberships[0].cluster_id == next(
        m.cluster_id for m in mb if m.lens == "geographic_district_micro"
    )
    assert geo_memberships[0].cluster_id == pack_cluster_id(
        schema_id="tallinn_civic",
        lens_id="geographic_district_micro",
        field_tokens=("kesklinn",),
    )


def test_pack_missing_geo_district_skips_membership() -> None:
    engine = _pack_engine()
    story = make_story_record(
        story_id="t-skip",
        schema_id="tallinn_civic",
        bound_schema_version="v1",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        structured_payload={"geo": {"street": "Pikk"}},
        geo=_snapshot(street="Pikk"),
    )
    geo_memberships = [
        m for m in engine.memberships_for_story(story) if m.lens == "geographic_district_micro"
    ]
    assert geo_memberships == []


def test_pack_exact_membership_on_geo_street_fixture() -> None:
    runtime = LocalSchemaRuntime(packs_root=PACKS_ROOT)
    context = runtime.resolve(SchemaRef("tallinn_civic", "v1"))
    street_lens = ExactLensBlock(
        lens_id="geo_street_demo",
        source_fields=("geo.street",),
        algorithm="exact",
        scope="node",
        scale="micro",
        missing_value_policy="skip",
        min_size=2,
        readiness_policy=ReadinessPolicy(
            min_readiness_score=35,
            min_stories=2,
            require_actionable_canonical_type=False,
        ),
        version="v1",
    )
    context = replace(context, exact_lenses=(street_lens,))
    engine = _pack_engine()
    a = _tallinn_story("ts1", district="kesklinn", street="Pikk")
    b = _tallinn_story("ts2", district="kesklinn", street="Pikk")
    c = _tallinn_story("ts3", district="kesklinn", street="Lai")
    ma = engine.memberships_for_context(a, context)
    mb = engine.memberships_for_context(b, context)
    mc = engine.memberships_for_context(c, context)
    assert len(ma) == 1 and ma[0].lens == "geo_street_demo"
    assert ma[0].cluster_id == mb[0].cluster_id
    assert ma[0].cluster_id != mc[0].cluster_id
    assert ma[0].cluster_id == pack_cluster_id(
        schema_id="tallinn_civic",
        lens_id="geo_street_demo",
        field_tokens=("Pikk",),
    )
