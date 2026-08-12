# Acceptance verification — TASK-M2-08-05-T08

- **Task:** AUDIT-GAP-35-01 — SQLite admin geo roundtrip test
- **Result:** PASS
- **Evidence:** `test_geo_admin_fields_survive_sqlite_roundtrip` green; read path fix in `db_sqlite.py` `_STORY_SELECT_COLUMNS` includes `geo_admin_*` (write path already persisted; SELECT omitted columns — root cause found by test)
- **Commands:** `pytest tests/test_geo_candidate_persistence_roundtrip.py -q`; full suite **269 passed**, 10 skipped

| AC | Status | Evidence |
|----|--------|----------|
| P0 new SQLite roundtrip test | PASS | `test_geo_admin_fields_survive_sqlite_roundtrip` |
| P0 SqliteDatabase + SqliteStoryRepository | PASS | in-memory schema + repo |
| P0 all four admin_* preserved | PASS | assert settlement/country/district/region |
| P1 file + full suite green | PASS | 269 passed |
