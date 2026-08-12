# task-gw-gauth-03-t03

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
`VerificationRequiredError` + HTTP **403** + payload по канону OAUTH-04 через `build_error_envelope` (backlog черновик T02). Поля: `error`, `reason`, `verify_url`.

## Code Facts
- OAUTH-04 canon — [`verification_required.py:14-23`](../../../../../../../../../doge-identity-service/src/core/oauth/verification_required.py)
- Gateway envelope — [`envelope.py:55`](../../../../../../../src/core/api/envelope.py)
- 09-gateway-expectations flat JSON reference — [`09-gateway-expectations.md:37-47`](../../../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md)
- Only 401 handler today — [`asgi_app.py:245-248`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- Traces parent AC #1, #2, #6: 403 `verification_required` body matches OAUTH-04 (embedding in `error.details` or documented flat shape — fix in acceptance)
- `VerificationRequiredError` distinct from `UnauthorizedError`
- `@app.exception_handler` returns 403 with trace_id envelope
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/api/security.py`](../../../../../../../src/core/api/security.py)
- [`src/core/api/envelope.py`](../../../../../../../src/core/api/envelope.py)
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — exception handler

## Out of scope
- Gate wiring (T04)
- Contract tests (T05)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'VerificationRequired|verification_required' src/core/api/
```
