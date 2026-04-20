from __future__ import annotations

from dataclasses import dataclass

from core.promotion.types import IssueCandidateRecord, PromotionGateResult


@dataclass(frozen=True)
class PromotionGatePolicy:
    min_readiness_score: int = 70
    min_stories: int = 2


def evaluate_promotion_gates(
    candidate: IssueCandidateRecord, policy: PromotionGatePolicy
) -> PromotionGateResult:
    reasons: list[str] = []
    if candidate.readiness_score < policy.min_readiness_score:
        reasons.append("readiness_below_threshold")
    if len(candidate.story_ids) < policy.min_stories:
        reasons.append("insufficient_story_evidence")

    passed = not reasons
    return PromotionGateResult(
        passed=passed,
        reasons=tuple(reasons),
        details={
            "readiness_score": candidate.readiness_score,
            "story_count": len(candidate.story_ids),
        },
    )
