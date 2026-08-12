## Task workspace — `task-m2-18-01-t01-zone-l-issue-projection-store-contract`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **L**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — IssueProjectionReadStore protocol contract (InMemory + SQLite)

### Цель
IssueProjectionReadStore protocol contract (InMemory + SQLite) (Zone **L**). Offline contract tests; дополняют REQ acceptance suites, не заменяют `test_req24_*` / `test_req40_*` без решения оператора.

### Факты из кода
1. `IssueProjectionReadStore` Protocol — `src/core/application/issue_create.py` (REQ-39 §L).
2. Implementations: `InMemoryIssueProjectionStore`, `SqliteIssueProjectionStore` — `repositories.py`, `db_sqlite.py`.
3. Table `doge_issues` per REQ-27.

### Gap / Проблема
Нет parametrized contract roundtrip list/get across store implementations.

### AC/DoD
- [x] (P0) L-01..L-04 per REQ-39 §L (save/get roundtrip, status filter, list all, missing id).
- [x] (P0) `@pytest.mark.parametrize` InMemory + SQLite factories.
- [x] (P1) Reuse payload helpers from `test_req24_tallinn_issues_read_api.py` where DRY.

### Где менять код
- `tests/test_issue_projection_store_contract.py` (new)

### Out of scope
Supabase live store; HTTP handlers.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_issue_projection_store_contract.py
```
