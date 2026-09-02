"""GW-SSR-30: tallinn MVP card_fields load + project_card_fields smoke."""

from __future__ import annotations

from pathlib import Path

from core.cluster.types import ClusterLens
from core.projection.card_fields import project_card_fields
from core.schema import SchemaRef
from core.schema.resolver import resolve_pack

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

MVP_CARD_FIELDS = (
    "signals.desired_outcome",
    "signals.affected_group",
    "signals.service_object",
)


def test_tallinn_resolve_pack_mvp_card_fields() -> None:
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert ctx.card_fields == MVP_CARD_FIELDS
    for path in MVP_CARD_FIELDS:
        assert ctx.field_policy.get(path) not in {"forbidden", "node_private"}
        assert path in ctx.field_policy


def test_tallinn_project_card_fields_smoke() -> None:
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    payload = {
        "signals": {
            "desired_outcome": "fix_lighting",
            "affected_group": "residents",
            "service_object": "street_lamp",
            "civic_domain": "infra",
        }
    }
    card = project_card_fields(payload, ctx.card_fields, ctx.field_policy)
    assert card == {
        "signals.desired_outcome": "fix_lighting",
        "signals.affected_group": "residents",
        "signals.service_object": "street_lamp",
    }
    assert "signals.civic_domain" not in card


def test_cluster_lens_enum_still_ten() -> None:
    assert len(ClusterLens) == 10


def test_legal_and_mobility_remain_without_card_fields() -> None:
    for pack_id in ("legal_process", "mobility_observation"):
        ctx = resolve_pack(SchemaRef(pack_id, "v1"), packs_root=PACKS_ROOT)
        assert ctx.card_fields == ()
