# task-gw-rc-01-t05

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro
- **Depends on:** T01, T02, T03, T04

## Purpose
Acceptance-тесты read-path: seed неполного `payload_json` (без `id`/`status`) → `GET /tallinn/issues` и `GET /tallinn/issues/{id}` возвращают `id`, `status`, `created_at` из колонок; `?status=` фильтрует по колонке.

## Code Facts
- REQ-24 тесты не покрывают неполный payload — [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py)
- Handlers: `GET /tallinn/issues`, `GET /tallinn/issues/{id}` — [`handlers.py`](../../../../../../../src/core/api/handlers.py) + [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- Traces parent AC: list/get — `id`, `status`, `created_at` из колонок
- Traces parent AC: неполный payload → `id`/`status` присутствуют
- Traces parent AC: `?status=` по колонке (не payload)
- Traces parent AC: Supabase / SQLite / InMemory (parametrize или отдельные cases)
- Traces parent AC: тест «seed неполного payload → есть id/status»
- Full unit suite без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_rc_01_read_path_column_merge.py` (новый файл)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_01_read_path_column_merge.py -q
cd doge-complaints-gateway && python3 -m pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
