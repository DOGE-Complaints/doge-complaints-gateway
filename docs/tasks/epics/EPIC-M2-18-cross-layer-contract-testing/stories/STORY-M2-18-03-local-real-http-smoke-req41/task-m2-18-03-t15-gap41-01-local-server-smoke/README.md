## Task workspace — `task-m2-18-03-t15-gap41-01-local-server-smoke`

- Story: [`../STORY-M2-18-03-local-real-http-smoke-req41.md`](../STORY-M2-18-03-local-real-http-smoke-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-01; PS-01, PS-19

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~2–4 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: tests — local server smoke (real HTTP stack, canvas intake)

### Цель
Создать `tests/smoke/test_local_server_smoke.py` с LS-01..LS-06: реальный TCP/HTTP против uvicorn, данные из sandbox canvas через `_scenario_to_payload()`.

### Почему это важно (риск)
Все 412+ offline тестов используют `FastAPI TestClient` (in-process ASGI). Проблемы uvicorn keep-alive, middleware headers, connection errors не ловятся.

### Факты из кода
1. REQ-41 §3 GAP-41-01 — `LOCAL_SERVER_URL` (default `http://127.0.0.1:8000`); skip без env.
2. [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) L54 — `_scenario_to_payload(scenario)`.
3. [`tests/sandbox/dogestonia_simulation_canvas_v0_1.json`](../../../../../../../tests/sandbox/dogestonia_simulation_canvas_v0_1.json) — 130 сценариев, 4 группы.
4. `tests/smoke/` — **не существует** (glob); Layer 6 описан в [`13-testing-and-quality-architecture.md`](../../../../../../solution%20architecture/13-testing-and-quality-architecture.md) L13–17.
5. `httpx` в [`pyproject.toml`](../../../../../../../pyproject.toml) dependencies.

### Gap / Проблема
**GAP-41-01:** нет pytest smoke против реального HTTP с sandbox-данными.

### AC/DoD
- [x] (P0) `tests/smoke/conftest.py` — fixture `local_server_url`; skip if unset; skip if `/health` unreachable.
- [x] (P0) LS-01: `GET /health` → 200, body contains `"status"`.
- [x] (P0) LS-02: `POST /intake/stories` (infrastructure scenario) → 202, `data.story_id`.
- [x] (P0) LS-03: intake × 4 groups → all 202.
- [x] (P0) LS-04: `GET /tallinn/issues` → 200, `Content-Type: application/json`.
- [x] (P0) LS-05: invalid payload → 422, error envelope.
- [x] (P0) LS-06: trace correlation (`x-trace-id` round-trip or `x-request-id` header).
- [x] (P1) Assert `Server` header contains `uvicorn` where applicable.

### Где менять код
- `tests/smoke/conftest.py` (new)
- `tests/smoke/test_local_server_smoke.py` (new)

### Out of scope
- Запуск uvicorn inside pytest (operator manual start, REQ-41 §7).
- `pkg-000020`; prod code changes unless test fails.

### Команды проверки
```bash
# Terminal 1 (from doge-complaints-gateway/):
APP_PROFILE=demo DB_BACKEND=in_memory CLUSTER_CRON_ENABLED=false \
  python3 -m uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000

# Terminal 2:
cd doge-complaints-gateway && LOCAL_SERVER_URL=http://127.0.0.1:8000 \
  python3 -m pytest -q tests/smoke/test_local_server_smoke.py
```
