# task-gw-gauth-04-t02

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Передать `user_introspection` из route `POST /intake/stories` через `handle_story_intake` → `StoryIntakeService.create_story` и применить T01 mapping **до** persist в Story Store.

## Code Facts
- `request.state.user_introspection` set in deps — [`asgi_app.py:329`](../../../../../../../src/core/api/asgi_app.py)
- Route не передаёт introspection — [`asgi_app.py:482-488`](../../../../../../../src/core/api/asgi_app.py)
- Handler → service — [`handlers.py:201-204`](../../../../../../../src/core/api/handlers.py), [`services.py:237-238`](../../../../../../../src/core/application/services.py)
- Verify-gated deps — [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) `_PUBLIC_CONTENT_WRITE_DEPS`

## Acceptance / DoD
- Traces parent AC #1: persisted author = introspected `sub` on happy path
- Traces parent AC #4: без introspection / rejected gate история не создаётся (регрессия GAUTH-02/03, не payload-author fallback)
- T01 helper invoked before `StoryRecord` construction
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — read `request.state.user_introspection` in `intake_stories`
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) — optional `user_introspection` param
- [`src/core/application/services.py`](../../../../../../../src/core/application/services.py) — apply authoritative submitter at persist

## Out of scope
- Mismatch structured log (T03)
- Contract tests (T05)
- Re-implementing introspection client (GAUTH-02)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'user_introspection|handle_story_intake' src/core/api/asgi_app.py src/core/api/handlers.py -n
```
