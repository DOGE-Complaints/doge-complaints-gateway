"""GW-SSR-26: taxonomy.json pack contract + loader (optional Contour2)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.cluster.types import ClusterLens
from core.schema import SchemaRef, UnsupportedVersionError
from core.schema.contracts import TaxonomyPack
from core.schema.resolver import resolve_pack
from core.taxonomy.axes import TAXONOMY_AXIS_VALUES

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

_AXES_ORDERED = tuple(sorted(TAXONOMY_AXIS_VALUES))


def _minimal_taxonomy(
    *,
    schema_id: str,
    schema_version: str = "v1",
    axes: tuple[str, ...] | None = None,
    extra_canonical: dict[str, list[dict[str, str]]] | None = None,
) -> dict:
    body: dict = {
        "schema_id": schema_id,
        "schema_version": schema_version,
        "axes": list(axes if axes is not None else _AXES_ORDERED),
        "internal_axes": ["risk_privacy_safety", "confidence_state"],
        "canonical_keys": {},
        "axis_to_signal_map": {"topic_domain": "signals.civic_domain"},
        "dispositions": [
            "canonical",
            "metadata_only",
            "needs_clarification",
            "rejected",
            "internal",
        ],
    }
    if extra_canonical:
        body["canonical_keys"] = extra_canonical
    return body


def _copy_legal_pack(dest: Path, *, taxonomy_schema: str | None = None) -> Path:
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    if taxonomy_schema is not None:
        manifest["taxonomy_schema"] = taxonomy_schema
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    return dest


def test_clusterlens_baseline_unchanged() -> None:
    assert len(ClusterLens) == 10


def test_legal_and_mobility_load_without_taxonomy() -> None:
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    mobility = resolve_pack(
        SchemaRef("mobility_observation", "v1"), packs_root=PACKS_ROOT
    )
    assert legal.taxonomy is None
    assert mobility.taxonomy is None
    # Orphan on-disk file without taxonomy_schema must not auto-load (tallinn).
    tallinn_manifest = json.loads(
        (PACKS_ROOT / "tallinn_civic" / "v1" / "pack.json").read_text(encoding="utf-8")
    )
    assert "taxonomy_schema" not in tallinn_manifest
    assert (PACKS_ROOT / "tallinn_civic" / "v1" / "taxonomy.json").is_file()
    tallinn = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert tallinn.taxonomy is None


def test_missing_taxonomy_file_when_declared_fails(tmp_path: Path) -> None:
    dest = _copy_legal_pack(
        tmp_path / "legal_process" / "v1", taxonomy_schema="taxonomy.json"
    )
    assert not (dest / "taxonomy.json").exists()
    with pytest.raises(UnsupportedVersionError, match="taxonomy file missing"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_invalid_axis_in_taxonomy_file_fails(tmp_path: Path) -> None:
    dest = _copy_legal_pack(
        tmp_path / "legal_process" / "v1", taxonomy_schema="taxonomy.json"
    )
    bad_axes = tuple(a for a in _AXES_ORDERED if a != "topic_domain") + (
        "not_a_real_axis",
    )
    (dest / "taxonomy.json").write_text(
        json.dumps(
            _minimal_taxonomy(schema_id="legal_process", axes=bad_axes)
        ),
        encoding="utf-8",
    )
    with pytest.raises(UnsupportedVersionError, match="unknown axis"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_duplicate_canonical_key_fails(tmp_path: Path) -> None:
    dest = _copy_legal_pack(
        tmp_path / "legal_process" / "v1", taxonomy_schema="taxonomy.json"
    )
    body = _minimal_taxonomy(
        schema_id="legal_process",
        extra_canonical={
            "governance_signal": [
                {"key": "dup_signal", "meaning": "one"},
                {"key": "dup_signal", "meaning": "two"},
            ]
        },
    )
    (dest / "taxonomy.json").write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="duplicate key"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_declared_taxonomy_loads_when_valid(tmp_path: Path) -> None:
    dest = _copy_legal_pack(
        tmp_path / "legal_process" / "v1", taxonomy_schema="taxonomy.json"
    )
    (dest / "taxonomy.json").write_text(
        json.dumps(_minimal_taxonomy(schema_id="legal_process")),
        encoding="utf-8",
    )
    ctx = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)
    assert isinstance(ctx.taxonomy, TaxonomyPack)
    assert ctx.taxonomy.schema_id == "legal_process"
    assert set(ctx.taxonomy.axes) == TAXONOMY_AXIS_VALUES
    assert ctx.taxonomy.axis_to_signal_map["topic_domain"] == "signals.civic_domain"
