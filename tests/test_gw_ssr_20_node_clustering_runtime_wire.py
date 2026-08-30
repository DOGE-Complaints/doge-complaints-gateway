"""GW-SSR-20: civic clustering runtime from active pack; semantic CLUSTER_* gone."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.cluster import ClusterLens
from core.config import ConfigError, ENV_SCHEMA, load_config_from_env
from core.config.schema import civic_clustering_from_active_node
from core.infrastructure.providers import provide_app_config, provide_service_factory
from core.promotion.gates import PromotionGatePolicy
from gw_ssr_16_node_schema import with_node_schema
from tests.test_gw_ssr_04_schema_driven_cluster_lens import CLUSTERLENS_BASELINE

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def test_clusterlens_still_ten_members() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    assert len(ClusterLens) == 10


def test_semantic_cluster_env_not_in_appconfig_or_schema() -> None:
    names = {spec.name for spec in ENV_SCHEMA}
    semantic = {
        "CLUSTER_MIN_SIZE",
        "CLUSTER_MIN_SIZE_BY_LENS",
        "CLUSTER_READINESS_THRESHOLD",
        "CLUSTER_ACTIVE_LENSES",
        "CLUSTER_PRIMARY_LENS",
        "CLUSTER_SIGNAL_SOURCE",
        "CLUSTER_ID_ALGORITHM",
        "CLUSTER_GEO_FILTER",
        "CLUSTER_GEO_SCOPE",
        "CLUSTER_TIE_BREAKER",
        "CLUSTER_TYPE_RESOLUTION",
    }
    assert names.isdisjoint(semantic)
    assert "CLUSTER_CRON_ENABLED" in names
    assert "CLUSTER_CRON_INTERVAL_S" in names
    assert "NODE_SCHEMA_ID" in names
    assert "NODE_SCHEMA_VERSION" in names
    config = load_config_from_env(
        with_node_schema(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_MIN_SIZE": "1",
            }
        )
    )
    assert not hasattr(config, "cluster_min_size")
    assert config.cluster_cron_enabled is True


def test_factory_civic_engine_and_gate_from_active_pack() -> None:
    config = provide_app_config(
        with_node_schema(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_MIN_SIZE": "99",
            }
        )
    )
    civic = civic_clustering_from_active_node(
        schema_id=config.node_schema_id,
        schema_version=config.node_schema_version,
    )
    factory = provide_service_factory(config)
    engine = factory.get_clustering_engine()
    assert tuple(lens.value for lens in engine.active_lenses) == civic.active_lenses
    assert engine.primary_lens is not None
    assert engine.primary_lens.value == civic.primary_lens
    assert engine.geo_filter == civic.geo_filter
    orchestrator = factory.get_story_cluster_orchestrator()
    assert orchestrator.default_cluster_min_size == civic.min_size
    assert orchestrator.cluster_min_size_by_lens["composite_primary_micro"] == 8
    gate = factory.get_issue_promotion_service().gate_policy
    assert gate.min_readiness_score == civic.readiness_threshold
    assert gate.min_stories == civic.min_size
    assert gate.require_actionable_canonical_type is True
    default_policy = PromotionGatePolicy()
    assert default_policy.require_actionable_canonical_type is True


def test_missing_node_clustering_on_active_pack_is_config_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dest = tmp_path / "broken_civic" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text(encoding="utf-8"))
    manifest["schema_id"] = "broken_civic"
    del manifest["node_clustering"]
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setenv("SCHEMA_PACKS_ROOT", str(tmp_path))
    with pytest.raises(ConfigError, match="pack catalog|node_clustering"):
        load_config_from_env(
            with_node_schema(
                {
                    "APP_PROFILE": "demo",
                    "API_BASE_URL": "https://demo.example/api",
                    "NODE_SCHEMA_ID": "broken_civic",
                    "NODE_SCHEMA_VERSION": "v1",
                }
            )
        )


def test_handlers_geo_scope_from_tallinn_pack() -> None:
    civic = civic_clustering_from_active_node(
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    assert civic.geo_scope == ("settlement", "tallinn")
