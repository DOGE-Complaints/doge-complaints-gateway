"""Shared factories for REQ-40 / REQ-39 Zone K geo propagation contract tests."""

from __future__ import annotations

from typing import Any

from core.application.cluster_orchestrator import StoryClusterOrchestrator
from core.application.issue_create import IssueCreateService, StoryPromotionProjectionBridge
from core.cluster import ClusteringEngine
from core.domain import StoryGeoSnapshot, StoryRecord
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryRepository,
)
from core.projection import IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from tests.intake_v2_fixtures import make_story_record, narrative_dict


def geo_kalamaja() -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label="Kalamaja, Tallinn",
        latitude=59.4372,
        longitude=24.7453,
        confidence=0.9,
        provider="stub",
        admin_district="Põhja-Tallinn",
        admin_settlement="Tallinn",
        admin_region="Harju maakond",
        admin_country="EE",
    )


def geo_mustamae() -> StoryGeoSnapshot:
    return StoryGeoSnapshot(
        normalized_label="Mustamäe, Tallinn",
        latitude=59.408,
        longitude=24.698,
        confidence=0.85,
        provider="stub",
        admin_district="Mustamäe",
        admin_settlement="Tallinn",
        admin_region="Harju maakond",
        admin_country="EE",
    )


def story_record(
    story_id: str,
    *,
    text: str,
    title_hint: str,
    geo: StoryGeoSnapshot | None = None,
    labels: tuple[str, ...] = ("roads", "broken_infrastructure"),
    **extra: Any,
) -> StoryRecord:
    return make_story_record(
        story_id=story_id,
        narrative_original_text=text,
        submitter_external_user_id=f"user-{story_id}",
        narrative_title=narrative_dict(en=title_hint),
        narrative_canonical_type="complaint",
        narrative_canonical_labels=labels,
        geo=geo,
        **extra,
    )


def build_orchestrator(
    stories: InMemoryStoryRepository,
) -> tuple[StoryClusterOrchestrator, InMemoryIssueProjectionStore]:
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
    return orchestrator, projection_store


def issue_payload(
    projection_store: InMemoryIssueProjectionStore,
    issue_id: str,
) -> dict[str, object]:
    payload = projection_store.get_projection(issue_id)
    assert payload is not None
    return payload
