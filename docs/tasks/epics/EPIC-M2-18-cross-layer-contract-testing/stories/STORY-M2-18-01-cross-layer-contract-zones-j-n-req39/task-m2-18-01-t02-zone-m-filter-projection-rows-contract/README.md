## Task workspace — `task-m2-18-01-t02-zone-m-filter-projection-rows-contract`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **M**

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — filter_projection_rows() filter engine contract

### Цель
filter_projection_rows() filter engine contract (Zone **M**). Offline contract tests; дополняют REQ acceptance suites, не заменяют `test_req24_*` / `test_req40_*` без решения оператора.

### Факты из кода
1. `filter_projection_rows()` — `src/core/projection/read_filters.py` L175+.
2. Partial coverage in `tests/test_req24_tallinn_issues_read_api.py` (AC-15/17/18/19).

### Gap / Проблема
Оставшиеся filter-режимы (type, labels, institution, temporal boundaries) без isolated contract tests.

### AC/DoD
- [x] (P0) M-01..M-08 per REQ-39 §M.
- [x] (P0) Pure unit tests on row tuples — no HTTP.
- [x] (P1) No duplicate assertions already in `test_req24_ac*` — extract shared fixtures if needed.

### Где менять код
- `tests/test_filter_projection_rows_contract.py` (new)

### Out of scope
Store SQL filtering; changing `read_filters.py` behavior.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_filter_projection_rows_contract.py
```
