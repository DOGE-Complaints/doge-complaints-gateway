# task-gw-draft-01-t03-post-story-drafts-route

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
`POST /story-drafts`: service-auth only (`require_public_content_service_auth`), `parse_story_intake_request`, save draft, return `{draft_id}`; **no issue create** (D-DRAFT-2 A+E).

## Code Facts
- Service auth — [`asgi_app.py:291-295`](../../../../../../../src/core/api/asgi_app.py)
- Intake parse — [`intake/contracts.py`](../../../../../../../src/core/intake/contracts.py)
- Intake route pattern — [`asgi_app.py:475`](../../../../../../../src/core/api/asgi_app.py)
- Error envelope — [`envelope.py:59`](../../../../../../../src/core/api/envelope.py)

## Acceptance / DoD
- Traces parent AC #1: valid service token → `{draft_id}`, no issue
- Traces parent AC #2: missing/invalid token → 401 UNAUTHORIZED
- Traces parent AC #4: invalid contract → 400 VALIDATION_ERROR
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)
- Handler module if extracted (e.g. `handlers.py`)

## Out of scope
GET route (T04); user-auth layer

## Verification commands
```bash
cd doge-complaints-gateway && rg 'story-drafts' src/core/api/
```
