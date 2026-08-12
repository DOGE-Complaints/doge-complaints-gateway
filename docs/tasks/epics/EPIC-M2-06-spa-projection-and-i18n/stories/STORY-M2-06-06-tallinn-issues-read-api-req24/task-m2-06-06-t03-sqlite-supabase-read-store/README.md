## Task workspace — `task-m2-06-06-t03-sqlite-supabase-read-store`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §3.3–3.4, §6 steps 5–6; REQ-27 (`doge_issues`); GAP-24-03

---
**Приоритет:** P0  
**Сложность:** L  
**Оценка времени:** ~2–3 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — SQLite and Supabase read stores

### Цель
Добавить `list_projections` и `get_projection` в `SqliteIssueProjectionStore` и `SupabaseIssueProjectionStore`, читая **`doge_issues`**.

### Факты из кода
1. [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L232 — `CREATE TABLE doge_issues`; L601 — `INSERT INTO doge_issues`.
2. [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) L604 — `path="/rest/v1/doge_issues"`.
3. REQ-24 §3.3 — SQL `SELECT status, payload_json FROM doge_issues` (документ устарел: `tallinn_issues_projections` → заменить на `doge_issues`).
4. Supabase integration tests pattern: [`tests/integration/supabase/test_spa_projection_supabase_roundtrip.py`](../../../../../../../tests/integration/supabase/test_spa_projection_supabase_roundtrip.py).

### Gap / Проблема
**GAP-24-03:** persisted backends не экспонируют read для HTTP layer.

### AC/DoD
- [ ] (P0) SQLite: `list_projections` / `get_projection` с SQL к `doge_issues`.
- [ ] (P0) Supabase: HTTP read к `doge_issues` (PostgREST).
- [ ] (P0) `status` filter в SQL WHERE; `issue_type`/`labels` post-fetch (REQ-24 §3.1.1).
- [ ] (P1) Unit test SQLite с temp DB file.
- [ ] (P1) Integration test Supabase skip без env.
- [ ] (P1) AC-1: table name `doge_issues` (not `tallinn_issues_projections`).

### Где менять код
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)

### Out of scope
- Geo/time extended filters (T07)
- Migration rename (REQ-27 done)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_db_backed_pipeline_e2e.py --maxfail=1 -x 2>/dev/null | head -20
```
