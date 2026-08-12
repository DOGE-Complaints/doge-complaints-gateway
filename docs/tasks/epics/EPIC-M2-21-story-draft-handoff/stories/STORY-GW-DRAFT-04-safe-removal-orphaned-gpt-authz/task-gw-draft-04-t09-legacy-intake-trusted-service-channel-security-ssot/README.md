# task-gw-draft-04-t09-legacy-intake-trusted-service-channel-security-ssot

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000046)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_04_audit_followup`)
- **Depends on:** T08 (architecture table aligned)
- **Audit ref:** [`audit-gw-draft-04-safe-removal-orphaned-gpt-authz-2026-07-03`](../../../../../../analysis/audit-gw-draft-04-safe-removal-orphaned-gpt-authz-2026-07-03.md) **G1**

## Purpose
Закрыть audit **G1**: явная trust-модель для legacy public-content writes — `/intake/stories` и `/tallinn/issues` = **trusted service channel** без user-verification (confused-deputy backstop снят by-design в T04). Продуктовый user submit с `phone_verified` gate — только browser `POST /story-drafts/{id}/submit` (GW-DRAFT-02).

## Code Facts
- Service-only routes — [`asgi_app.py:485,501`](../../../../../../../src/core/api/asgi_app.py) — `require_public_content_service_auth` only
- Payload submitter persisted when no introspection — [`handlers.py:180-203`](../../../../../../../src/core/api/handlers.py) — `user_introspection=None` → payload submitter (no authoritative override)
- Stale contrast — [`security-env-api-access.md:100`](../../../../../../../docs/runtime-docs/security-env-api-access.md) — «service token + X-User-Token + IdentityIntrospectionClient»
- Stale deploy guide — [`server-env-quickstart.md:58-69`](../../../../../../../docs/runtime-docs/manuals/server-env-quickstart.md) — two-layer GAUTH + `IDENTITY_INTROSPECT_URL` (env removed from [`schema.py`](../../../../../../../src/core/config/schema.py))
- Browser path SSOT — [`security-env-api-access.md:88-98`](../../../../../../../docs/runtime-docs/security-env-api-access.md) — `/story-drafts*` + `/me` + verification gate

## Acceptance / DoD
- Traces audit G1: security SSOT states `/intake/stories` + `/tallinn/issues` = trusted service channel; no user-verification backstop
- Explicit risk note: service token compromise or re-exposing route as user-facing removes prior confused-deputy protection
- `security-env-api-access.md` contrast paragraph updated (no `X-User-Token` / `IdentityIntrospectionClient`)
- `server-env-quickstart.md` intake section: only `SERVICE_API_TOKEN`; no `IDENTITY_INTROSPECT_*` / `require_user_token` references
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`docs/runtime-docs/security-env-api-access.md`](../../../../../../../docs/runtime-docs/security-env-api-access.md) — § contrast legacy intake (~L100); optional trust callout near §4.1
- [`docs/runtime-docs/manuals/server-env-quickstart.md`](../../../../../../../docs/runtime-docs/manuals/server-env-quickstart.md) — § intake auth (~L58-69)

## Out of scope
- Identity `04-security` canon (GW-DRAFT-03 G1 → STORY-IDS-DOC-DRAFT-05, `activation: none`)
- Prod code; pytest
- G2 deps consolidation (`require_story_draft_*`, `activation: none`)

## Verification commands
```bash
rg 'IDENTITY_INTROSPECT|X-User-Token|require_user_token|IdentityIntrospection' \
  doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md \
  doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md
# expect 0 after P6
rg -i 'trusted service|service-only|service channel' \
  doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md
```
