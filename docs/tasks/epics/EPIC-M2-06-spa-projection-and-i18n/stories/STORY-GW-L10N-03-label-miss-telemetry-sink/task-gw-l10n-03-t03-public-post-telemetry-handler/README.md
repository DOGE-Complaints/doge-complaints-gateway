# task-gw-l10n-03-t03

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
`POST /telemetry/label-misses` без auth; validate `label_key` non-empty, `locale ∈ {et,ru,en}`; soft 400 via envelope; `202 Accepted`; store errors isolated (log + safe response, no ASGI crash).

## Code Facts
- `src/core/api/asgi_app.py:394-409` — public `/intake/stories` (no `require_service_auth`)
- `src/core/api/asgi_app.py:378` — contrast: `/tallinn/issues` POST requires auth
- `src/core/api/handlers.py` — `build_success_envelope`, `ensure_trace_id`
- `src/core/api/envelope.py` — error envelope types

## Acceptance / DoD
- Traces: AC1 (public POST без PII), AC3 (soft 400; store fail isolated)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/api/asgi_app.py` — route registration (no auth dependency)
- `src/core/api/handlers.py` or new `telemetry_handlers.py` — handler logic
- Request validation model (Pydantic or dataclass)

## Verification commands
```bash
pytest tests/test_gw_l10n_03_label_miss_telemetry.py -q -k post
# TestClient: valid → 202; invalid → 400
```
