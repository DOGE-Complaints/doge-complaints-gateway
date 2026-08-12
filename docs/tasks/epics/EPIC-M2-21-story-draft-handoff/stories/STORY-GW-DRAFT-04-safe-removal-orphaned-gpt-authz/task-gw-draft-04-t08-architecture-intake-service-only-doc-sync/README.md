# task-gw-draft-04-t08-architecture-intake-service-only-doc-sync

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000046)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_04_audit_followup`)
- **Depends on:** T07 (story gate PASS)
- **Audit ref:** [`audit-gw-draft-04-safe-removal-orphaned-gpt-authz-2026-07-03`](../../../../../../analysis/audit-gw-draft-04-safe-removal-orphaned-gpt-authz-2026-07-03.md) **R1**

## Purpose
Закрыть audit **R1**: привести architecture route table к as-built **service-only** на `POST /intake/stories` после GW-DRAFT-04 T04. Убрать устаревшее «service + user (legacy GPT direct)» / «two-token path»; явный pointer: продуктовый user submit → `POST /story-drafts/{id}/submit` (GW-DRAFT-02).

## Code Facts
- As-built route deps — [`asgi_app.py:485,501`](../../../../../../../src/core/api/asgi_app.py) — `[Depends(require_public_content_service_auth)]`; `require_user_token` = 0 in `src/`
- Doc drift — [`architecture-and-layers-as-is.md:50`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md) — «service + user (legacy GPT direct)»
- T06 already aligned — [`simulation-runner-manual.md:50`](../../../../../../../docs/runtime-docs/testing/simulation-runner-manual.md) — service-only after GW-DRAFT-04
- Browser user path unchanged — [`architecture-and-layers-as-is.md:52-53`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md) — `/story-drafts*` Bearer → `/me`

## Acceptance / DoD
- Traces audit R1: `/intake/stories` Access column = service-only (trusted channel), not «service + user»
- Runtime meaning row states legacy seed/simulation path; product submit → story-draft handoff
- No «two-token» / «X-User-Token» on intake row in architecture table
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`docs/runtime-docs/architecture-and-layers-as-is.md`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md) — route table ~L50 and related prose if needed

## Out of scope
- `security-env-api-access.md`, `server-env-quickstart.md` (T09 G1)
- Prod code; pytest
- `/tallinn/issues` row (not in architecture table today; T09 covers security SSOT)

## Verification commands
```bash
rg 'service \\+ user|two-token|X-User-Token' \
  doge-complaints-gateway/docs/runtime-docs/architecture-and-layers-as-is.md
# expect 0 on /intake/stories row after P6
```
