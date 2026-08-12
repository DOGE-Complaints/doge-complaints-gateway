# task-gw-gauth-02-t01

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** GW-GAUTH-01 (Done)

## Purpose
Добавить конфигурацию gateway→identity introspection: `IDENTITY_INTROSPECT_URL` (база identity) и `IDENTITY_SERVICE_TOKEN` (сервисный токен для `require_service_token` на стороне identity). Подключить значения в `AppConfig` и `ApiDependencies`.

## Code Facts
- Нет `IDENTITY_*` env в [`schema.py`](../../../../../../../src/core/config/schema.py) (grep — 0 matches)
- Образец `EnvSpec` — [`schema.py`](../../../../../../../src/core/config/schema.py) (`SERVICE_API_TOKEN` и др.)
- `ApiDependencies` — [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) (нет introspection-полей)
- Identity ожидает service token на `/oauth/introspect` — [`identity asgi_app.py:407-410`](../../../../../../../../../doge-identity-service/src/core/api/asgi_app.py)

## Acceptance / DoD
- Traces parent AC: Gateway предъявляет identity свой сервисный токен — env `IDENTITY_SERVICE_TOKEN` documented and loadable
- `IDENTITY_INTROSPECT_URL` validated as HTTP(S) base URL (trailing slash normalized)
- Config wired into `ApiDependencies` factory for downstream client (T02)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) — `EnvSpec` + `AppConfig` fields
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — expose introspection config to handlers/client

## Out of scope
- HTTP client implementation (T02)
- `require_user_token` wiring (T03)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'IDENTITY_INTROSPECT_URL|IDENTITY_SERVICE_TOKEN' src/core/config/schema.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_config_loading.py -k IDENTITY 2>/dev/null || true
```
