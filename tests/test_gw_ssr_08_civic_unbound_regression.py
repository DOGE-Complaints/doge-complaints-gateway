"""GW-SSR-08 T04: civic unbound path stays; ClusterLens remains 10."""

from __future__ import annotations

from pathlib import Path

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine, ClusterLens
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from core.schema import (
    LocalSchemaRuntime,
    SchemaPackClusterEngine,
    is_schema_bound,
    pack_cluster_id,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

CLUSTERLENS_BASELINE = (
    "composite_primary_micro",
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "desired_outcome_local",
    "affected_group_local",
    "geographic_district_micro",
    "service_object_micro",
    "deep_need_local",
    "ecosystem_signal_systemic",
)


def test_civic_gate_default_and_factory_unchanged() -> None:
    from core.promotion.gates import PromotionGatePolicy

    default = PromotionGatePolicy()
    assert default.require_actionable_canonical_type is True
    assert default.min_readiness_score == 70
    assert default.min_stories == 2
    factory_src = (
        GATEWAY_ROOT / "src/core/infrastructure/service_factory.py"
    ).read_text(encoding="utf-8")
    assert "PromotionGatePolicy(" in factory_src
    assert "require_actionable_canonical_type=False" not in factory_src


def test_clusterlens_still_ten_civic_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10
    assert "tallinn_civic" not in {member.value for member in ClusterLens}


def test_unbound_civic_story_is_not_pack_membership() -> None:
    civic = make_story_record(
        story_id="civic-unbound",
        narrative_original_text="broken road in district center",
        submitter_external_user_id="user-civic",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="hint"),
        narrative_description=narrative_dict(en="hint description"),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
    )
    engine = SchemaPackClusterEngine(LocalSchemaRuntime(packs_root=PACKS_ROOT))
    assert is_schema_bound(civic) is False
    assert engine.memberships_for_story(civic) == ()


def _civic_story(story_id: str) -> object:
    return make_story_record(
        story_id=story_id,
        narrative_original_text="broken road in district center",
        submitter_external_user_id=f"user-{story_id}",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="hint"),
        narrative_description=narrative_dict(en="hint description"),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
    )


def _tallinn_bound(story_id: str) -> object:
    return make_story_record(
        story_id=story_id,
        narrative_original_text="Pothole on the tram line.",
        submitter_external_user_id=f"user-{story_id}",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="Tram pothole"),
        narrative_description=narrative_dict(en="Recurring pothole on the tram line."),
        schema_id="tallinn_civic",
        bound_schema_version="v1",
        structured_payload={
            "signals": {
                "civic_domain": "transport",
                "failure_pattern": "broken_infrastructure",
            }
        },
    )


def test_bound_tallinn_story_does_not_enter_civic_buckets() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_civic_story("c1"))
    stories.save_story(_civic_story("c2"))
    stories.save_story(_tallinn_bound("t1"))
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(
            active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
            primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
            id_algorithm="legacy_hash",
        ),
        issue_create_service=IssueCreateService(
            promotion_service=IssuePromotionService(
                candidates=InMemoryIssueCandidateStore(),
                audit_log=InMemoryReviewAuditLogRepository(),
                gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
            ),
            projection_service=IssueProjectionService(),
            bridge=StoryPromotionProjectionBridge(story_repository=stories),
        ),
        cluster_membership_store=store,
        schema_pack_engine=SchemaPackClusterEngine(
            LocalSchemaRuntime(packs_root=PACKS_ROOT)
        ),
    )
    created = orchestrator.process_all_pending()
    assert created
    pack = stories.get_story("t1")
    assert pack is not None
    assert pack.lifecycle_status is not StoryLifecycleStatus.CLUSTERED
    cid = pack_cluster_id(
        schema_id="tallinn_civic",
        lens_id="civic_domain_micro",
        field_tokens=("transport",),
    )
    assert store.get_cluster_members(cid, "civic_domain_micro") == ["t1"]
    for sid in ("c1", "c2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
        assert sid not in store.get_cluster_members(cid, "civic_domain_micro")
