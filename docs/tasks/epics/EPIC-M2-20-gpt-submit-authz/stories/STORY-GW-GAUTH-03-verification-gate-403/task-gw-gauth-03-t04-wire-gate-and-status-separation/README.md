# task-gw-gauth-03-t04

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** T02, T03

## Purpose
Подключить гейт в `require_user_token` после introspection; развести HTTP-коды (backlog черновик T03 + T04). Dependency выполняется до `handle_story_intake` — контент не сохраняется при отказе.

## Code Facts
- `require_user_token` — [`asgi_app.py:272-290`](../../../../../../../src/core/api/asgi_app.py)
- `_PUBLIC_CONTENT_WRITE_DEPS` — [`asgi_app.py:292-296`](../../../../../../../src/core/api/asgi_app.py)
- Intake route — [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) `POST /intake/stories`

## Acceptance / DoD
- Traces parent AC #1, #4, #5: `active=false` → **401**; `phone_verified=false` → **403** verification_required; identity down → **503/500**, not verification_required
- Traces parent AC #1: story not persisted on any reject path (gate before handler)
- `active=true && phone_verified=true` → handler runs unchanged
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — `require_user_token`
- Gate decision (T02) + errors (T03)

## Out of scope
- Contract test file (T05)
- Authoritative submitter (GW-GAUTH-04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'phone_verified|VerificationRequired' src/core/api/asgi_app.py
```
