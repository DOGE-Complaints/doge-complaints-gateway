"""Map schema-pack ReadinessPolicy knobs onto PromotionGatePolicy (SSR-05)."""

from __future__ import annotations

from core.promotion.gates import PromotionGatePolicy
from core.schema.contracts import ReadinessPolicy


def promotion_gate_policy_from_pack(policy: ReadinessPolicy) -> PromotionGatePolicy:
    """Copy the three pack-file knobs onto a per-call PromotionGatePolicy.

    Numbers and the actionable-type flag come from the pack file, not civic
    defaults (70/2/True). Does not invent a fourth knob.
    """
    return PromotionGatePolicy(
        min_readiness_score=policy.min_readiness_score,
        min_stories=policy.min_stories,
        require_actionable_canonical_type=policy.require_actionable_canonical_type,
    )
