"""GW-SSR-05 T05: no generic filter HTTP; build_index stays stub; GET /node/issues stays."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.schema import LocalSchemaRuntime, SchemaRef

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"


def test_asgi_has_no_filter_route_and_keeps_tallinn_issues() -> None:
    text = (GATEWAY_ROOT / "src/core/api/asgi_app.py").read_text(encoding="utf-8")
    assert "story_dimensions" not in text
    assert "/schema-filter" not in text
    assert "generic.filter" not in text
    assert '@app.get("/node/issues")' in text


def test_build_index_and_project_remain_stubs() -> None:
    runtime = LocalSchemaRuntime(packs_root=PACKS_ROOT)
    ctx = runtime.resolve(SchemaRef("legal_process", "v1"))
    with pytest.raises(NotImplementedError, match="SSR-06"):
        runtime.build_index(ctx, {"institution": {"office_id": "x"}})
    with pytest.raises(NotImplementedError, match="SSR-07"):
        runtime.project({"institution": {"office_id": "x"}}, SchemaRef("legal_process", "v1"))


def test_clusterlens_baseline_unchanged() -> None:
    from core.cluster import ClusterLens
    from tests.test_gw_ssr_04_schema_driven_cluster_lens import CLUSTERLENS_BASELINE

    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE
    types = (GATEWAY_ROOT / "src/core/cluster/types.py").read_text(encoding="utf-8")
    assert "POLICE_STATION" not in types
    assert "police_station" not in types
