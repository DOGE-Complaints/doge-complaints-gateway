from __future__ import annotations

from datetime import UTC, datetime

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine, ClusterLens
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
from core.promotion.service import PromotionStateError


def _story(story_id: str, text: str, title_hint: str) -> StoryRecord:
    from tests.intake_v2_fixtures import make_story_record, narrative_dict

    return make_story_record(
        story_id=story_id,
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        narrative_title=narrative_dict(en=title_hint),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=("roads", "broken_infrastructure"),
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
        gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
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
    assert saved["status"] == "PUBLISHED"
    assert projection_embedding_store._rows is not None
    assert projection_embedding_store._rows[0]["embedding_policy_version"] == "m3.doge_issue_embedding_policy.v1"
    assert issue_story_link_store._rows is not None
    assert issue_id in issue_story_link_store._rows
    s1 = stories.get_story("s1")
    s2 = stories.get_story("s2")
    assert s1 is not None and s2 is not None
    assert s1.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert s2.lifecycle_status is StoryLifecycleStatus.CLUSTERED


def test_process_story_returns_none_when_story_not_found() -> None:
    stories = InMemoryStoryRepository()
    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )
    assert orchestrator.process_story("missing-story") is None


def test_process_story_returns_none_when_story_not_ready_for_profile() -> None:
    stories = InMemoryStoryRepository()
    now = datetime.now(UTC)
    from tests.intake_v2_fixtures import make_story_record, narrative_dict

    stories.save_story(
        make_story_record(
            story_id="partial",
            narrative_original_text="single report",
            submitter_external_user_id="user-partial",
            lifecycle_status=StoryLifecycleStatus.PARTIAL_READY,
            narrative_title=narrative_dict(en="Partial"),
            narrative_canonical_type="complaint",
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
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )
    assert orchestrator.process_story("partial") is None


def test_process_story_suppresses_promotion_state_error() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_story("s1", "street light broken", "Broken light"))
    stories.save_story(_story("s2", "street light broken", "Broken light"))

    class _AlwaysFailIssueCreate:
        def create_issue(self, command: object) -> object:
            raise PromotionStateError("forced failure")

    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=_AlwaysFailIssueCreate(),  # type: ignore[arg-type]
    )
    assert orchestrator.process_story("s1") is None


def test_process_story_second_call_returns_none_after_stories_marked_clustered() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_story("s1", "district lights broken", "Broken light"))
    stories.save_story(_story("s2", "district lights broken", "Broken light"))

    class _IssueCreateOnce:
        def create_issue(self, command: object) -> object:
            class _Result:
                issue_id = "issue-first"

            return _Result()

    issue_create = _IssueCreateOnce()
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,  # type: ignore[arg-type]
    )
    assert orchestrator.process_story("s1") == "issue-first"
    row1 = stories.get_story("s1")
    row2 = stories.get_story("s2")
    assert row1 is not None and row2 is not None
    assert row1.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert row2.lifecycle_status is StoryLifecycleStatus.CLUSTERED
    assert orchestrator.process_story("s1") is None


def test_process_story_returns_none_when_story_not_in_memberships() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_story("s1", "same narrative", "Broken light"))
    stories.save_story(_story("s2", "same narrative", "Broken light"))

    class _MembershipsWithoutTargetEngine:
        active_lenses = (ClusterLens.CIVIC_DOMAIN_MICRO,)

        def memberships(
            self, profiles: object, *, id_algorithm: str | None = None
        ) -> dict[str, dict[str, str]]:
            return {"s2": {"civic_domain_micro": "cluster:civic_domain_micro:1"}}

        def resolved_primary_lens(self) -> ClusterLens:
            return ClusterLens.CIVIC_DOMAIN_MICRO

    issue_create = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(min_readiness_score=60, min_stories=2),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_MembershipsWithoutTargetEngine(),  # type: ignore[arg-type]
        issue_create_service=issue_create,
    )
    assert orchestrator.process_story("s1") is None


def test_e2e_living_issue_two_batches_reuses_issue_and_appends_stories() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_story("s1", "district lights broken near school", "Broken light"))
    stories.save_story(_story("s2", "district lights broken near station", "Broken light"))

    projection_store = InMemoryIssueProjectionStore()
    issue_story_link_store = InMemoryIssueStoryLinkStore()
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
        issue_story_link_store=issue_story_link_store,
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=ClusteringEngine(),
        issue_create_service=issue_create,
    )

    first_issue_ids = orchestrator.process_all_pending()
    assert len(first_issue_ids) == 1
    issue_id = first_issue_ids[0]

    stories.save_story(_story("s3", "district lights broken near square", "Broken light"))
    stories.save_story(_story("s4", "district lights broken near bridge", "Broken light"))
    second_issue_ids = orchestrator.process_all_pending()

    assert second_issue_ids == [issue_id]
    promoted = promotion_service.candidates.get(issue_id)
    assert promoted is not None
    assert set(promoted.story_ids) == {"s1", "s2", "s3", "s4"}

    links = issue_story_link_store._rows
    assert links is not None
    assert issue_id in links
    assert set(links[issue_id][1]) == {"s1", "s2", "s3", "s4"}
    for story_id in ("s1", "s2", "s3", "s4"):
        story = stories.get_story(story_id)
        assert story is not None
        assert story.lifecycle_status is StoryLifecycleStatus.CLUSTERED

    audit = promotion_service.audit_trail(issue_id)
    assert [entry.rationale for entry in audit][-1] == "cluster_growth_extend"
