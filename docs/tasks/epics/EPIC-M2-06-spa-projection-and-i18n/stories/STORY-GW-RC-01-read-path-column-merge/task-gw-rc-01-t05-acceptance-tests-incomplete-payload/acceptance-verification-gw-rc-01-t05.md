# Acceptance — TASK-GW-RC-01-T05

- **Result:** PASS
- **Date:** 2026-06-19

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Неполный payload → list/get с `id`/`status`/`created_at` | PASS | `test_gw_rc_01_read_path_column_merge.py` store + HTTP |
| `?status=` по колонке | PASS | `test_store_status_filter_uses_column_not_payload`, `test_http_status_filter_uses_column_not_payload` |
| InMemory + SQLite | PASS | `@pytest.fixture(params=["memory", "sqlite"])` |
