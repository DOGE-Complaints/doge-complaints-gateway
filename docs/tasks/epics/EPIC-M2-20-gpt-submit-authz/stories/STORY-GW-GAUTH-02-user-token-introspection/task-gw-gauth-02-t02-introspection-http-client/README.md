# task-gw-gauth-02-t02

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Реализовать HTTP-клиент introspection: `POST {IDENTITY_INTROSPECT_URL}/oauth/introspect`, `application/x-www-form-urlencoded` с `token=<user access token>`, сервисный заголовок (`Authorization: Bearer` или `X-Service-Token` по образцу gateway [`security.py`](../../../../../../../src/core/api/security.py)). Парсинг `{active, sub, phone_verified}`; тайм-аут и единый путь ошибки для fail-closed (T04).

## Code Facts
- Identity contract always HTTP 200 — [`introspection.py:14-32`](../../../../../../../../../doge-identity-service/src/core/oauth/introspection.py)
- Active response shape — [`introspection.py:28-32`](../../../../../../../../../doge-identity-service/src/core/oauth/introspection.py)
- Form input `token=` — [`identity asgi_app.py:413-415`](../../../../../../../../../doge-identity-service/src/core/api/asgi_app.py)
- Gateway HTTP patterns — [`db_supabase.py` `_request`](../../../../../../../src/core/infrastructure/db_supabase.py) (httpx); `REQUEST_TIMEOUT_S` in config

## Acceptance / DoD
- Traces parent AC: свежий `{ active, sub, phone_verified }` via `POST /oauth/introspect` — client returns typed result
- Traces parent AC: сервисный токен в исходящем запросе к identity
- Traces parent AC: `phone_verified` parsed from JSON body, **not** decoded from user JWT locally
- Traces parent AC: контракт ответа matches identity `introspection.py`
- Timeout configurable (reuse `REQUEST_TIMEOUT_S` or dedicated knob)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Новый модуль: `src/core/identity/introspection_client.py` (или `src/core/api/identity_introspection.py` — зафиксировать при implement)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — inject client

## Out of scope
- FastAPI dependency wiring on routes (T03)
- `verification_required` 403 for `phone_verified=false` (GW-GAUTH-03)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'introspect|Introspection' src/core -n
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py -k client 2>/dev/null || true
```
