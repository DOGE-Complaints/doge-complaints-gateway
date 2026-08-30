"""GW-SSR-04: schema-pack exact lens membership; civic ClusterLens unchanged."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

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
    PackLensMissingPathError,
    SchemaPackClusterEngine,
    SchemaRef,
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


def _engine() -> SchemaPackClusterEngine:
    return SchemaPackClusterEngine(LocalSchemaRuntime(packs_root=PACKS_ROOT))


def _civic_clustering() -> ClusteringEngine:
    return ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        id_algorithm="legacy_hash",
    )


def _issue_service(stories: InMemoryStoryRepository) -> IssueCreateService:
    return IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )


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


def _pack_story(
    story_id: str,
    *,
    office_id: str = "station-42",
    extra_payload: dict | None = None,
    schema_id: str = "legal_process",
    bound_schema_version: str = "v1",
) -> object:
    payload: dict = {"institution": {"office_id": office_id}}
    if extra_payload:
        payload.update(extra_payload)
    return make_story_record(
        story_id=story_id,
        narrative_original_text="filed at station",
        submitter_external_user_id=f"user-{story_id}",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="legal"),
        narrative_description=narrative_dict(en="legal description"),
        schema_id=schema_id,
        bound_schema_version=bound_schema_version,
        structured_payload=payload,
    )


def _orchestrator(
    stories: InMemoryStoryRepository,
    store: InMemoryClusterMembershipStore | None = None,
) -> StoryClusterOrchestrator:
    return StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_clustering(),
        issue_create_service=_issue_service(stories),
        cluster_membership_store=store if store is not None else InMemoryClusterMembershipStore(),
        schema_pack_engine=_engine(),
        node_schema_id="legal_process",
        node_schema_version="v1",
    )


def test_clusterlens_still_ten_civic_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert "police_station" not in {member.value for member in ClusterLens}


def test_two_payloads_same_office_id_share_cluster_id() -> None:
    engine = _engine()
    a = _pack_story("p1", office_id="station-42")
    b = _pack_story("p2", office_id="station-42")
    ma = engine.memberships_for_story(a)
    mb = engine.memberships_for_story(b)
    assert len(ma) == 1
    assert ma[0].cluster_id == mb[0].cluster_id
    assert ma[0].cluster_id == pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-42",),
    )
    assert ma[0].cluster_id.startswith("schema:legal_process:police_station:")
    assert ma[0].lens == "police_station"


def test_cluster_id_does_not_embed_secret_note() -> None:
    engine = _engine()
    story = _pack_story(
        "p-secret",
        office_id="station-7",
        extra_payload={"secret_note": "do-not-cluster-this"},
    )
    memberships = engine.memberships_for_story(story)
    assert len(memberships) == 1
    assert "do-not-cluster-this" not in memberships[0].cluster_id
    assert "secret_note" not in memberships[0].cluster_id


def test_missing_path_skip_yields_no_membership() -> None:
    engine = _engine()
    story = make_story_record(
        story_id="p-skip",
        schema_id="legal_process",
        bound_schema_version="v1",
        structured_payload={"institution": {"name": "only-name"}},
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
    )
    assert engine.memberships_for_story(story) == ()


def test_missing_path_error_policy_raises() -> None:
    runtime = LocalSchemaRuntime(packs_root=PACKS_ROOT)
    context = runtime.resolve(SchemaRef("legal_process", "v1"))
    lens = replace(context.exact_lenses[0], missing_value_policy="error")
    context = replace(context, exact_lenses=(lens,))
    story = make_story_record(
        story_id="p-err",
        schema_id="legal_process",
        bound_schema_version="v1",
        structured_payload={},
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
    )
    engine = _engine()
    with pytest.raises(PackLensMissingPathError) as exc:
        engine.memberships_for_context(story, context)
    assert exc.value.code == "pack_lens_missing_path"


def test_unbound_story_is_not_schema_bound() -> None:
    civic = _civic_story("c1")
    assert is_schema_bound(civic) is False
    assert _engine().memberships_for_story(civic) == ()


def test_process_all_pending_persists_pack_membership_without_clustered() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p1", office_id="station-42"))
    stories.save_story(_pack_story("p2", office_id="station-42"))
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert created == []
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-42",),
    )
    assert store.get_cluster_members(cid, "police_station") == ["p1", "p2"]
    for sid in ("p1", "p2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
    # idempotent re-run
    orchestrator.process_all_pending()
    assert store.get_cluster_members(cid, "police_station") == ["p1", "p2"]


def test_schema_bound_does_not_enter_civic_buckets() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_civic_story("c1"))
    stories.save_story(_civic_story("c2"))
    stories.save_story(_pack_story("p1", office_id="station-99"))
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert created  # civic issue from unlabeled fixtures
    pack = stories.get_story("p1")
    assert pack is not None
    assert pack.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-99",),
    )
    assert store.get_cluster_members(cid, "police_station") == ["p1"]
    for sid in ("c1", "c2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert store.get_cluster_members(cid, ClusterLens.CIVIC_DOMAIN_MICRO.value) == []


def test_process_story_pack_returns_none_and_keeps_ready() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_pack_story("p1"))
    orchestrator = _orchestrator(stories, store)
    assert orchestrator.process_story("p1") is None
    row = stories.get_story("p1")
    assert row is not None
    assert row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE


def test_payload_without_binding_stays_civic() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    civic_with_payload = make_story_record(
        story_id="c-payload",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
        structured_payload={"institution": {"office_id": "should-not-pack"}},
    )
    stories.save_story(civic_with_payload)
    stories.save_story(_civic_story("c2"))
    orchestrator = _orchestrator(stories, store)
    created = orchestrator.process_all_pending()
    assert created
    row = stories.get_story("c-payload")
    assert row is not None
    assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert store.get_cluster_members(
        pack_cluster_id(
            schema_id="legal_process",
            lens_id="police_station",
            field_tokens=("should-not-pack",),
        ),
        "police_station",
    ) == []


def test_cron_source_still_calls_process_all_pending() -> None:
    text = (GATEWAY_ROOT / "src/core/scheduler/cluster_cron.py").read_text(encoding="utf-8")
    assert "process_all_pending" in text
    assert "class ClusterCronJob" in text
    assert text.count("class ClusterCronJob") == 1
