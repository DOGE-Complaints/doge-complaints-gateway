# task-gw-es-03-t03-public-get-handler

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** T00 Done; T02
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
Публичный GET Emerging L2: handler → `build_success_envelope`; path from T00 REQ/ADR only; register in `PUBLIC_ROUTES` + OPTIONS.

## Code Facts
- Pulse public etalon — [`asgi_app.py:65,429–439`](../../../../../../../../src/core/api/asgi_app.py) `/tallinn/network-pulse`
- Issues public — [`asgi_app.py:443`](../../../../../../../../src/core/api/asgi_app.py)
- Handler pulse etalon — [`handlers.py`](../../../../../../../../src/core/api/handlers.py) `handle_network_pulse`
- **Path invent forbidden** until T00 artifact names it

## Acceptance / DoD
- [ ] Traces AC: Public GET; path in `PUBLIC_ROUTES`
- [ ] Handler uses **only** `dependencies.emerging_signals_service`
- [ ] No `require_*_service_auth` on route
- [ ] Path string taken from T00 REQ/ADR (cite path in acceptance)
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t03.md` signed (Date post P3 verify only)

## Where to change
- [`handlers.py`](../../../../../../../../src/core/api/handlers.py)
- [`asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) `PUBLIC_ROUTES` + GET/OPTIONS

## Out of scope
- Naming path without T00; OpenAPI (T06); service logic (T01)

## Verification commands
```bash
# After T00 names path — replace PATH:
rg -n 'PUBLIC_ROUTES|emerging|handle_emerging' doge-complaints-gateway/src/core/api/
```
