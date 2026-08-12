# Acceptance verification — TASK-M2-06-06-T03

- **Task:** SQLite + Supabase read store
- **Result:** PASS
- **Evidence:** `src/core/infrastructure/db_sqlite.py`, `db_supabase.py` — read `doge_issues`; AC-1 table check
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py::test_req24_ac1_sqlite_doge_issues_table_exists -q`
