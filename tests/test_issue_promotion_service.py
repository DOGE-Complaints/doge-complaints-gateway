import pytest

from core.promotion import (
    IssueCandidateStatus,
    IssuePromotionService,
    PromotionGatePolicy,
    PromotionStateError,
    ReviewDecision,
)


def test_happy_path_promotion_flow() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="cluster-1",
        story_ids=("story-a", "story-b"),
        readiness_score=80,
        title="Distinct issue candidate",
    )
    svc.submit_for_review(candidate.candidate_id)
    svc.start_review(candidate.candidate_id)
    promoted = svc.record_review(
        candidate_id=candidate.candidate_id,
        actor="reviewer-1",
        decision=ReviewDecision.APPROVE,
        rationale="Looks distinct and actionable.",
    )
    assert promoted.status == IssueCandidateStatus.PROMOTED
    audit = svc.audit_trail(candidate.candidate_id)
    assert len(audit) == 1
    assert audit[0].decision == ReviewDecision.APPROVE


def test_rejection_flow() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="cluster-2",
        story_ids=("story-x", "story-y"),
        readiness_score=70,
        title="Overlapping scope",
    )
    svc.submit_for_review(candidate.candidate_id)
    svc.start_review(candidate.candidate_id)
    rejected = svc.record_review(
        candidate_id=candidate.candidate_id,
        actor="reviewer-2",
        decision=ReviewDecision.REJECT,
        rationale="Too similar to existing issue.",
    )
    assert rejected.status == IssueCandidateStatus.REJECTED


def test_gate_blocks_low_readiness() -> None:
    policy = PromotionGatePolicy(min_readiness_score=90)
    svc = IssuePromotionService.baseline(gate_policy=policy)
    candidate = svc.create_candidate(
        cluster_id="cluster-3",
        story_ids=("story-1", "story-2"),
        readiness_score=50,
        title="Low readiness",
    )
    with pytest.raises(PromotionStateError):
        svc.submit_for_review(candidate.candidate_id)


def test_merge_and_split_draft_candidates() -> None:
    svc = IssuePromotionService.baseline()
    left = svc.create_candidate(
        cluster_id="cluster-merge",
        story_ids=("s1",),
        readiness_score=60,
        title="Left",
    )
    right = svc.create_candidate(
        cluster_id="cluster-merge",
        story_ids=("s2", "s3"),
        readiness_score=70,
        title="Right",
    )
    merged = svc.merge_candidates(left.candidate_id, right.candidate_id)
    assert set(merged.story_ids) == {"s1", "s2", "s3"}
    assert merged.readiness_score == 70

    a, b = svc.split_candidate(merged.candidate_id)
    assert a.story_ids == ("s1",)
    assert b.story_ids == ("s2", "s3")


def test_reframe_title_requires_draft() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="cluster-4",
        story_ids=("story-a", "story-b"),
        readiness_score=85,
        title="Old title",
    )
    svc.submit_for_review(candidate.candidate_id)
    with pytest.raises(PromotionStateError):
        svc.reframe_title(candidate.candidate_id, "New title")


def test_extend_candidate_updates_promoted_with_dedup_and_audit() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="cluster-extend",
        story_ids=("s1", "s2"),
        readiness_score=85,
        title="Cluster issue",
    )
    svc.submit_for_review(candidate.candidate_id)
    svc.start_review(candidate.candidate_id)
    promoted = svc.record_review(
        candidate_id=candidate.candidate_id,
        actor="reviewer",
        decision=ReviewDecision.APPROVE,
        rationale="ok",
    )

    updated = svc.extend_candidate(
        promoted.candidate_id,
        additional_story_ids=("s2", "s3"),
        new_readiness_score=92,
    )

    assert updated.status == IssueCandidateStatus.PROMOTED
    assert updated.readiness_score == 92
    assert updated.story_ids == ("s1", "s2", "s3")
    audit = svc.audit_trail(promoted.candidate_id)
    assert audit[-1].rationale == "cluster_growth_extend"
    assert audit[-1].related_story_ids == ("s2", "s3")


def test_extend_candidate_rejects_non_promoted_status() -> None:
    svc = IssuePromotionService.baseline()
    candidate = svc.create_candidate(
        cluster_id="cluster-extend-invalid",
        story_ids=("s1",),
        readiness_score=90,
        title="Draft candidate",
    )
    with pytest.raises(PromotionStateError):
        svc.extend_candidate(
            candidate.candidate_id,
            additional_story_ids=("s2",),
            new_readiness_score=90,
        )
