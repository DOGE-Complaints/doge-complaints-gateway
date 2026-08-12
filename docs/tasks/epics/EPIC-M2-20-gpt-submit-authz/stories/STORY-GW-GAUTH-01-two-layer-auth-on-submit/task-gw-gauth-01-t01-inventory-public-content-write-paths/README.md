# task-gw-gauth-01-t01

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** analyze
- **Status:** ⚪ Todo
- **Package:** pkg-000039
- **Skill declared:** python-pro

## Purpose
Инвентаризация write-путей: перечислить все мутации публичного контента (как минимум `POST /intake/stories`; сверить `/tallinn/issues` и иные `@app.post`), зафиксировать, какие уже под `require_service_auth`, какие нет; классификация по D-GAUTH-2.

## Code Facts
- `POST /intake/stories` — без auth ([`asgi_app.py:396`](../../../../../../../src/core/api/asgi_app.py#L396))
- `POST /tallinn/issues` — `require_service_auth` ([`asgi_app.py:380`](../../../../../../../src/core/api/asgi_app.py#L380))
- `POST /telemetry/label-misses` — без auth ([`asgi_app.py:414`](../../../../../../../src/core/api/asgi_app.py#L414))
- `require_service_auth` — [`asgi_app.py:252-256`](../../../../../../../src/core/api/asgi_app.py#L252-L256)
- D-GAUTH-2 — [`interview-gpt-submit-authz-2026-06-24.md`](../../../../../../backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md)

## Acceptance / DoD
- Traces parent AC: Политика «оба слоя» применена ко **всем** write-путям публичного контента (D-GAUTH-2), не только к intake — inventory matrix complete
- Artifact [`public-content-write-path-inventory.md`](./public-content-write-path-inventory.md): route, method, public-content (Y/N), service gate (current/target), user gate (current/target)
- All `@app.post` routes in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) listed
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifact: `public-content-write-path-inventory.md` in this folder
- No `src/core/` changes in T01

## Out of scope
- Attaching service gate to routes (T02)
- Config policy for mandatory service auth (T03)
- User introspection (GW-GAUTH-02)

## Verification commands
```bash
cd doge-complaints-gateway && rg '@app\.(post|put|patch|delete)' src/core/api/asgi_app.py -n
```
