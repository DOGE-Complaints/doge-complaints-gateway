# run-summary — GW-SSR-16 P3 Execute

- **Date:** 2026-08-30T14:24:58Z
- **Package:** pkg-000073-20260830-gw-ssr-16-node-active-schema-config.yaml
- **Story:** STORY-GW-SSR-16 node active schema config
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000073-20260830-gw-ssr-16-node-active-schema-config.yaml
- **Result:** PASS (T01–T06 Done; story gate G16 PASS)

## G16 (runbook §6.1)

`NODE_SCHEMA_ID` + `NODE_SCHEMA_VERSION` required in AppConfig; boot `resolve_pack`; no `DEFAULT_SCHEMA_PACK`; `SCHEMA_PACKS_ROOT` stays `os.environ` in resolver. Pytest `tests/test_gw_ssr_16_*.py` only (not full suite). No intake gate. No ClusterLens change. No `GET /schema-active`.

## Queue executed

T01 config fields → T02 boot resolve → T03 lifespan log → T04 env docs → T05 tests + helper → T06 story acceptance gate.

## Live verification

```text
ok 6 paths (project=gateway, pkg …/pkg-000073-…)
utc_now: 2026-08-30T14:24:58Z
G16 pytest -q -m "not live_integration" tests/test_gw_ssr_16_*.py
  → 8 passed
rg NODE_SCHEMA_ID|NODE_SCHEMA_VERSION src/core/config/schema.py → EnvSpec + _require_value
rg class ClusterLens -A 14 src/core/cluster/types.py → 10 members
rg story_dimensions|/schema-filter|schema-active src/core/api/asgi_app.py → empty
rg SCHEMA_PACKS_ROOT src/core/config/schema.py → empty
rg DEFAULT_SCHEMA_PACK src → empty
ok date-check (after this summary)
```

## Product claims (code)

- `AppConfig.node_schema_id` / `node_schema_version` — `src/core/config/schema.py` AppConfig + `ENV_SCHEMA` required
- Boot: `_resolve_node_schema_pack` → `resolve_pack(SchemaRef)` wrap `UnknownSchemaError`/`UnsupportedVersionError` → `ConfigError`
- Lifespan: `asgi_app.py` `_lifespan` logs `node_schema_id` / `node_schema_version` on `startup.config`
- Helper: `tests/gw_ssr_16_node_schema.py` + autouse `monkeypatch_node_schema` in `tests/conftest.py`
- Tests: `tests/test_gw_ssr_16_node_active_schema.py`
- Docs: `.env.test.example` two lines; `server-env-quickstart.md` one section
- Not touched: `SCHEMA_PACKS_ROOT` not in AppConfig; ClusterLens still 10; no intake 4xx; no `GET /schema-active`; no SSR-06/07/12; no identity-service; no bullrun §Актуальная точка; pkg-000073 YAML immutable

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-17/06/07/12. Optional P8 commits when asked.
