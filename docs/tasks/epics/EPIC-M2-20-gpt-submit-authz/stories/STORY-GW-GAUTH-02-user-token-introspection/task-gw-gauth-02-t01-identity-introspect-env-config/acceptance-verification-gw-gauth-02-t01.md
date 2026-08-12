# Acceptance — TASK-GW-GAUTH-02-T01

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Gateway предъявляет identity свой сервисный токен | PASS | `IDENTITY_SERVICE_TOKEN` EnvSpec + `AppConfig.identity_service_token` in [`schema.py`](../../../../../../../src/core/config/schema.py); wired via [`build_identity_introspection_from_config`](../../../../../../../src/core/identity/introspection_client.py) |
| `IDENTITY_INTROSPECT_URL` base URL config | PASS | `IDENTITY_INTROSPECT_URL` EnvSpec + HTTP validation; paired env cross-check |

**Verification:**
```
rg 'IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN' src/core/config/schema.py
```
