# Acceptance — TASK-GW-RC-01-T07

- **Result:** PASS
- **Date:** 2026-06-19

| AC (audit G3) | Status | Evidence |
|---------------|--------|----------|
| `created_at` всегда в ответе list/get | PASS | `read_filters.py` `merge_projection_columns` always sets `created_at` |
| InMemory fallback `updated_at` | PASS | `repositories.py` `_row_created_at_text` |
| Edge без колонки `created_at` | PASS | `test_store_created_at_fallback_from_updated_at_when_column_missing` |
| Regression GW-RC-01 suite | PASS | `491 passed` unit live 2026-06-19 |
