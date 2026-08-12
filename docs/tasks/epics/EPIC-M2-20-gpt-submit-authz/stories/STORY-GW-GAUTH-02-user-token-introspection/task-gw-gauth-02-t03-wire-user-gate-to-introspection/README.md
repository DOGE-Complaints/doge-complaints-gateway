# task-gw-gauth-02-t03

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Заменить GAUTH-01 stub `require_user_token`: извлечь пользовательский токен из `X-User-Token` ([`extract_user_token`](../../../../../../../src/core/api/security.py)), вызвать introspection-клиент (T02), сохранить результат (`sub`, `phone_verified`, `active`) в request state / dependency для downstream GAUTH-03/04.

## Code Facts
- Presence-only stub — [`asgi_app.py:266-268`](../../../../../../../src/core/api/asgi_app.py)
- `extract_user_token` — [`security.py:16-19`](../../../../../../../src/core/api/security.py)
- `_PUBLIC_CONTENT_WRITE_DEPS` — [`asgi_app.py:271-274`](../../../../../../../src/core/api/asgi_app.py)
- Audit G2 closed: `X-User-Token` — [`audit-gw-gauth-01-...`](../../../../../../analysis/audit-gw-gauth-01-two-layer-auth-on-submit-2026-06-25.md) §3 G2

## Acceptance / DoD
- Traces parent AC: verify-гейтед mutation calls identity introspection per request (optional per-request cache — open question)
- Traces parent AC: статус не из тела входящего токена — only identity response used
- Introspection result available to handlers without creating story on failure path (T04)
- Service layer unchanged (`Authorization: Bearer` / `X-Service-Token` separate from `X-User-Token`)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — replace `require_user_token` stub
- [`src/core/api/security.py`](../../../../../../../src/core/api/security.py) — optional result types / errors
- Introspection client from T02

## Out of scope
- `phone_verified=false` → `verification_required` 403 (GW-GAUTH-03)
- Authoritative `submitter` from introspection (GW-GAUTH-04)
- Re-implementing `X-User-Token` extraction (done in GAUTH-01)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'require_user_token|introspect' src/core/api/asgi_app.py -n
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py -k wire 2>/dev/null || true
```
