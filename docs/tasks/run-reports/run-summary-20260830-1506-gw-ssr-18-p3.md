# run-summary — GW-SSR-18 P3 Execute

- **Date:** 2026-08-30T15:06:33Z
- **Package:** pkg-000075-20260830-gw-ssr-18-cluster-active-schema.yaml
- **Story:** STORY-GW-SSR-18 cluster active schema
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000075-20260830-gw-ssr-18-cluster-active-schema.yaml
- **Result:** PASS (T01–T05 Done; story gate G18 PASS)

## G18 (runbook §6.3)

Pack/dual iff persist == `NODE_SCHEMA_*`. Mismatch bound → skip + `cluster.skipped_schema_mismatch`, no foreign pack membership. Unbound READY_FOR_PROFILE civic as-is. Dual from **active** `pack.json`. Manual: warehouse vs env; intake 4xx; cluster from server. Smoke binding = env. `ClusterLens` = 10. No `GET /schema-active`. Full offline **767 passed**.

## Queue executed

T01 pack iff active pair → T02 civic unbound legacy → T03 tests → T04 docs warehouse vs env → T05 story acceptance gate.

## Live verification

```text
ok 5 paths (project=gateway, pkg …/pkg-000075-…)
utc_now: 2026-08-30T15:06:33Z
G18 pytest -q -m "not live_integration" tests/test_gw_ssr_18_*.py + test_clustering_engine.py
  → green
full offline GATEWAY_URL= .venv/bin/python -m pytest -q -m "not live_integration"
  → 767 passed, 18 skipped, 10 deselected
rg class ClusterLens -A 14 src/core/cluster/types.py → 10 members
rg «клиент выбирает любой pack|решает тело intake» → empty
rg NODE_SCHEMA_ID|NODE_SCHEMA_VERSION manual → present
rg story_dimensions|/schema-filter|schema-active asgi_app.py → empty
git diff --name-only → GPT UI files: no
ok date-check (after this summary)
```

## Product claims (code)

- Match/skip: `src/core/application/cluster_orchestrator.py` `_matches_active_node_schema` + `_skip_schema_mismatch` + `process_story` `:303–307` / `process_all_pending`
- Dual: `dual_civic_lenses_for_ref` on env pair — `src/core/schema/pack_engine.py`; orchestrator `_dual_civic_enabled`
- Factory: `src/core/infrastructure/service_factory.py` passes `node_schema_id`/`version`
- Civic unbound: `_civic_ready` `:89–91`
- Intake env fallback (test isolation): `src/core/application/services.py` `_active_schema_pair` reads `NODE_SCHEMA_*` before `load_config_from_env`
- Tests: `tests/test_gw_ssr_18_cluster_active_schema.py`
- Docs: `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md`; `docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md`
- Not touched: ClusterLens still 10; no `GET /schema-active`; no SSR-06/07/12; no new SQL; no GPT UI; no bullrun §«Актуальная точка»; pkg-000075 YAML immutable; pie T-wave no

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-06/07/12. Optional P8 commits when asked.
