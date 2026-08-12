# BULLRUN Phase Log — TASK-M2-08-05-T08

- [x] Analysis: AUDIT-GAP-35-01 — no SQLite assert for `geo_admin_*` roundtrip
- [x] Implement: `test_geo_admin_fields_survive_sqlite_roundtrip`; fix `_STORY_SELECT_COLUMNS` missing admin columns on read path
- [x] Verify: `acceptance-verification-m2-08-05-t08.md`; `pytest -q` → 269 passed
