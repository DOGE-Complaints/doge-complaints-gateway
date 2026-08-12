# Acceptance — TASK-GW-RC-01-T01

- **Result:** PASS
- **Date:** 2026-06-19

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Неполный payload → `id`/`status` из колонок | PASS | `merge_projection_columns` in `read_filters.py`; `test_m14_incomplete_payload_merge_columns` |
| Фильтр `?status=` по колонке | PASS | `filter_projection_rows` row_status branch; `test_m13_status_filter_uses_column_not_payload` |
