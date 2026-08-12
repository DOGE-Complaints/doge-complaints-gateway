# task-gw-cab-02-t03-draft-get-owner-association-on-read

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Ассоциация draft↔owner при чтении: `handle_story_draft_get` принимает `sub` → `draft_owner.set_owner` (best-effort); route прокидывает `user_introspection.sub` (backlog C.5–C.6, D-CAB02-1).

## Code Facts
- `handle_story_draft_get` не принимает `sub` — [`handlers.py:567`](../../../../../../../../src/core/api/handlers.py#L567)
- Route `GET /story-drafts/{draft_id}` не прокидывает `user_introspection.sub` — [`asgi_app.py:514`](../../../../../../../../src/core/api/asgi_app.py#L514)
- Contrast: `story_draft_submit` уже использует `user_introspection` — [`asgi_app.py:537-543`](../../../../../../../../src/core/api/asgi_app.py#L537)
- `require_story_draft_read_user` reuse — [`asgi_app.py:302-357`](../../../../../../../../src/core/api/asgi_app.py#L302)

## Acceptance / DoD
- [x] Traces parent AC-2: association `draft_id→sub` on `GET /story-drafts/{id}` under session
- [x] Traces parent AC-3: isolation prep (owner-scoped writes)
- [x] Scope trace: backlog §C.5–C.6
- [x] Best-effort: read succeeds even if `set_owner` fails
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t03.md`](./acceptance-verification-gw-cab-02-t03.md) signed

## Where to change
- [`src/core/api/handlers.py`](../../../../../../../../src/core/api/handlers.py) — `handle_story_draft_get`
- [`src/core/api/asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) — route `GET /story-drafts/{draft_id}`

## Out of scope
- `GET /story-drafts/current` endpoint (T04)
- Contract tests (T05)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -k 'cab_02 and association' --tb=short
```
