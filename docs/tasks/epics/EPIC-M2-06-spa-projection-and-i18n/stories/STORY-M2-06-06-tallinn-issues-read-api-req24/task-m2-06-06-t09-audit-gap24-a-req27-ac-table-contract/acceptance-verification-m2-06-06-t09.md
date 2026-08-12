# Acceptance verification — TASK-M2-06-06-T09

- **Task:** REQ-27 AC-1/AC-2 table contract (no DDL rename)
- **Result:** PASS
- **Evidence:** `test_req24_ac1_sqlite_doge_issues_table_exists`, `test_req24_ac2_write_path_uses_doge_issues`, `test_req24_ac2_sqlite_write_path_uses_doge_issues_table`; REQ-24 §2.1 superseded + §3.3–3.4 / §6 step 1 → `doge_issues`
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py::test_req24_ac1_sqlite_doge_issues_table_exists tests/test_req24_tallinn_issues_read_api.py::test_req24_ac2_write_path_uses_doge_issues tests/test_req24_ac2_sqlite_write_path_uses_doge_issues_table -q`
