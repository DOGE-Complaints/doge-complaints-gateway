# Acceptance verification — TASK-M2-08-05-T03

- **Task:** Persist geo admin fields in story store
- **Result:** PASS
- **Evidence:** `db_sqlite.py` / `db_supabase.py` read/write `geo_admin_district|settlement|region|country`; `supabase/bootstrap/000_full_init.sql` DDL aligned with `_STORY_SELECT_FIELDS`
- **Commands:** `python3 -m pytest tests/test_stories_schema_cross_layer_invariant.py -q`

| AC | Status | Evidence |
|----|--------|----------|
| P0 SQLite roundtrip admin_* | PASS | insert/select mapping in db_sqlite |
| P0 Supabase adapter parity | PASS | `_STORY_SELECT_FIELDS` + row mapping |
| P1 bootstrap/migration path documented | PASS | `000_full_init.sql`, `20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql` |
| P1 None serializes without loss | PASS | nullable columns, conditional str cast |
