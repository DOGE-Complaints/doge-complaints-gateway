# DOGE Complaints Gateway API Reference

## 1. Overview

This reference describes the runtime API surface for `doge-complaints-gateway` with explicit state separation:

- **As-is**: behavior currently implemented in handler functions under `src/core/api/handlers.py`.
- **Planned**: HTTP route bindings and extended endpoint surfaces not yet wired in the runtime transport layer.

The canonical machine-readable contract is:

- `docs/runtime-docs/api-reference/openapi.yaml`

## 2. Runtime Boundary

Current runtime is **handler-driven** and does not include a framework router entrypoint under `src/core`.

This means:

1. Operational behaviors (`health`, `ready`, `protected`, `metrics`) are implemented.
2. HTTP path mapping is documented as a reference binding for integration consistency.

## 3. Authentication Model

### As-is

Service-to-service authentication is implemented via:

- `Authorization: Bearer <SERVICE_API_TOKEN>`
- `X-Service-Token: <SERVICE_API_TOKEN>`

Implementation sources:

- `src/core/api/security.py`
- `src/core/api/handlers.py` (`handle_protected_status`)

If `SERVICE_API_TOKEN` is unset, auth is disabled by design in current runtime mode.

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

## 5. Ops Endpoints (as-is behavior, planned HTTP binding)

### `GET /health`

- **As-is implementation**: `handle_health`
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

- **As-is implementation**: `handle_readiness`
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

- **As-is implementation**: `handle_protected_status`
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

- **As-is implementation**: `handle_metrics`
- **Purpose**: in-process counters (`health_requests`, `readiness_requests`, `protected_requests`, `metrics_requests`, `auth_failures`)

## 6. Intake Endpoint (planned HTTP binding, existing contract)

### `POST /intake/stories`

- **Contract exists**: `src/core/intake/contracts.py`
- **HTTP binding state**: planned (not currently implemented in `src/core/api/handlers.py`)
- **Schema version**: `m2.story_intake_envelope.v1`

The response contract is envelope-based with payload schema version:

- `m2.story_intake_response.v1`

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

- Handler-level operational API behavior.
- Envelope/error/trace consistency.
- Service-token gate with optional strict mode.

### Planned

- First-class HTTP router entrypoint.
- Full intake HTTP handler wiring.
- Extended API surface for downstream domain modules.

## 9. Compatibility Guidance

For integrators:

1. Treat `openapi.yaml` as the normative reference format.
2. Read operation descriptions for runtime-state markers (`as-is` vs `planned`).
3. Do not assume planned endpoints are already routable in runtime transport.
