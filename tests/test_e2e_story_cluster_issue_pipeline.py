from __future__ import annotations

from datetime import UTC, datetime

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.repositories import (
    InMemoryIssueStoryLinkStore,
    InMemoryIssueProjectionEmbeddingStore,
    InMemoryIssueProjectionStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)


def _story(story_id: str, text: str, title_hint: str) -> StoryRecord:
    now = datetime.now(UTC)
    return StoryRecord(
        story_id=story_id,
        schema_version="v1",
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        submitter_identity_issuer=None,
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title_hint=title_hint,
        narrative_canonical_type="improvement",
        narrative_canonical_labels=("infrastructure",),
    )


def test_e2e_story_cluster_issue_pipeline_creates_projection() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_story("s1", "street light broken near district center", "Broken light"))
    stories.save_story(_story("s2", "street light still broken in same district", "Street light issue"))

    projection_store = InMemoryIssueProjectionStore()
    projection_embedding_store = InMemoryIssueProjectionEmbeddingStore()
    issue_story_link_store = InMemoryIssueStoryLinkStore()
    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(min_readiness_score=70, min_stories=2),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_projection_embedding_store=projection_embedding_store,
        issue_story_link_store=issue_story_link_store,
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )

    issue_id = orchestrator.process_story("s1")

    assert issue_id is not None
    assert projection_store._rows is not None
    assert issue_id in projection_store._rows
    saved = projection_store._rows[issue_id]
    assert saved["status"] == "promoted"
    assert projection_embedding_store._rows is not None
    assert projection_embedding_store._rows[0]["embedding_policy_version"] == "m2.issue_embedding_policy.v1"
    assert issue_story_link_store._rows is not None
    assert issue_id in issue_story_link_store._rows
