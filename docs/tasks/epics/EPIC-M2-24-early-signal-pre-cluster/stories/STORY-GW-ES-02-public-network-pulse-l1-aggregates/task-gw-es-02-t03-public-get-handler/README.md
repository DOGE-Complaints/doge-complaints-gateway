# task-gw-es-02-t03-public-get-handler

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** **T00 Done** (path+payload); T01; T02
- **decision_ref:** backlog ES-02 §C — path from REQ/ADR only

## Purpose
Добавить `handle_network_pulse` → success envelope; `@app.get(<PATH_FROM_T00>)` **без** service-auth; тот же path в `PUBLIC_ROUTES`. Вызов только `dependencies.network_pulse_service`.

## Code Facts
- `PUBLIC_ROUTES` — [`asgi_app.py:57-64`](../../../../../../../../src/core/api/asgi_app.py)
- L3 public pattern — [`handlers.py:362`](../../../../../../../../src/core/api/handlers.py) Issues list without service-auth
- Envelope — [`envelope.py`](../../../../../../../../src/core/api/envelope.py)
- `/metrics` unfit — [`metrics.py:31-38`](../../../../../../../../src/core/api/metrics.py) (do not reuse)

## Acceptance / DoD
- [x] Traces parent AC: Public GET (no service-auth) returns envelope; path in `PUBLIC_ROUTES`
- [x] Path literal taken **only** from T00 REQ/ADR artifact
- [x] Handler uses `dependencies.network_pulse_service` (not intake repository dig)
- [x] `/metrics` not used for Pulse
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t03.md` signed (Date post P3 verify only)

## Where to change
- [`handlers.py`](../../../../../../../../src/core/api/handlers.py)
- [`asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) — route + `PUBLIC_ROUTES`

## Out of scope
- Inventing path if T00 not Done; normative docs polish (T04/T06); Emerging L2

## Verification commands
```bash
# Replace PATH with T00 literal after Done:
rg -n 'handle_network_pulse|PUBLIC_ROUTES' doge-complaints-gateway/src/core/api/asgi_app.py doge-complaints-gateway/src/core/api/handlers.py
rg -n 'require_.*service_auth' doge-complaints-gateway/src/core/api/asgi_app.py | head
```
