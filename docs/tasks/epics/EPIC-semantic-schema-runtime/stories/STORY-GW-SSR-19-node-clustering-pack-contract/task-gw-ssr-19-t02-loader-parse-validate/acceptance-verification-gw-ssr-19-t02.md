# acceptance-verification — GW-SSR-19 t02

- **Result:** PASS
- **Date:** 2026-08-30T19:21:58Z
- **Package:** pkg-000076

## Evidence

`_parse_civic_clustering` in `src/core/schema/resolver.py`: missing `node_clustering` / invalid primary → `UnsupportedVersionError`. Valid block → `SchemaContext.node_clustering.civic`. No silent default; no env override.
