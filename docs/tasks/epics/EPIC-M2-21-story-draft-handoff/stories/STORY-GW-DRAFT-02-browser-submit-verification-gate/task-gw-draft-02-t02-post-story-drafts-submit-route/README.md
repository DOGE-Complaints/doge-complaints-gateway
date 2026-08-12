# task-gw-draft-02-t02-post-story-drafts-submit-route

## Meta
- **Story:** [STORY-GW-DRAFT-02](../STORY-GW-DRAFT-02-browser-submit-verification-gate.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000044
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Роут `POST /story-drafts/{draft_id}/submit` в [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py): извлечь Supabase-Bearer, вызвать `/me`-клиент, достать черновик из GW-DRAFT-01 store (`story_draft_repository`).

## Code Facts
- User-auth stub — [`asgi_app.py:343-345`](../../../../../../../src/core/api/asgi_app.py) `require_story_draft_user_auth`
- Intake route pattern — [`asgi_app.py:475+`](../../../../../../../src/core/api/asgi_app.py)
- Draft handlers — [`handlers.py:507+`](../../../../../../../src/core/api/handlers.py)
- Bearer extract — `extract_user_token` in security layer (used by `require_user_token`)

## Acceptance / DoD
- Traces parent AC #1 partial: route registered `POST /story-drafts/{draft_id}/submit`
- Traces parent AC #5 partial: unknown/expired draft → 404 path wired
- Handler `handle_story_draft_submit` skeleton delegates to me-client + draft repo
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) (me client wiring)

## Out of scope
Verification gate outcomes + story create (T03); idempotency (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'story-drafts/.*/submit|handle_story_draft_submit' src/core/api/
```
