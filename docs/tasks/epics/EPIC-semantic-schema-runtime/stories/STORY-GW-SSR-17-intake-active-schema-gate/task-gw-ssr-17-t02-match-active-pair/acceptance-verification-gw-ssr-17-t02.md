# acceptance-verification — GW-SSR-17 t02

- **Result:** PASS
- **Date:** 2026-08-30T14:45:34Z
- **Package:** pkg-000074

## Evidence

`create_story`: `binding is None` → 4xx; pair ≠ `NODE_SCHEMA_*` → `IntakeValidationError` with match message — `src/core/application/services.py:249–260`. Active pair from service fields or `load_config_from_env()` — `:108–114`. Factory passes `AppConfig` pair — `src/core/infrastructure/service_factory.py:86–87`. Persist uses client pair after match (`bound_schema_id = binding.schema_id`) — `services.py:274–275`. HTTP 400 — `handlers.py` submit/stash.
