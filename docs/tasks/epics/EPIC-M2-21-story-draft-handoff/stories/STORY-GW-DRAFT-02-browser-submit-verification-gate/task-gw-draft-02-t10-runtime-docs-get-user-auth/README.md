# task-gw-draft-02-t10-runtime-docs-get-user-auth

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000044)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_02_audit_followup`)
- **Depends on:** T09
- **Audit ref:** [`audit-gw-draft-02-browser-submit-verification-gate-2026-07-03`](../../../../../../analysis/audit-gw-draft-02-browser-submit-verification-gate-2026-07-03.md) **G1**

## Purpose
Runtime-docs delta для GET user-auth: убрать «stub until GW-DRAFT-02»; задокументировать различие GET (session) vs submit (session + `phone_verified`).

## Code Facts
- GET stub note — [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md) §6.8 (`user-auth stub`)
- OpenAPI GET — [`openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml) `/story-drafts/{draft_id}` (no security on GET today)
- Security env §4.1 — [`security-env-api-access.md`](../../../../../../../runtime-docs/security-env-api-access.md) (submit path documented; GET read path TBD)

## Acceptance / DoD
- `API_REFERENCE.md` §6.8 GET: browser Bearer, `/me` active session, codes 401/503/200/404; **no** 403 on GET
- `openapi.yaml` GET: `security: BearerAuth`, responses 401/503
- `security-env-api-access.md` §4.1: GET (session) vs POST submit (session + verify)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/security-env-api-access.md`](../../../../../../../runtime-docs/security-env-api-access.md)

## Out of scope
Production code (T08); tests (T09); story gate re-sign (optional note in T07 gate post-P6)

## Verification commands
```bash
rg 'story-drafts/\{draft_id\}' doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml
rg 'GET /story-drafts' doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md
```
