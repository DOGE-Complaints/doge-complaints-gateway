# task-gw-gauth-01-t03

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000039
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Сделать сервисный слой **обязательным** на gated write-путях (политика «enabled required», не demo no-op) — отсутствие `SERVICE_API_TOKEN` не открывает intake молча; согласовать с `APP_PROFILE` в [`config/schema.py`](../../../../../../../src/core/config/schema.py).

## Code Facts
- `ServiceTokenAuth.require()` no-op when disabled — [`security.py:54-56`](../../../../../../../src/core/api/security.py#L54-L56)
- `build_service_auth_from_env` — [`security.py:65-72`](../../../../../../../src/core/api/security.py#L65-L72)
- `SERVICE_API_TOKEN` env — [`schema.py:117`](../../../../../../../src/core/config/schema.py#L117)
- Pilot requires token — [`schema.py:463-466`](../../../../../../../src/core/config/schema.py#L463-L466)
- ApiDependencies wiring — [`dependencies.py`](../../../../../../../src/core/api/dependencies.py)

## Acceptance / DoD
- Traces parent AC: Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op) — including when token env unset on gated routes
- Traces parent AC: Наличие только сервисного токена **не** открывает создание истории за произвольного пользователя — service layer enforced before handler
- Policy documented: demo vs pilot `SERVICE_API_TOKEN` requirement for public-content writes
- No silent no-op on `POST /intake/stories` when service auth required
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/api/security.py`](../../../../../../../src/core/api/security.py)
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- Optional: startup fail-fast or route-level enforcement per profile decision

## Out of scope
- HTTP introspection client (GW-GAUTH-02)
- Full contract test suite (T04)

## Verification commands
```bash
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_config_loading.py -k SERVICE_API 2>/dev/null || true
cd doge-complaints-gateway && rg 'SERVICE_API_TOKEN|ServiceTokenAuth|service_auth' src/core -n
```
