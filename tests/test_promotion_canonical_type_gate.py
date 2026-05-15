from __future__ import annotations

from core.promotion.gates import PromotionGatePolicy, evaluate_promotion_gates
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus


def _candidate() -> IssueCandidateRecord:
    return IssueCandidateRecord(
        candidate_id="cand-1",
        status=IssueCandidateStatus.DRAFT,
        cluster_id="cluster-1",
        story_ids=("s1", "s2"),
        readiness_score=80,
        title="Test cluster",
    )


def test_gate_rejects_observation_only_cluster() -> None:
    result = evaluate_promotion_gates(
        _candidate(),
        policy=PromotionGatePolicy(),
        cluster_canonical_types=("observation", "observation"),
    )
    assert not result.passed
    assert "no_actionable_canonical_type" in result.reasons


def test_gate_passes_with_complaint_in_cluster() -> None:
    result = evaluate_promotion_gates(
        _candidate(),
        policy=PromotionGatePolicy(),
        cluster_canonical_types=("observation", "complaint"),
    )
    assert result.passed


def test_gate_passes_with_system_bug() -> None:
    result = evaluate_promotion_gates(
        _candidate(),
        policy=PromotionGatePolicy(),
        cluster_canonical_types=("system_bug",),
    )
    assert result.passed
