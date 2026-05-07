from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import patch

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateCommand, IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine, ClusterLens
from core.domain import StoryLifecycleStatus, StoryRecord
from core.infrastructure.repositories import InMemoryStoryRepository, InMemoryStorySignalStore
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def _ready_story(
    story_id: str,
    *,
    text: str = "broken road in district center",
    labels: tuple[str, ...] = ("roads", "broken_infrastructure"),
    lifecycle: StoryLifecycleStatus = StoryLifecycleStatus.READY_FOR_PROFILE,
) -> StoryRecord:
    now = datetime.now(UTC)
    return StoryRecord(
        story_id=story_id,
        schema_version="v1",
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        submitter_identity_issuer=None,
        lifecycle_status=lifecycle,
        created_at=now,
        updated_at=now,
        narrative_language="en",
        narrative_title_hint="hint",
        narrative_canonical_type="infrastructure",
        narrative_canonical_labels=labels,
    )


def _civic_engine(
    *,
    lenses: tuple[ClusterLens, ...] = (ClusterLens.CIVIC_DOMAIN_MICRO,),
    primary: ClusterLens | None = None,
) -> ClusteringEngine:
    return ClusteringEngine(
        active_lenses=lenses,
        primary_lens=primary if primary is not None else lenses[0],
        id_algorithm="legacy_hash",
        signal_source="canonical",
        geo_filter="any",
        tie_breaker="lexical",
        type_resolution="canonical_priority",
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


def test_orchestrator_skips_clustered_story() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(
        _ready_story("s1", lifecycle=StoryLifecycleStatus.CLUSTERED),
    )
    calls: list[IssueCreateCommand] = []

    class _Track:
        def create_issue(self, cmd: IssueCreateCommand) -> object:
            calls.append(cmd)
            return type("R", (), {"issue_id": "x"})()

    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=_Track(),  # type: ignore[arg-type]
    )
    assert orchestrator.process_story("s1") is None
    assert calls == []


def test_orchestrator_advances_lifecycle() -> None:
    stories = InMemoryStoryRepository()
    for sid in ("s1", "s2", "s3"):
        stories.save_story(_ready_story(sid))
    issue_create = _issue_service(stories)
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
    )
    issue_id = orchestrator.process_story("s1")
    assert issue_id is not None
    for sid in ("s1", "s2", "s3"):
        row = stories.get_story(sid)
        assert row is not None
        assert row.lifecycle_status is StoryLifecycleStatus.CLUSTERED


def test_orchestrator_signals_cached() -> None:
    store = InMemoryStorySignalStore()
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
    stories.save_story(_ready_story("s1"))
    stories.save_story(_ready_story("s2"))
    issue_create = _issue_service(stories)
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
        story_signal_store=store,
    )
    with patch("core.application.cluster_orchestrator.get_signals_for_story") as mock_gs:
        orchestrator.process_story("s1")
        mock_gs.assert_not_called()


def test_orchestrator_no_duplicate_issue() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1"))
    stories.save_story(_ready_story("s2"))
    calls: list[IssueCreateCommand] = []

    class _Track:
        def create_issue(self, cmd: IssueCreateCommand) -> object:
            calls.append(cmd)
            return type("R", (), {"issue_id": "issue-first"})()

    issue_create = _Track()  # type: ignore[assignment]
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
    )
    first = orchestrator.process_story("s1")
    assert first is not None
    n_after_first = len(calls)
    second = orchestrator.process_story("s1")
    assert second is None
    assert len(calls) == n_after_first


def test_orchestrator_readiness_passed_to_create_issue() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1"))
    stories.save_story(_ready_story("s2"))
    captured: list[IssueCreateCommand] = []

    class _Cap:
        issue_projection_store = None
        issue_projection_embedding_store = None
        issue_story_link_store = None

        def create_issue(self, cmd: IssueCreateCommand) -> object:
            captured.append(cmd)
            return type("R", (), {"issue_id": "issue-1"})()

    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=_Cap(),  # type: ignore[arg-type]
    )
    orchestrator.process_story("s1")
    assert captured
    score = captured[0].readiness_score
    assert score != 100
    assert 0 < score <= 100


def test_orchestrator_primary_lens_from_config() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1", labels=("roads", "delay")))
    stories.save_story(_ready_story("s2", labels=("roads", "delay")))
    captured: list[IssueCreateCommand] = []

    class _Cap:
        issue_projection_store = None
        issue_projection_embedding_store = None
        issue_story_link_store = None

        def create_issue(self, cmd: IssueCreateCommand) -> object:
            captured.append(cmd)
            return type("R", (), {"issue_id": "issue-1"})()

    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO, ClusterLens.FAILURE_PATTERN_MICRO),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        id_algorithm="legacy_hash",
        signal_source="canonical",
        geo_filter="any",
        tie_breaker="lexical",
        type_resolution="canonical_priority",
    )
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=engine,
        issue_create_service=_Cap(),  # type: ignore[arg-type]
    )
    orchestrator.process_story("s1")
    assert captured[0].cluster_id.startswith("cluster:civic_domain_micro:")


def test_process_all_pending_returns_empty_when_below_min_size() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1"))
    issue_create = _issue_service(stories)
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
    )
    assert orchestrator.process_all_pending() == []


def test_process_all_pending_creates_issue_for_ready_batch() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1"))
    stories.save_story(_ready_story("s2"))
    issue_create = _issue_service(stories)
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
    )
    issue_ids = orchestrator.process_all_pending()
    assert len(issue_ids) == 1
    assert issue_ids[0]


def test_process_all_pending_is_idempotent_after_lifecycle_advance() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_ready_story("s1"))
    stories.save_story(_ready_story("s2"))
    issue_create = _issue_service(stories)
    orchestrator = StoryClusterOrchestrator(
        story_repository=stories,
        clustering_engine=_civic_engine(),
        issue_create_service=issue_create,
    )
    first = orchestrator.process_all_pending()
    second = orchestrator.process_all_pending()
    assert len(first) == 1
    assert second == []
