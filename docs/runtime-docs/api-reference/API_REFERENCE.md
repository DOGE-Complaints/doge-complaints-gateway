# DOGE Complaints Gateway API Reference

## 1. Overview

This reference describes the runtime API surface for `doge-complaints-gateway` with explicit state separation:

- **As-is**: behavior implemented in `FastAPI` transport routes (`src/core/api/asgi_app.py`) backed by handler functions.
- **Planned**: extended endpoint surfaces not yet wired in the runtime transport layer.

The canonical machine-readable contract is:

- `docs/runtime-docs/api-reference/openapi.yaml`

## 2. Runtime Boundary

Current runtime is **ASGI/FastAPI-driven** under `src/core/api/asgi_app.py`.

This means:

1. Operational behaviors (`health`, `ready`, `protected`, `metrics`) are implemented and routable over HTTP.
2. Public/protected policy is declared in route definitions and validated by transport smoke tests.

## 3. Authentication Model

### As-is

Service-to-service authentication is implemented via:

- `Authorization: Bearer <SERVICE_API_TOKEN>`
- `X-Service-Token: <SERVICE_API_TOKEN>`

Implementation sources:

- `src/core/api/security.py`
- `src/core/api/asgi_app.py` (route dependency policy)
- `src/core/api/handlers.py` (defense-in-depth auth checks)

If `SERVICE_API_TOKEN` is unset, auth is disabled by design in demo runtime mode.
For pilot profile, config loading now fails fast when `SERVICE_API_TOKEN` is missing.

### Planned

- Formal key lifecycle policy (rotation/revocation/audit procedures).
- Optional multi-key/keyset strategy for higher-assurance environments.

## 4. Envelope and Error Contract

All operations are expected to return a unified envelope:

- Success: `{ "data": { ... }, "trace_id": "..." }`
- Error: `{ "error": { code, type, message, details }, "trace_id": "..." }`

Error mapping is implemented in:

- `src/core/api/envelope.py`

Validated in:

- `tests/test_error_envelope_contract.py`
- `tests/test_trace_propagation.py`

## 5. Ops Endpoints (as-is behavior, active HTTP binding)

### `GET /health`

- **As-is implementation**: `GET /health` in `asgi_app` -> `handle_health`
- **Purpose**: liveness status from `HealthService`
- **Success example**:

```json
{
  "data": {
    "status": "ok"
  },
  "trace_id": "trace-health-1"
}
```

### `GET /ready`

- **As-is implementation**: `GET /ready` in `asgi_app` -> `handle_readiness`
- **Purpose**: readiness signal for runtime checks
- **Success example**:

```json
{
  "data": {
    "status": "ready"
  },
  "trace_id": "trace-ready-1"
}
```

### `GET /protected/status`

- **As-is implementation**: `GET /protected/status` in `asgi_app` -> `handle_protected_status`
- **Purpose**: verify service-token gate behavior
- **Auth required**: Bearer token or `X-Service-Token` when auth is enabled
- **Unauthorized example**:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "type": "auth",
    "message": "Missing service API token.",
    "details": {}
  },
  "trace_id": "trace-protected-err-1"
}
```

### `GET /metrics`

- **As-is implementation**: `GET /metrics` in `asgi_app` -> `handle_metrics`
- **Purpose**: in-process counters (`health_requests`, `readiness_requests`, `protected_requests`, `metrics_requests`, `auth_failures`)
- **Auth required**: Bearer token or `X-Service-Token` when auth is enabled

## 6. Intake Endpoint (planned HTTP binding, existing contract)

### `POST /intake/stories`

- **Contract exists**: `src/core/intake/contracts.py`
- **HTTP binding state**: planned (not currently implemented in `src/core/api/handlers.py`)
- **Schema version**: `m2.story_intake_envelope.v1`
- **Submitter identity fields**:
  - `submitter.external_user_id` (required, non-empty string)
  - `submitter.identity_issuer` (optional string)

The response contract is envelope-based with payload schema version:

- `m2.story_intake_response.v1`

### Identity linkage for stories (as-is data path)

The runtime data path for submitter identity is already implemented in core logic:

1. Intake parser validates `submitter.external_user_id` in `parse_story_intake_request`.
2. `StoryIntakeService.create_story` maps submitter data to `StoryRecord`.
3. `StoryRecord` persists:
   - `submitter_external_user_id`
   - `submitter_identity_issuer`

Code sources:

- `src/core/intake/contracts.py`
- `src/core/application/services.py`
- `src/core/domain/contracts.py`

Test evidence:

- `tests/test_story_intake_contract.py`
- `tests/test_story_repository_lifecycle.py`
- `tests/test_story_intake_idempotency.py`

## 7. Observability Notes

- `trace_id` is preserved or generated in API envelopes (`ensure_trace_id`).
- Auth failure metrics are exposed via `ApiMetrics` and can be checked by `alert_contract`.

Sources:

- `src/core/api/envelope.py`
- `src/core/api/metrics.py`
- `tests/test_api_security_and_ops.py`
- `tests/test_trace_propagation.py`

## 8. As-is vs Planned Summary

### As-is

- FastAPI/ASGI runtime entrypoint and routable HTTP operations.
- Envelope/error/trace consistency.
- Service-token gate on protected operations:
  - `GET /protected/status`
  - `GET /metrics`
- Public operations:
  - `GET /health`
  - `GET /ready`

### Planned

- Full intake HTTP handler wiring.
- Extended API surface for downstream domain modules.
- Fully enforced server auth for protected business operations:
  - route-level centralized auth enforcement on all future protected endpoints,
  - pilot/production-like fail-fast when `SERVICE_API_TOKEN` is missing,
  - explicit public/protected operation map in API docs and tests.

## 9. Compatibility Guidance

For integrators:

1. Treat `openapi.yaml` as the normative reference format.
2. Read operation descriptions for runtime-state markers (`as-is` vs `planned`).
3. Assume only endpoints listed in section 5 are routable today; other endpoints remain planned.
