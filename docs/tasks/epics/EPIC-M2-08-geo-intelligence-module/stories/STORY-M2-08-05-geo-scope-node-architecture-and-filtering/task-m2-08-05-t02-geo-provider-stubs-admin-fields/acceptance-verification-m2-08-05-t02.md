# Acceptance verification — TASK-M2-08-05-T02

- **Task:** Demo geo stubs with admin levels
- **Result:** PASS
- **Evidence:** `src/core/geo/providers.py` — `_TallinnOpenCageStub` / `_NarvaNominatimStub` set `admin_settlement`, `admin_country=EE`, district/region; legacy `cluster_tags` retained
- **Commands:** `python3 -m pytest tests/test_req35_geo_scope_and_filter.py::test_demo_stubs_expose_admin_levels -q`

| AC | Status | Evidence |
|----|--------|----------|
| P0 Tallinn admin_settlement + admin_country | PASS | stub resolve + test |
| P0 Narva admin_settlement + EE | PASS | stub resolve + scope rejection test |
| P1 cluster_tags preserved | PASS | existing tags unchanged in providers |
