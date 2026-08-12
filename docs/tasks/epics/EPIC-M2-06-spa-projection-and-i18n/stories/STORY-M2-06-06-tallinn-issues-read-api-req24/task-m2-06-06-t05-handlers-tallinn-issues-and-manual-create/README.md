## Task workspace — `task-m2-06-06-t05-handlers-tallinn-issues-and-manual-create`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: REQ-24 §4.1, §6 steps 9–11; GAP-24-05

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** ~2 ч  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — Tallinn handlers and `create_manual_issue`

### Цель
Добавить `handle_tallinn_issues_list`, `handle_tallinn_issue_get`, `handle_tallinn_issue_create` и `IssueCreateService.create_manual_issue`.

### Факты из кода
1. [`handlers.py`](../../../../../../../src/core/api/handlers.py) — нет `handle_tallinn_*` (`grep` → 0).
2. `grep create_manual_issue src/` → 0.
3. REQ-24 §4.1 — success envelope `data.issues` / `data.issue` / `data.issue_id`; 404 на missing id.
4. REQ-24 AC-10..12 — POST body: `cluster_id`, `story_ids`, `title`, `type`.

### Gap / Проблема
**GAP-24-05:** нет application handlers и manual create path для оператора.

### AC/DoD
- [ ] (P0) `handle_tallinn_issues_list` → `issue_projection_read_store.list_projections(...)`.
- [ ] (P0) `handle_tallinn_issue_get` → 200 / 404.
- [ ] (P0) `handle_tallinn_issue_create` → `create_manual_issue` → 201.
- [ ] (P0) `IssueCreateService.create_manual_issue` сохраняет projection в store (write path).
- [ ] (P1) Unit tests с mock `ApiDependencies`.
- [ ] (P1) Query params geo/time — T07 (pass-through stub OK until T07).

### Где менять код
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py)

### Out of scope
- Route registration (T06)
- Full filter logic in stores (T07)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.api import handlers; assert hasattr(handlers,'handle_tallinn_issues_list'); print('ok')"
```
