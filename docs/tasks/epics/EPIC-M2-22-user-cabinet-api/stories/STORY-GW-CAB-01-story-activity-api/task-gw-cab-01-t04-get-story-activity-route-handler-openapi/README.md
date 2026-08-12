# task-gw-cab-01-t04-get-story-activity-route-handler-openapi

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000052
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Expose `GET /story-activity` with browser Bearer auth (`require_story_draft_read_user`), SuccessEnvelope, and OpenAPI/API_REFERENCE sync.

## Code Facts
- Read dep reuse — [`asgi_app.py:301-321`](../../../../../../../../src/core/api/asgi_app.py#L301) `require_story_draft_read_user`
- `_STORY_DRAFT_READ_DEPS` — [`asgi_app.py:356`](../../../../../../../../src/core/api/asgi_app.py#L356)
- Handler patterns — [`handlers.py`](../../../../../../../../src/core/api/handlers.py)
- OpenAPI SSOT — [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)

## Acceptance / DoD
- [x] Traces parent AC-1: `GET /story-activity` → 200 + MVP `data` shape
- [x] Traces parent AC-3: user-scoped read only; author from `request.state.user_introspection.sub`
- [x] Missing/invalid Bearer → 401 (existing dep behavior)
- [x] OpenAPI + `API_REFERENCE.md` document endpoint
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t04.md`](./acceptance-verification-gw-cab-01-t04.md) signed

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) — route registration
- [`src/core/api/handlers.py`](../../../../../../../../src/core/api/handlers.py) — handler (or new cabinet module)
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)

## Out of scope
- Pagination (AC-4 out of scope)
- Write endpoints (AC-4)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_cab_01_story_activity_api.py -k 'route or openapi' --tb=short
curl -sS -H "Authorization: Bearer $TOKEN" http://localhost:8000/story-activity | jq .
```
