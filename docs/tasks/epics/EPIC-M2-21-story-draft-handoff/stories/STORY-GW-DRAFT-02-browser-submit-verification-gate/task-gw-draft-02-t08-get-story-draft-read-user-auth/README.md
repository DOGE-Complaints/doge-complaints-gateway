# task-gw-draft-02-t08-get-story-draft-read-user-auth

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000044)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_02_audit_followup`)
- **Depends on:** T02 (GET route exists via GW-DRAFT-01 T04)
- **Audit ref:** [`audit-gw-draft-02-browser-submit-verification-gate-2026-07-03`](../../../../../../analysis/audit-gw-draft-02-browser-submit-verification-gate-2026-07-03.md) **G1**

## Purpose
Закрыть carry-over G1: `GET /story-drafts/{draft_id}` сейчас под placeholder [`require_story_draft_user_auth`](../../../../../../../src/core/api/asgi_app.py) (`_ = request`); полный payload черновика доступен без Bearer. Реализовать browser session auth через identity `/me` (**active session only** — без `phone_verified` gate на GET, per [`mvp-integration-plan-2026-07-02 §4`](../../../../../../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md)).

## Code Facts
- Placeholder — [`asgi_app.py:345-347`](../../../../../../../src/core/api/asgi_app.py#L345) `require_story_draft_user_auth`
- GET route — [`asgi_app.py:559`](../../../../../../../src/core/api/asgi_app.py#L559), `_STORY_DRAFT_READ_DEPS`
- Submit auth (reference, **не алиасить**) — [`asgi_app.py:350`](../../../../../../../src/core/api/asgi_app.py#L350) `require_story_draft_submit_user` (full GAUTH-03 gate incl. 403)
- Bearer extract — [`security.py:49`](../../../../../../../src/core/api/security.py#L49) `extract_authorization_bearer`
- `/me` client — [`me_client.py`](../../../../../../../src/core/identity/me_client.py) `IdentityMeClient.fetch_me`
- GW-DRAFT-01 audit отложил G1 → GW-DRAFT-02; submit закрыт, GET остался бесхозным

## Acceptance / DoD
- Новый dep `require_story_draft_read_user`: Bearer → `/me` → **active=true** only (401 inactive/missing; 503 identity down/unconfigured)
- **Не** вызывать `evaluate_verification_gate` / **не** возвращать 403 `verification_required` на GET (submit-only)
- `_STORY_DRAFT_READ_DEPS` wired to real dep (placeholder removed)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P6)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

## Out of scope
`phone_verified` gate on GET; draft→user binding (interview open question); G2 dep consolidation → [GW-DRAFT-04](../../../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md); contract tests (T09); runtime docs (T10)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'require_story_draft_read_user|require_story_draft_user_auth' src/core/api/asgi_app.py
```
