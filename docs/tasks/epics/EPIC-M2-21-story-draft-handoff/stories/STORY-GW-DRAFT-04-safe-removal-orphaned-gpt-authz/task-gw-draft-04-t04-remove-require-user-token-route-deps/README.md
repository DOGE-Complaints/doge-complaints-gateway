# task-gw-draft-04-t04-remove-require-user-token-route-deps

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T01, T03

## Purpose
Backlog T03 (part 2): удалить `require_user_token`; заменить `_PUBLIC_CONTENT_WRITE_DEPS` на service-only per T01 (`[Depends(require_public_content_service_auth)]`); wire `/intake/stories` + `/tallinn/issues`.

## Code Facts
- `require_user_token` — [`asgi_app.py:303-334`](../../../../../../../src/core/api/asgi_app.py#L303)
- `_PUBLIC_CONTENT_WRITE_DEPS` — [`asgi_app.py:337-340`](../../../../../../../src/core/api/asgi_app.py#L337)
- Routes — [`/tallinn/issues:525`](../../../../../../../src/core/api/asgi_app.py#L525), [`/intake/stories:541`](../../../../../../../src/core/api/asgi_app.py#L541)
- T01 default: service-only on both; browser auth unchanged on `/story-drafts*`

## Acceptance / DoD
- Traces parent AC #1: `require_user_token` removed; no OAuth user path in `src/`
- Traces parent AC #4: `/intake/stories` + `/tallinn/issues` deps explicit (service-only); no dangling `_PUBLIC_CONTENT_WRITE_DEPS` with user layer
- `POST` without service token → 401 (contrast test still valid)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

## Out of scope
Test/conftest updates (T05); simulation_runner (T06)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'require_user_token|_PUBLIC_CONTENT_WRITE_DEPS' src/core/api/asgi_app.py
pytest tests/test_http_intake_endpoint.py -q 2>/dev/null || true
```
