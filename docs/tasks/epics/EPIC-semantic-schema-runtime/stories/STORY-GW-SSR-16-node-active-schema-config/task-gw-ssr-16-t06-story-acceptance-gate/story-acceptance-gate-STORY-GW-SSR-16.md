# Story acceptance gate — STORY-GW-SSR-16

- **Story:** Node active schema (config + boot)
- **Package:** `pkg-000073-20260830-gw-ssr-16-node-active-schema-config.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T14:24:58Z

## G16 (runbook §6.1)

| G16 check | Result | Evidence |
|-----------|--------|----------|
| pytest `test_gw_ssr_16_*` зелёный | PASS | 8 passed (`tests/test_gw_ssr_16_node_active_schema.py`) |
| missing env → `ConfigError`; existing pack loads; unknown id / missing dir → fail-fast | PASS | same file: missing/empty/unknown/`v9-missing` + `tallinn_civic`/`v1` |
| оба поля required в `AppConfig` / `ENV_SCHEMA` | PASS | `schema.py` EnvSpec `NODE_SCHEMA_ID`/`NODE_SCHEMA_VERSION`; `test_env_specs_both_required_no_default` |
| `ClusterLens` members **ровно** baseline (10) | PASS | `types.py:10–22` |
| нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions` | PASS | `rg` asgi empty |
| `SCHEMA_PACKS_ROOT` не в AppConfig | PASS | `rg SCHEMA_PACKS_ROOT src/core/config/schema.py` empty |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `NODE_SCHEMA_ID` и `NODE_SCHEMA_VERSION` в AppConfig; оба required. | PASS | `schema.py` AppConfig + ENV_SCHEMA; G16 rg |
| Нет пары / нет каталога pack → процесс не стартует (`ConfigError`). | PASS | `_require_value` + `_resolve_node_schema_pack`; T05 tests |
| Каталог на диске резолвится (пример `tallinn_civic` / `v1`). | PASS | `test_existing_pack_loads` |
| Lifespan логирует активную пару. | PASS | `asgi_app.py` `_lifespan`; `test_lifespan_logs_active_pair` |
| `SCHEMA_PACKS_ROOT` не перенесён в AppConfig в этой стори. | PASS | `schema.py` rg empty; resolver `_ENV_PACKS_ROOT` |

## Commands (live verification 2026-08-30T14:24:58Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_16_*.py
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
