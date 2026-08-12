# Acceptance verification — TASK-M2-08-05-T06

- **Task:** Intake GEO_SCOPE_MISMATCH rejection
- **Result:** PASS
- **Evidence:** `handle_story_intake` resolves location when `cluster_geo_scope` set; mismatch raises before `create_story`; unified envelope `code=GEO_SCOPE_MISMATCH`
- **Commands:** `python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q -k intake`

| AC | Status | Evidence |
|----|--------|----------|
| P0 settlement:tallinn + Narva → 422 GEO_SCOPE_MISMATCH | PASS | `test_intake_geo_scope_rejects_narva_location` |
| P0 same scope, no location_query → accepted | PASS | `test_intake_geo_scope_allows_story_without_location` |
| P1 scope unset → unchanged behavior | PASS | scope check gated on `cluster_geo_scope is not None` |
| P1 unified error envelope | PASS | `envelope.py` GeoScopeMismatchError mapping |
