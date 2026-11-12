# acceptance-verification — GW-SSR-16 t02

- **Result:** PASS
- **Date:** 2026-08-30T14:24:58Z
- **Package:** pkg-000073

## Evidence

`load_config_from_env` calls `_resolve_node_schema_pack` → `resolve_pack(SchemaRef)`. Unknown id / missing version dir → `ConfigError`. `tallinn_civic`/`v1` loads. Resolver `SCHEMA_PACKS_ROOT` unchanged.
