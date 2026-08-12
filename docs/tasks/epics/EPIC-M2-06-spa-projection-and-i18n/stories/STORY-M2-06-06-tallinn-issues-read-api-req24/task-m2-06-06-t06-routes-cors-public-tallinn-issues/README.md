## Task workspace — `task-m2-06-06-t06-routes-cors-public-tallinn-issues`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §4.2; GAP-24-06

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** ~1–1.5 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — routes, CORS, PUBLIC_ROUTES

### Цель
Зарегистрировать `GET /tallinn/issues`, `GET /tallinn/issues/{issue_id}`, `POST /tallinn/issues` (Bearer); добавить CORS middleware.

### Факты из кода
1. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) L32–37 — `PUBLIC_ROUTES` без `/tallinn/issues`.
2. REQ-24 §4.2 — `CORSMiddleware` before routes; `allow_methods=["GET","POST"]`.
3. Existing auth: `require_service_auth` / route policy patterns in `asgi_app.py` and [`security.py`](../../../../../../../src/core/api/security.py).

### Gap / Проблема
**GAP-24-06:** HTTP surface для SPA read отсутствует.

### AC/DoD
- [ ] (P0) `GET /tallinn/issues` → 200 (public).
- [ ] (P0) `GET /tallinn/issues/{issue_id}` → 200/404.
- [ ] (P0) `POST /tallinn/issues` → 401 without Bearer; 201 with valid token (AC-10, AC-11).
- [ ] (P0) `PUBLIC_ROUTES` includes `/tallinn/issues` for GET policy.
- [ ] (P0) CORS: `OPTIONS /tallinn/issues` → AC-9.
- [ ] (P1) All Query params wired (geo expanded in T07).

### Где менять код
- [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

### Out of scope
- OpenAPI (T08)
- Store filter implementation (T07)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.api.asgi_app import app; paths=[r.path for r in app.routes]; assert '/tallinn/issues' in str(paths) or any('tallinn' in str(p) for p in paths); print('ok')"
```
