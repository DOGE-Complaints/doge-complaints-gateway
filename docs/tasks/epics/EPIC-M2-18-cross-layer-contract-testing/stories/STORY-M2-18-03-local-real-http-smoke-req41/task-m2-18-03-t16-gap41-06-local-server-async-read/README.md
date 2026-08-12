## Task workspace — `task-m2-18-03-t16-gap41-06-local-server-async-read`

- Story: [`../STORY-M2-18-03-local-real-http-smoke-req41.md`](../STORY-M2-18-03-local-real-http-smoke-req41.md)
- Decision Ref: [`../../../../../../requirements/41-testing-production-coverage-target-state.md`](../../../../../../requirements/41-testing-production-coverage-target-state.md) §3 GAP-41-06

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~1–2 ч  
**Статус:** Done  
**Wave:** `pkg-000021`  
---

## Task: tests — async httpx read against local server

### Цель
`tests/smoke/test_local_server_async_read.py` — AC-01..03: `httpx.AsyncClient` для `GET /tallinn/issues` после sync intake seed.

### Почему это важно (риск)
SPA uses async `fetch`; sync TestClient does not exercise async client chunked/reuse behavior.

### Факты из кода
1. REQ-41 §3 GAP-41-06 — same `LOCAL_SERVER_URL` guard as T15.
2. [`pyproject.toml`](../../../../../../../pyproject.toml) — `asyncio_default_fixture_loop_scope` set; **no** `pytest-asyncio` in dev deps yet.
3. Depends on T15 smoke conftest / server running.

### Gap / Проблема
**GAP-41-06:** no async HTTP client tests for issues read API.

### AC/DoD
- [x] (P0) Add `pytest-asyncio` to `[project.optional-dependencies] dev` if missing.
- [x] (P0) AC-01: async `GET /tallinn/issues` → 200, valid JSON.
- [x] (P0) AC-02: `GET /tallinn/issues?status=PUBLISHED` → 200 (empty list OK).
- [x] (P0) AC-03: `asyncio.gather` × 3 parallel GETs → all 200, identical `data` payloads.
- [x] (P1) Optional sync pre-seed via `httpx.Client` (5 infrastructure scenarios).

### Где менять код
- [`pyproject.toml`](../../../../../../../pyproject.toml) (dev deps)
- `tests/smoke/test_local_server_async_read.py` (new)

### Out of scope
- Changing FastAPI handlers; `pkg-000020`.

### Команды проверки
```bash
cd doge-complaints-gateway && LOCAL_SERVER_URL=http://127.0.0.1:8000 \
  python3 -m pytest -q tests/smoke/test_local_server_async_read.py
```
