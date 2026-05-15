from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import patch

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusterLens, ClusteringEngine
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStorySignalStore
from core.infrastructure.repositories import InMemoryStorySignalStore, InMemoryStoryRepository
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def test_signal_persistence_read_after_write_in_memory() -> None:
    store = InMemoryStorySignalStore()
    signals = {"civic_domain": "roads", "failure_pattern": "broken_infrastructure"}
    store.save_signals("story-1", "v2.canonical", signals)
    result = store.get_signals("story-1", "v2.canonical")
    assert dict(result or {}) == signals


def test_signal_store_returns_none_for_different_policy() -> None:
    store = InMemoryStorySignalStore()
    store.save_signals("story-1", "v2.canonical", {"civic_domain": "roads"})
    assert store.get_signals("story-1", "v1.keyword") is None


def test_signal_persistence_read_after_write_sqlite() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    store = SqliteStorySignalStore(db=db)
    signals = {"civic_domain": "roads", "failure_pattern": "delay"}
    store.save_signals("story-1", "v2.canonical", signals)
    result = store.get_signals("story-1", "v2.canonical")
    assert dict(result or {}) == signals


def test_signals_not_recomputed_if_cached() -> None:
    db = SqliteDatabase.from_url("sqlite:///:memory:")
    db.ensure_schema()
    store = SqliteStorySignalStore(db=db)
    cached = {
        "civic_domain": "roads",
        "failure_pattern": "broken_infrastructure",
        "civic_weight": "isolated",
        "desired_outcome": "unknown",
        "affected_group": "general_public",
        "geographic_district": "unknown",
    }
    store.save_signals("s1", "v2.canonical", cached)
    store.save_signals("s2", "v2.canonical", cached)

    stories = InMemoryStoryRepository()
    now = datetime.now(UTC)
    for sid in ("s1", "s2"):
        stories.save_story(
            StoryRecord(
                story_id=sid,
                schema_version="v1",
                narrative_original_text="broken road near center",
                submitter_external_user_id=f"u-{sid}",
                submitter_identity_issuer=None,
                lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
                created_at=now,
                updated_at=now,
                narrative_canonical_labels=("roads", "broken_infrastructure"),
            )
        )

    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO,),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        id_algorithm="legacy_hash",
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=engine,
        issue_create_service=issue_create,
        story_signal_store=store,
    )

    with patch("core.application.cluster_orchestrator.get_signals_for_story") as mock_gs:
        orchestrator.process_story("s1")
        mock_gs.assert_not_called()
