# task-gw-draft-02-t06-runtime-docs-submit-api

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T05

## Purpose
Runtime-docs дельта: `POST /story-drafts/{id}/submit` (коды 202/403/401/503/404); `IDENTITY_BASE_URL` + браузерный auth-путь.

## Code Facts
- Existing draft docs — [`API_REFERENCE.md §6.8`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- Security env — [`security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md)
- OpenAPI — [`openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)

## Acceptance / DoD
- Traces parent Runtime-docs дельта (backlog)
- `openapi.yaml` + `API_REFERENCE.md` — submit route + response codes
- `security-env-api-access.md` — `IDENTITY_BASE_URL`
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- [`docs/runtime-docs/security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md)

## Out of scope
Product code changes; story gate (T07)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'story-drafts/.*/submit|IDENTITY_BASE_URL' docs/runtime-docs/
```
