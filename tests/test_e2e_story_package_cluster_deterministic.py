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
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def _story(story_id: str, text: str) -> StoryRecord:
    now = datetime.now(UTC)
    return StoryRecord(
        story_id=story_id,
        schema_version="m2.story_intake_envelope.v1",
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        submitter_identity_issuer=None,
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title_hint="District lighting issue",
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
    )


def test_story_package_clustering_is_deterministic_for_same_package() -> None:
    stories = InMemoryStoryRepository()
    package = (
        _story("pkg-1", "Street lights broken near district center and unsafe at night"),
        _story("pkg-2", "Street lights broken near district center and unsafe at night"),
        _story("pkg-3", "Street lights broken near district center and unsafe at night"),
    )
    for story in package:
        stories.save_story(story)

    projection_store = InMemoryIssueProjectionStore()
    projection_embedding_store = InMemoryIssueProjectionEmbeddingStore()
    issue_story_link_store = InMemoryIssueStoryLinkStore()
    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
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

    issue_ids = [orchestrator.process_story(story.story_id) for story in package]
    issue_ids = [issue_id for issue_id in issue_ids if issue_id is not None]

    assert issue_ids
    assert issue_story_link_store._rows
    linked_rows = [issue_story_link_store._rows[issue_id] for issue_id in issue_ids]
    cluster_ids = {cluster_id for cluster_id, _ in linked_rows}
    assert len(cluster_ids) == 1

    expected_story_ids = {story.story_id for story in package}
    for _, linked_story_ids in linked_rows:
        assert set(linked_story_ids) == expected_story_ids
