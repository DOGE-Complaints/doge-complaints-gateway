from __future__ import annotations

import pytest

from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.infrastructure.repositories import InMemoryStoryRepository
from core.projection import DeterministicStoryToProjectionPolicy, IssueProjectionService
from core.promotion import IssuePromotionService
from core.promotion.service import PromotionStateError
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)


def _build_issue_create_service() -> IssueCreateService:
    return IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=InMemoryStoryRepository()),
    )


def test_issue_create_rejects_whitespace_story_ids() -> None:
    service = _build_issue_create_service()
    with pytest.raises(PromotionStateError):
        service.create_issue(
            IssueCreateCommand(
                cluster_id="cluster-x",
                story_ids=("   ",),
                readiness_score=90,
                title="Valid title",
            )
        )


def test_derive_labels_is_deterministic_and_unique() -> None:
    draft = DeterministicStoryToProjectionPolicy().build_draft(
        promoted_title="Danger in district road",
        aggregate_text="road road safety safety district infrastructure",
    )
    labels = draft.labels
    assert labels == tuple(dict.fromkeys(labels))
    assert "safety" in labels
    assert "district" in labels


def test_derive_issue_type_defaults_to_improvement() -> None:
    draft = DeterministicStoryToProjectionPolicy().build_draft(
        promoted_title="Community feedback",
        aggregate_text="We would like to improve the park lighting experience.",
    )
    assert draft.issue_type == "IMPROVEMENT"
