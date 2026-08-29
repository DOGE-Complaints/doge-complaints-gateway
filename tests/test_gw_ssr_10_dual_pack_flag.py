"""GW-SSR-10 T00: pack dual_civic_lenses flag; default exact-only."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.cluster import ClusterLens
from core.schema import LocalSchemaRuntime, SchemaRef, UnsupportedVersionError
from core.schema.resolver import resolve_pack

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

CLUSTERLENS_BASELINE = (
    "composite_primary_micro",
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "desired_outcome_local",
    "affected_group_local",
    "geographic_district_micro",
    "service_object_micro",
    "deep_need_local",
    "ecosystem_signal_systemic",
)


def test_clusterlens_still_ten() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10
    assert "police_station" not in {member.value for member in ClusterLens}


def test_legal_process_absent_dual_key_is_exact_only() -> None:
    manifest = json.loads((PACKS_ROOT / "legal_process" / "v1" / "pack.json").read_text())
    assert "dual_civic_lenses" not in manifest
    ctx = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    assert ctx.dual_civic_lenses is False


def test_tallinn_civic_absent_dual_key_is_exact_only() -> None:
    manifest = json.loads((PACKS_ROOT / "tallinn_civic" / "v1" / "pack.json").read_text())
    assert "dual_civic_lenses" not in manifest
    ctx = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    assert ctx.dual_civic_lenses is False


def test_explicit_false_is_exact_only(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["dual_civic_lenses"] = False
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    ctx = LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
    assert ctx.dual_civic_lenses is False


def test_explicit_true_opts_in(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["dual_civic_lenses"] = True
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    ctx = LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
    assert ctx.dual_civic_lenses is True


def test_non_boolean_dual_key_rejected(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["dual_civic_lenses"] = "yes"
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError):
        LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
