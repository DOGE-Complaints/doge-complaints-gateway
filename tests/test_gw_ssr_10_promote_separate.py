"""GW-SSR-10 T02: civic and pack promote stay separate candidates."""

from __future__ import annotations

from pathlib import Path

from core.promotion.gates import PromotionGatePolicy

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
ORCH = GATEWAY_ROOT / "src/core/application/cluster_orchestrator.py"
FACTORY = GATEWAY_ROOT / "src/core/infrastructure/service_factory.py"
GATES = GATEWAY_ROOT / "src/core/promotion/gates.py"


def test_pack_promote_does_not_use_civic_readiness_or_create() -> None:
    text = ORCH.read_text(encoding="utf-8")
    promote_start = text.index("def _promote_pack_membership")
    next_fn = text.index("\n    def process_story")
    pack_fn = text[promote_start:next_fn]
    assert "readiness_score_for_cluster" not in pack_fn
    assert "_create_issue_for_cluster" not in pack_fn
    assert "gate_policy=gate_policy" in pack_fn
    assert "_pack_readiness_score" in pack_fn


def test_dual_civic_uses_civic_create_not_pack_score() -> None:
    text = ORCH.read_text(encoding="utf-8")
    start = text.index("def _process_dual_civic_membership")
    end = text.index("\n    def _process_bound_story")
    civic_fn = text[start:end]
    assert "_create_issue_for_cluster" in civic_fn
    assert "_pack_readiness_score" not in civic_fn
    assert "_promote_pack_membership" not in civic_fn


def test_civic_factory_and_default_type_gate_untouched() -> None:
    factory = FACTORY.read_text(encoding="utf-8")
    start = factory.index("def get_issue_promotion_service")
    end = factory.index("\n    def get_issue_projection_service")
    block = factory[start:end]
    assert "PromotionGatePolicy(" in block
    assert "min_readiness_score=self.config.cluster_readiness_threshold" in block
    assert "min_stories=self.config.cluster_min_size" in block
    assert "require_actionable_canonical_type" not in block
    gates = GATES.read_text(encoding="utf-8")
    assert "require_actionable_canonical_type: bool = True" in gates
    policy = PromotionGatePolicy()
    assert policy.require_actionable_canonical_type is True
