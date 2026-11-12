# acceptance-verification — GW-SSR-17 t01

- **Result:** PASS
- **Date:** 2026-08-30T14:45:34Z
- **Package:** pkg-000074

## Evidence

`_parse_schema_binding_block` required: `None` / non-mapping / empty `{}` → `IntakeValidationError("Missing or invalid root.schema_binding.")` — `src/core/intake/contracts.py:227–241`. Call site: key absent → same error — `:480–482`. Shared envelope parse (stash + submit).
