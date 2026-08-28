"""GW-SSR-05 T01: pack ReadinessPolicy mapper → PromotionGatePolicy."""

from __future__ import annotations

from pathlib import Path

from core.promotion.gates import PromotionGatePolicy
from core.schema import LocalSchemaRuntime, SchemaRef, promotion_gate_policy_from_pack
from core.schema.contracts import ReadinessPolicy

PACKS_ROOT = Path(__file__).resolve().parents[1] / "schema-packs"
GATEWAY_ROOT = Path(__file__).resolve().parents[1]


def test_mapper_copies_three_pack_file_knobs_not_civic_defaults() -> None:
    runtime = LocalSchemaRuntime(packs_root=PACKS_ROOT)
    context = runtime.resolve(SchemaRef("legal_process", "v1"))
    pack_policy = context.exact_lenses[0].readiness_policy
    mapped = promotion_gate_policy_from_pack(pack_policy)
    assert pack_policy.min_readiness_score == 40
    assert pack_policy.min_stories == 3
    assert pack_policy.require_actionable_canonical_type is False
    assert mapped.min_readiness_score == 40
    assert mapped.min_stories == 3
    assert mapped.require_actionable_canonical_type is False
    civic = PromotionGatePolicy()
    assert civic.min_readiness_score == 70
    assert civic.min_stories == 2
    assert civic.require_actionable_canonical_type is True


def test_mapper_does_not_invent_fourth_knob() -> None:
    mapped = promotion_gate_policy_from_pack(
        ReadinessPolicy(
            min_readiness_score=40,
            min_stories=3,
            require_actionable_canonical_type=False,
        )
    )
    assert set(mapped.__dataclass_fields__) == {
        "min_readiness_score",
        "min_stories",
        "require_actionable_canonical_type",
    }


def test_civic_factory_and_default_knob_unchanged() -> None:
    gates = (GATEWAY_ROOT / "src/core/promotion/gates.py").read_text(encoding="utf-8")
    factory = (GATEWAY_ROOT / "src/core/infrastructure/service_factory.py").read_text(
        encoding="utf-8"
    )
    assert "require_actionable_canonical_type: bool = True" in gates
    assert "min_readiness_score: int = 70" in gates
    assert "min_stories: int = 2" in gates
    assert "PromotionGatePolicy(" in factory
    assert "require_actionable_canonical_type=False" not in factory
