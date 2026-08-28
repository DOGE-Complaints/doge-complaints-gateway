"""GW-SSR-05 T02: optional gate_policy on command / submit_for_review."""

from __future__ import annotations

import pytest

from core.application.issue_create import IssueCreateCommand
from core.promotion import IssuePromotionService, PromotionGatePolicy, PromotionStateError
from core.promotion.types import IssueCandidateStatus


def test_issue_create_command_gate_policy_defaults_none() -> None:
    command = IssueCreateCommand(
        cluster_id="c1",
        story_ids=("s1", "s2"),
        readiness_score=80,
        title="civic title",
    )
    assert command.gate_policy is None
    assert command.min_stories is None


def test_submit_for_review_none_policy_uses_civic_and_rejects_empty_types() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="civic-empty-types",
        story_ids=("s1", "s2"),
        readiness_score=80,
        title="civic cluster",
    )
    with pytest.raises(PromotionStateError, match="no_actionable_canonical_type"):
        svc.submit_for_review(candidate.candidate_id, cluster_canonical_types=())


def test_submit_for_review_pack_override_passes_without_civic_types() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="pack-override",
        story_ids=("p1", "p2", "p3"),
        readiness_score=40,
        title="pack cluster",
    )
    pack_policy = PromotionGatePolicy(
        min_readiness_score=40,
        min_stories=3,
        require_actionable_canonical_type=False,
    )
    updated = svc.submit_for_review(
        candidate.candidate_id,
        cluster_canonical_types=(),
        policy=pack_policy,
    )
    assert updated.status is IssueCandidateStatus.READY_FOR_REVIEW
    assert svc.gate_policy.require_actionable_canonical_type is True
    assert svc.gate_policy.min_readiness_score == 70
