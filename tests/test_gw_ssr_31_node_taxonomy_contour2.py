"""GW-SSR-31: Contour2 pack-defined axes (≠13) load SUCCESS."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from core.cluster.types import ClusterLens
from core.schema import SchemaRef
from core.schema.contracts import TaxonomyPack
from core.schema.resolver import resolve_pack
from core.taxonomy.axes import TAXONOMY_AXIS_VALUES

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

# uus-shaped stub: 24 node-defined axes (not the tallinn reference 13).
_UUS_SHAPED_AXES = tuple(f"uus_axis_{i:02d}" for i in range(1, 25))


def _copy_legal_pack(dest: Path, *, taxonomy_schema: str) -> Path:
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    manifest["taxonomy_schema"] = taxonomy_schema
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    return dest


def test_clusterlens_enum_still_ten() -> None:
    assert len(ClusterLens) == 10


def test_uus_shaped_twenty_four_axis_taxonomy_loads(tmp_path: Path) -> None:
    assert len(_UUS_SHAPED_AXES) == 24
    assert set(_UUS_SHAPED_AXES) != TAXONOMY_AXIS_VALUES
    dest = _copy_legal_pack(
        tmp_path / "legal_process" / "v1", taxonomy_schema="taxonomy.json"
    )
    body = {
        "schema_id": "legal_process",
        "schema_version": "v1",
        "axes": list(_UUS_SHAPED_AXES),
        "internal_axes": [],
        "canonical_keys": {},
        "axis_to_signal_map": {},
        "dispositions": [
            "canonical",
            "metadata_only",
            "needs_clarification",
            "rejected",
            "internal",
        ],
    }
    (dest / "taxonomy.json").write_text(json.dumps(body), encoding="utf-8")
    ctx = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)
    assert isinstance(ctx.taxonomy, TaxonomyPack)
    assert ctx.taxonomy.axes == _UUS_SHAPED_AXES


def test_legal_and_mobility_remain_without_taxonomy() -> None:
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    mobility = resolve_pack(
        SchemaRef("mobility_observation", "v1"), packs_root=PACKS_ROOT
    )
    assert legal.taxonomy is None
    assert mobility.taxonomy is None


def test_tallinn_official_seed_still_loads() -> None:
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert isinstance(ctx.taxonomy, TaxonomyPack)
    assert set(ctx.taxonomy.axes) == TAXONOMY_AXIS_VALUES
