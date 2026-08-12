# Acceptance — TASK-GW-GAUTH-01-T03

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Подача без сервисного слоя — отклоняется (не no-op) | PASS | `build_service_auth_from_env()` → `mandatory_channel()` when env unset; `require(..., mandatory=True)` on public writes |
| Service enforced before handler | PASS | FastAPI `dependencies=` on routes; handlers `_require_service_auth` uses `mandatory=False` for ops routes only |
| Policy documented (demo vs pilot) | PASS | [`schema.py`](../../../../../../../src/core/config/schema.py) `SERVICE_API_TOKEN` description + pilot fail-fast L463–466 |
