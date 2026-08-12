## Task workspace — `task-m2-06-06-t01-issue-projection-read-store-protocol`

- Story: [`../STORY-M2-06-06-tallinn-issues-read-api-req24.md`](../STORY-M2-06-06-tallinn-issues-read-api-req24.md)
- Decision Ref: [`../../../../../../requirements/24-tallinn-issues-read-api.md`](../../../../../../requirements/24-tallinn-issues-read-api.md) §3.1; SA-18 §7.1; GAP-24-01

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~45 min  
**Статус:** ready  
**Wave:** `pkg-000019`  
---

## Task: implement — `IssueProjectionReadStore` Protocol

### Цель
Добавить Protocol `IssueProjectionReadStore` в `issue_create.py` с полной сигнатурой `list_projections` / `get_projection` (категориальные, временные и geo-параметры).

### Факты из кода
1. [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) L50+ — есть `IssueProjectionStore` (write), нет `IssueProjectionReadStore`.
2. `grep IssueProjectionReadStore src/` → 0 вхождений.
3. REQ-24 §3.1 — полная сигнатура с `status`, `issue_type`, `labels`, `institution`, `created_after`/`before`, geo bbox и address filters.
4. REQ-27 — read store читает таблицу **`doge_issues`**, не `tallinn_issues_projections`.

### Gap / Проблема
**GAP-24-01:** нет контракта read-слоя; stores и handlers не могут типизировать list/get.

### AC/DoD
- [ ] (P0) `IssueProjectionReadStore(Protocol)` объявлен рядом с `IssueProjectionStore`.
- [ ] (P0) `list_projections(...)` — все параметры из REQ-24 §3.1 / SA-18 §7.1.
- [ ] (P0) `get_projection(issue_id: str) -> dict[str, object] | None`.
- [ ] (P1) Docstring описывает OR/AND/null-safety для geo (REQ-24 §3.1.1).
- [ ] (P1) Реализации store — T02–T03; wiring — T04.

### Где менять код
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py)

### Out of scope
- Store implementations (T02–T03)
- HTTP handlers (T05–T06)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.application.issue_create import IssueProjectionReadStore; print('ok', IssueProjectionReadStore)"
```
