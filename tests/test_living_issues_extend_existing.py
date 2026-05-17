from __future__ import annotations

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine
from core.domain import StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService
from core.projection.extraction_policy import (
    canonical_labels_from_cluster,
    spa_labels_from_canonical,
)
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def _story(
    story_id: str,
    *,
    text: str,
    title_hint: str,
    labels: tuple[str, ...] = ("roads", "broken_infrastructure"),
) -> object:
    return make_story_record(
        story_id=story_id,
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        narrative_title=narrative_dict(en=title_hint),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=labels,
    )


def _build_orchestrator(
    stories: InMemoryStoryRepository,
) -> tuple[StoryClusterOrchestrator, IssuePromotionService, InMemoryIssueProjectionStore]:
    projection_store = InMemoryIssueProjectionStore()
    promotion_service = IssuePromotionService(
        candidates=InMemoryIssueCandidateStore(),
        audit_log=InMemoryReviewAuditLogRepository(),
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
    )
    issue_create = IssueCreateService(
        promotion_service=promotion_service,
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        issue_projection_store=projection_store,
        issue_story_link_store=InMemoryIssueStoryLinkStore(),
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )
    return orchestrator, promotion_service, projection_store


def test_extend_flow_process_story_story_count_three_and_labels_union() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        _story(
            "s1",
            text="street light broken near district center",
            title_hint="Broken light",
            labels=("roads", "broken_infrastructure"),
        )
    )
    stories.save_story(
        _story(
            "s2",
            text="street light still broken in same district",
            title_hint="Street light issue",
            labels=("roads",),
        )
    )
    orchestrator, promotion_service, projection_store = _build_orchestrator(stories)

    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None
    promoted = promotion_service.candidates.get(issue_id)
    assert promoted is not None
    assert len(promoted.story_ids) == 2
    assert set(promoted.story_ids) == {"s1", "s2"}

    stories.save_story(
        _story(
            "s3",
            text="street light broken near square same district",
            title_hint="Square light",
            labels=("roads", "parking"),
        )
    )
    extend_issue_id = orchestrator.process_story("s3")
    assert extend_issue_id == issue_id

    promoted_after = promotion_service.candidates.get(issue_id)
    assert promoted_after is not None
    assert len(promoted_after.story_ids) == 3
    assert set(promoted_after.story_ids) == {"s1", "s2", "s3"}

    cluster_records = tuple(
        stories.get_story(sid)
        for sid in ("s1", "s2", "s3")
        if stories.get_story(sid) is not None
    )
    expected_canonical = canonical_labels_from_cluster(cluster_records)
    assert set(expected_canonical) == {"roads", "broken_infrastructure", "parking"}

    payload = projection_store._rows[issue_id]["payload"]
    assert set(payload["labels"]) == set(spa_labels_from_canonical(expected_canonical))

    for sid in ("s1", "s2", "s3"):
        story = stories.get_story(sid)
        assert story is not None
        assert story.lifecycle_status is StoryLifecycleStatus.CLUSTERED
