"""GW-SSR-19: node_clustering.civic loader contract; ClusterLens stays 10."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.cluster import ClusterLens
from core.schema import SchemaRef, UnsupportedVersionError
from core.schema.resolver import resolve_pack
from tests.test_gw_ssr_04_schema_driven_cluster_lens import CLUSTERLENS_BASELINE

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

_ENVSPEC_ACTIVE = (
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
_ENVSPEC_BY_LENS = {
    "composite_primary_micro": 8,
    "service_object_micro": 3,
    "deep_need_local": 3,
    "ecosystem_signal_systemic": 3,
}


def _copy_legal(tmp_path: Path) -> Path:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    return dest


def test_clusterlens_still_ten_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10


def test_example_packs_load_civic_from_envspec_defaults() -> None:
    tallinn = resolve_pack(SchemaRef("tallinn_civic", "v1"), packs_root=PACKS_ROOT)
    legal = resolve_pack(SchemaRef("legal_process", "v1"), packs_root=PACKS_ROOT)
    mobility = resolve_pack(SchemaRef("mobility_observation", "v1"), packs_root=PACKS_ROOT)
    for ctx in (tallinn, legal, mobility):
        civic = ctx.node_clustering.civic
        assert civic.active_lenses == _ENVSPEC_ACTIVE
        assert civic.primary_lens == "composite_primary_micro"
        assert civic.min_size == 5
        assert dict(civic.min_size_by_lens) == _ENVSPEC_BY_LENS
        assert civic.readiness_threshold == 60
        assert civic.signal_source == "canonical"
        assert civic.id_algorithm == "sha256"
        assert civic.geo_filter == "country"
        assert civic.tie_breaker == "alpha"
        assert civic.type_resolution == "canonical_priority"
    assert tallinn.node_clustering.civic.geo_scope == ("settlement", "tallinn")
    assert legal.node_clustering.civic.geo_scope is None
    assert mobility.node_clustering.civic.geo_scope is None
    tallinn_json = json.loads(
        (PACKS_ROOT / "tallinn_civic" / "v1" / "pack.json").read_text(encoding="utf-8")
    )
    assert tallinn_json["node_clustering"]["civic"]["geo_scope"] == "settlement:tallinn"


def test_missing_node_clustering_is_loader_error(tmp_path: Path) -> None:
    dest = _copy_legal(tmp_path)
    manifest = json.loads((PACKS_ROOT / "legal_process" / "v1" / "pack.json").read_text())
    del manifest["node_clustering"]
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="node_clustering"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_invalid_primary_is_loader_error(tmp_path: Path) -> None:
    dest = _copy_legal(tmp_path)
    manifest = json.loads((PACKS_ROOT / "legal_process" / "v1" / "pack.json").read_text())
    manifest["node_clustering"]["civic"]["primary_lens"] = "not_a_lens"
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="primary_lens"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)


def test_primary_not_in_active_is_loader_error(tmp_path: Path) -> None:
    dest = _copy_legal(tmp_path)
    manifest = json.loads((PACKS_ROOT / "legal_process" / "v1" / "pack.json").read_text())
    civic = manifest["node_clustering"]["civic"]
    civic["active_lenses"] = [
        lens for lens in civic["active_lenses"] if lens != "composite_primary_micro"
    ]
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError, match="active_lenses"):
        resolve_pack(SchemaRef("legal_process", "v1"), packs_root=tmp_path)
