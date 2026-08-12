# task-gw-draft-01-t04-get-story-drafts-route

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
`GET /story-drafts/{draft_id}`: return saved JSON; 404 on unknown/expired; **user-auth Depends stub** for GW-DRAFT-02 (D-DRAFT-2 B).

## Code Facts
- No `/story-drafts` routes today — [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)
- User gate pattern (future) — `require_user_token` [`asgi_app.py:298`](../../../../../../../src/core/api/asgi_app.py) — **stub only in T04**

## Acceptance / DoD
- Traces parent AC #3: GET returns payload; unknown/expired → 404
- User-auth hook present as placeholder Depends (no-op or minimal stub documented)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

## Out of scope
Full identity `/me` client (GW-DRAFT-02); POST submit

## Verification commands
```bash
cd doge-complaints-gateway && rg 'GET.*story-drafts|get_story_draft' src/core/api/
```
