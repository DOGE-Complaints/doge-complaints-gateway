## Task workspace — `task-m2-18-02-t07-zone-b-supabase-deserialization-contracts`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **B**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — PostgREST type coercion contracts

### Цель
PostgREST type coercion contracts (Zone **B**). Offline contract tests per REQ-39.

### Факты из кода
1. `_coerce_jsonb_text_id_sequence` and related — `db_supabase.py`.
2. PostgREST JSON shapes (list/dict/str) per REQ-39 §B.

### Gap / Проблема
Unit tests never exercise PostgREST deserialization paths.

### AC/DoD
- [x] (P0) B-01..B-04 per REQ-39 §B.
- [x] (P0) New file `tests/test_supabase_deserialization_contracts.py`.

### Где менять код
- `tests/test_supabase_deserialization_contracts.py` (new)

### Out of scope
Changing coercion implementation beyond test fixes.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_supabase_deserialization_contracts.py
```
