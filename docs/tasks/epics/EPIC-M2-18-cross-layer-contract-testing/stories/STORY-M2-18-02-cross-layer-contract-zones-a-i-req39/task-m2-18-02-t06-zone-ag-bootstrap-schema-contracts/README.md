## Task workspace — `task-m2-18-02-t06-zone-ag-bootstrap-schema-contracts`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **A, G**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — Bootstrap SQL ↔ Python SELECT/INSERT field invariant

### Цель
Bootstrap SQL ↔ Python SELECT/INSERT field invariant (Zone **A, G**). Offline contract tests per REQ-39.

### Факты из кода
1. `_STORY_SELECT_FIELDS`, `save_story()`, `_story_geo_supabase_fields()` — `db_supabase.py`.
2. `supabase/bootstrap/000_full_init.sql`.
3. Partial tests in `tests/test_supabase_bootstrap_schema.py`.

### Gap / Проблема
GAP-07 class: SELECT fields vs bootstrap drift undetected.

### AC/DoD
- [x] (P0) A-01..A-05, G-01..G-02 per REQ-39 §A, §G (+5 tests to existing file).
- [x] (P1) Delta migration assert A-04 if not already present.

### Где менять код
- `tests/test_supabase_bootstrap_schema.py` (extend)

### Out of scope
Runtime code changes; live Supabase.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_bootstrap_schema.py
```
