# run-summary — GW-SSR-17 P3 Execute

- **Date:** 2026-08-30T14:45:34Z
- **Package:** pkg-000074-20260830-gw-ssr-17-intake-active-schema-gate.yaml
- **Story:** STORY-GW-SSR-17 intake active schema gate
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000074-20260830-gw-ssr-17-intake-active-schema-gate.yaml
- **Result:** PASS (T01–T05 Done; story gate G17 PASS)

## G17 (runbook §6.2)

Absent/`{}`/null binding → `IntakeValidationError` 4xx. Match `NODE_SCHEMA_*` → validate **active** pack (`SchemaRef` env pair). Mismatch id or version → 4xx. Civic HTTP fixtures adapted (binding + env). No silent coerce. No GPT UI in diff. `ClusterLens` = 10. No `GET /schema-active`.

## Queue executed

T01 parse require binding → T02 match active pair → T03 validate active pack → T04 tests + civic fixtures → T05 story acceptance gate.

## Live verification

```text
ok 5 paths (project=gateway, pkg …/pkg-000074-…)
utc_now: 2026-08-30T14:45:34Z
G17 pytest -q -m "not live_integration" tests/test_gw_ssr_17_*.py tests/test_gw_ssr_03_*.py
  → 22 passed
req24 + G17 (adapted civic HTTP) → 45 passed
rg class ClusterLens -A 14 src/core/cluster/types.py → 10 members
rg schema-active|/schema-filter|story_dimensions src/core/api/asgi_app.py → empty
git diff --name-only → GPT UI files: no
ok date-check (after this summary)
```

## Product claims (code)

- Parse required: `src/core/intake/contracts.py` `_parse_schema_binding_block` + absent-key raise
- Match: `src/core/application/services.py` `_active_schema_pair` + pair compare before resolve
- Validate: `SchemaRef(active_id, active_version)` then persist client pair
- Factory: `src/core/infrastructure/service_factory.py` passes AppConfig pair
- Helper: `tests/gw_ssr_16_node_schema.py` `active_node_schema_binding()`
- Tests: `tests/test_gw_ssr_17_intake_active_schema.py`; SSR-03 civic-absent now reject
- Not touched: ClusterLens still 10; no `GET /schema-active`; no SSR-06/07/12/18; no new SQL; no GPT UI; no bullrun §Актуальная точка; pkg-000074 YAML immutable

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-18/06/07/12. Optional P8 commits when asked.
