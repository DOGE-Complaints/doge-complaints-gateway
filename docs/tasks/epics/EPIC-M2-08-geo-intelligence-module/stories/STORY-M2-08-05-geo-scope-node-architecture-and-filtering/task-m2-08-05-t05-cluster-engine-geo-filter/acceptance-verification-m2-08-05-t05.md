# Acceptance verification — TASK-M2-08-05-T05

- **Task:** CLUSTER_GEO_FILTER in clustering engine
- **Result:** PASS
- **Evidence:** `cluster/engine.py` uses `geo_filter_bucket(profile.geo, geo_filter)` in `cluster_key_for_lens`; `service_factory` passes `config.cluster_geo_filter`
- **Commands:** `python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q -k cluster`

| AC | Status | Evidence |
|----|--------|----------|
| P0 settlement splits Tallinn vs Narva | PASS | `test_geo_filter_settlement_splits_tallinn_and_narva` |
| P0 country groups EE stories | PASS | `test_geo_filter_country_groups_estonian_settlements` |
| P0 geo=None participates without partition | PASS | `geo:agnostic` bucket in `geo_filter_bucket` |
| P1 case-insensitive admin compare | PASS | `normalize_admin_value` in `geo/scope.py` |
