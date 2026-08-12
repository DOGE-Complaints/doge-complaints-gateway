## Task workspace — `task-m2-06-06-t02-inmemory-read-store-list-get`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §3.2, §6 step 4; GAP-24-02

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** ~1–1.5 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — InMemory `list_projections` / `get_projection`

### Цель
Расширить `InMemoryIssueProjectionStore` read-методами с категориальными фильтрами (`status`, `issue_type`, `labels`).

### Факты из кода
1. [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) L150–172 — только `save_projection`.
2. REQ-24 §3.2 — post-fetch loop для `type` / `labels`; `status` по `row["status"]`.
3. Payload shape — `DOGEIssue.to_public_dict()` (dict в `row["payload"]`).

### Gap / Проблема
**GAP-24-02:** in-memory backend не умеет читать projections для тестов и dev.

### AC/DoD
- [ ] (P0) `list_projections` возвращает `list[dict[str, object]]` (копии payload).
- [ ] (P0) `get_projection(issue_id)` → payload или `None`.
- [ ] (P0) Фильтры `status`, `issue_type`, `labels` по REQ-24 §3.2.
- [ ] (P1) Unit test: empty → `[]`; after save → item present.
- [ ] (P1) Geo/time/institution — T07.

### Где менять код
- [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- `tests/` (минимальный unit в этом таске или T08)

### Out of scope
- SQLite/Supabase (T03)
- Extended filters (T07)

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_issue_create_service.py -k projection --maxfail=1 2>/dev/null || true
```
