from __future__ import annotations

from dataclasses import dataclass

from core.promotion.types import IssueCandidateRecord, PromotionGateResult

ACTIONABLE_CANONICAL_TYPES = frozenset({"complaint", "system_bug"})


@dataclass(frozen=True)
class PromotionGatePolicy:
    min_readiness_score: int = 70
    min_stories: int = 2
    require_actionable_canonical_type: bool = True


def evaluate_promotion_gates(
    candidate: IssueCandidateRecord,
    policy: PromotionGatePolicy,
    *,
    cluster_canonical_types: tuple[str, ...] | None = None,
) -> PromotionGateResult:
    reasons: list[str] = []
    if candidate.readiness_score < policy.min_readiness_score:
        reasons.append("readiness_below_threshold")
    if len(candidate.story_ids) < policy.min_stories:
        reasons.append("insufficient_story_evidence")
    if policy.require_actionable_canonical_type and cluster_canonical_types is not None:
        normalized = {
            value.strip().lower()
            for value in cluster_canonical_types
            if value and value.strip()
        }
        if not normalized.intersection(ACTIONABLE_CANONICAL_TYPES):
            reasons.append("no_actionable_canonical_type")

    passed = not reasons
    details: dict[str, object] = {
        "readiness_score": candidate.readiness_score,
        "story_count": len(candidate.story_ids),
    }
    if cluster_canonical_types is not None:
        details["cluster_canonical_types"] = list(cluster_canonical_types)
    return PromotionGateResult(
        passed=passed,
        reasons=tuple(reasons),
        details=details,
    )
