# task-gw-gauth-01-t02

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000039
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Привязать сервисный гейт к незащищённым write-путям публичного контента из T01 inventory (минимум `POST /intake/stories`): `dependencies=[Depends(require_service_auth)]` по образцу `/tallinn/issues:380`.

## Code Facts
- Pattern — [`asgi_app.py:380`](../../../../../../../src/core/api/asgi_app.py#L380) `dependencies=[Depends(require_service_auth)]`
- Intake route — [`asgi_app.py:396`](../../../../../../../src/core/api/asgi_app.py#L396)
- `require_service_auth` — [`asgi_app.py:252-256`](../../../../../../../src/core/api/asgi_app.py#L252-L256)
- T01 matrix — [`public-content-write-path-inventory.md`](../task-gw-gauth-01-t01-inventory-public-content-write-paths/public-content-write-path-inventory.md)

## Acceptance / DoD
- Traces parent AC: Подача истории из GPT без доверенного сервисного слоя — отклоняется (не no-op) — when `SERVICE_API_TOKEN` set
- Traces parent AC: Политика «оба слоя» на все write-пути — service gate attached per T01 matrix
- `POST /intake/stories` has `dependencies=[Depends(require_service_auth)]`
- Other public-content writes from T01 covered or explicitly excluded with rationale in inventory
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — route `dependencies=`
- Update T01 inventory with implemented targets

## Out of scope
- Mandatory service auth when token unset (T03)
- User token layer / introspection (GW-GAUTH-02)
- Contract tests (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'intake/stories|require_service_auth' src/core/api/asgi_app.py -n
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_api_security_and_ops.py -k service 2>/dev/null || true
```
