# acceptance-verification — GW-SSR-16 t01

- **Result:** PASS
- **Date:** 2026-08-30T14:24:58Z
- **Package:** pkg-000073

## Evidence

`ENV_SCHEMA` + `AppConfig` fields `node_schema_id` / `node_schema_version`. Both `required=True`, `default=None`. Empty strip → `ConfigError` via `_get_value`. No `SCHEMA_PACKS_ROOT` / `DEFAULT_SCHEMA_PACK` on AppConfig.
