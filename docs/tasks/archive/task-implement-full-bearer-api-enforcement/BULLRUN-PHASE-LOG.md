# BULLRUN PHASE LOG — TASK-AUTH-01

## Phase 0 — Analysis

- Verified current auth flow and API surface in:
  - `src/core/api/security.py`
  - `src/core/api/handlers.py`
  - `src/core/config/schema.py`
- Confirmed gap: no strict pilot fail-fast on missing `SERVICE_API_TOKEN`; no unified auth helper for protected ops.

## Phase 1 — Implementation

- Added pilot strict auth guard in `load_config_from_env`:
  - for `APP_PROFILE=pilot`, missing `SERVICE_API_TOKEN` raises `ConfigError`.
- Added `SERVICE_API_TOKEN` to `ENV_SCHEMA`.
- Introduced unified auth helper in API handlers:
  - `_require_service_auth(...)` in `src/core/api/handlers.py`.
- Applied auth gate to protected metrics operation:
  - `handle_metrics(..., headers=...)` now enforces service auth like `handle_protected_status`.

## Phase 2 — Tests

- Extended tests in `tests/test_api_security_and_ops.py`:
  - metrics reject without token when auth enabled;
  - metrics accept with valid bearer token.
- Updated config tests in `tests/test_config_loading.py` for pilot strict auth mode.
- Verification run:
  - `python3 -m pytest tests/test_api_security_and_ops.py tests/test_config_loading.py tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q`
  - Result: `31 passed`.

## Phase 3 — Documentation sync

- Updated runtime docs:
  - `docs/runtime-docs/security-env-api-access.md`
  - `docs/runtime-docs/api-reference/API_REFERENCE.md`
  - `docs/runtime-docs/api-reference/openapi.yaml`
- Synced protected/public operation split and pilot strict auth behavior.
