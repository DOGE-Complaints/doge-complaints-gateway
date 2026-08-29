"""GW-SSR-10 T01: dual civic + pack exact memberships on one story_id."""

from __future__ import annotations

import json
import shutil
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
from core.schema import LocalSchemaRuntime, SchemaPackClusterEngine, pack_cluster_id
from tests.intake_v2_fixtures import make_story_record, narrative_dict
from tests.test_gw_ssr_04_schema_driven_cluster_lens import (
    PACKS_ROOT,
    _civic_story,
    _orchestrator,
    _pack_story,
)

GATEWAY_ROOT = Path(__file__).resolve().parents[1]


def _lenses_for(store: InMemoryClusterMembershipStore, story_id: str) -> set[str]:
    assert store._story_lens_to_cluster is not None
    return {ln for (sid, ln) in store._story_lens_to_cluster if sid == story_id}


def _write_dual_legal_root(tmp_path: Path, *, dual: bool = True) -> Path:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    if dual:
        manifest["dual_civic_lenses"] = True
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


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


def _dual_orchestrator(
    stories: InMemoryStoryRepository,
    store: InMemoryClusterMembershipStore,
    packs_root: Path,
) -> StoryClusterOrchestrator:
    return StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(
            active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
            primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
            id_algorithm="legacy_hash",
        ),
        issue_create_service=_issue_service(stories),
        cluster_membership_store=store,
        schema_pack_engine=SchemaPackClusterEngine(LocalSchemaRuntime(packs_root=packs_root)),
    )


def _dual_bound_story(story_id: str, *, office_id: str = "station-42") -> object:
    return make_story_record(
        story_id=story_id,
        narrative_original_text="broken road filed at station",
        submitter_external_user_id=f"user-{story_id}",
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        narrative_title=narrative_dict(en="dual"),
        narrative_description=narrative_dict(en="dual description"),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
        schema_id="legal_process",
        bound_schema_version="v1",
        structured_payload={"institution": {"office_id": office_id}},
    )


def test_dual_fixture_civic_and_pack_lens_on_same_story(tmp_path: Path) -> None:
    packs = _write_dual_legal_root(tmp_path)
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_dual_bound_story("d1"))
    orchestrator = _dual_orchestrator(stories, store, packs)
    orchestrator.process_story("d1")
    lenses = _lenses_for(store, "d1")
    assert ClusterLens.CIVIC_DOMAIN_MICRO.value in lenses
    assert "police_station" in lenses
    cid = pack_cluster_id(
        schema_id="legal_process",
        lens_id="police_station",
        field_tokens=("station-42",),
    )
    assert store.get_cluster_members(cid, "police_station") == ["d1"]
    assert store._story_lens_to_cluster is not None
    civic_cid = store._story_lens_to_cluster[("d1", ClusterLens.CIVIC_DOMAIN_MICRO.value)]
    assert civic_cid != cid


def test_pack_without_dual_key_stays_exact_only() -> None:
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(
        _pack_story(
            "p1",
            office_id="station-42",
        )
    )
    # labels present but legal_process has no dual key
    row = stories.get_story("p1")
    assert row is not None
    orchestrator = _orchestrator(stories, store)
    orchestrator.process_story("p1")
    lenses = _lenses_for(store, "p1")
    assert lenses == {"police_station"}
    assert ClusterLens.CIVIC_DOMAIN_MICRO.value not in lenses


def test_civic_unbound_unchanged_when_dual_bound_present(tmp_path: Path) -> None:
    packs = _write_dual_legal_root(tmp_path)
    stories = InMemoryStoryRepository()
    store = InMemoryClusterMembershipStore()
    stories.save_story(_civic_story("c1"))
    stories.save_story(_civic_story("c2"))
    stories.save_story(_dual_bound_story("d1", office_id="station-99"))
    orchestrator = _dual_orchestrator(stories, store, packs)
    created = orchestrator.process_all_pending()
    assert created
    for sid in ("c1", "c2"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    dual_lenses = _lenses_for(store, "d1")
    assert ClusterLens.CIVIC_DOMAIN_MICRO.value in dual_lenses
    assert "police_station" in dual_lenses
    assert store._story_lens_to_cluster is not None
    dual_civic_cid = store._story_lens_to_cluster[
        ("d1", ClusterLens.CIVIC_DOMAIN_MICRO.value)
    ]
    pack_cid = store._story_lens_to_cluster[("d1", "police_station")]
    assert dual_civic_cid != pack_cid
    assert not pack_cid.startswith("cluster:")
    assert pack_cid.startswith("schema:")
    dual_row = stories.get_story("d1")
    assert dual_row is not None
    assert dual_row.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
