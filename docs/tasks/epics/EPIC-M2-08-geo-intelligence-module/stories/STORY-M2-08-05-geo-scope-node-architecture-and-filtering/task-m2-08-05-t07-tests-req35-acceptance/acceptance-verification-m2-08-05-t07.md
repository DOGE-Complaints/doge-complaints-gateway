# Acceptance verification — TASK-M2-08-05-T07

- **Task:** REQ-35 acceptance test coverage
- **Result:** PASS
- **Evidence:** `tests/test_req35_geo_scope_and_filter.py` covers REQ-35 §5 matrix (snapshot, scope 422/accept, settlement/country clustering)
- **Commands:** `python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q`; `python3 -m pytest -q` → **268 passed**, 10 skipped

| AC | Status | Evidence |
|----|--------|----------|
| P0 stub admin_settlement + admin_country | PASS | `test_demo_stubs_expose_admin_levels` |
| P0 scope Narva → 422 | PASS | `test_intake_geo_scope_rejects_narva_when_tallinn_node` |
| P0 scope without location → success | PASS | `test_intake_geo_scope_allows_story_without_location` |
| P0 settlement filter splits clusters | PASS | `test_geo_filter_settlement_splits_tallinn_and_narva` |
| P0 country default clusters together | PASS | `test_geo_filter_country_groups_estonian_settlements` |
| P1 full suite green | PASS | 268 passed (2026-05-16 run) |
