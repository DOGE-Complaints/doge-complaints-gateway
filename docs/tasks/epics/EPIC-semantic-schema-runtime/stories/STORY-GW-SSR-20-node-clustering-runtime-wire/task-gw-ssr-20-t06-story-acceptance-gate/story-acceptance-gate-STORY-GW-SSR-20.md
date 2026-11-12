# Story acceptance gate — STORY-GW-SSR-20

- **Story:** Node clustering runtime from active pack
- **Package:** `pkg-000077-20260830-gw-ssr-20-node-clustering-runtime-wire.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T19:40:38Z

## G20 (runbook §6.2)

| G20 check | Result | Evidence |
|-----------|--------|----------|
| civic engine / gate / min_size из активного pack | PASS | `service_factory.py` `_active_civic`; `test_factory_civic_engine_and_gate_from_active_pack` |
| семантические CLUSTER_* не в AppConfig / ENV_SCHEMA | PASS | `rg cluster_min_size\|CLUSTER_MIN_SIZE\|CLUSTER_ACTIVE_LENSES src/core/config/schema.py` empty |
| `CLUSTER_CRON_*` на месте | PASS | `schema.py` EnvSpec `CLUSTER_CRON_ENABLED` / `CLUSTER_CRON_INTERVAL_S` |
| missing `node_clustering` → ConfigError | PASS | `test_missing_node_clustering_on_active_pack_is_config_error` |
| pytest 20 + clustering_engine | PASS | **21 passed** (`test_gw_ssr_20_*` + `test_clustering_engine.py`) |
| полный offline pytest | PASS | **776 passed**, 18 skipped, 10 deselected |
| ClusterLens=10 | PASS | `types.py:10–22` |
| нет filter HTTP / `GET /schema-active` | PASS | `rg story_dimensions\|/schema-filter\|schema-active src/core/api/asgi_app.py` empty |
| не `live_integration` как proof | PASS | marker `not live_integration` |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Civic `ClusteringEngine` knobs = `node_clustering.civic` активного pack. | PASS | factory `get_clustering_engine`; leftover `CLUSTER_MIN_SIZE=99` ignored |
| Civic `PromotionGatePolicy` min_readiness / min_stories из pack. | PASS | factory `readiness_threshold` / `min_size`; default type gate True |
| Orchestrator min_size / by_lens из pack. | PASS | `default_cluster_min_size` + `min_size_by_lens` from civic |
| Handlers geo_scope из pack. | PASS | `handlers.py` civic.geo_scope; tallinn `settlement:tallinn` |
| Семантические `CLUSTER_*` не в AppConfig; cron + NODE_SCHEMA остаются. | PASS | AppConfig fields + ENV_SCHEMA; G20 rg |
| Missing `node_clustering` на активном pack → ConfigError при boot/load. | PASS | `civic_clustering_from_active_node` wraps loader error |
| `test_clustering_engine.py` + offline suite зелёные после адаптации фикстур. | PASS | 21 + 776 passed |
| `ClusterLens` = 10. | PASS | `types.py:10–22` |

## Commands (live verification 2026-08-30T19:40:38Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_20_node_clustering_runtime_wire.py
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
.venv/bin/python -m pytest -q -m "not live_integration"
rg -n "cluster_min_size|CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES" src/core/config/schema.py
rg -n "CLUSTER_CRON_ENABLED|CLUSTER_CRON_INTERVAL_S" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
