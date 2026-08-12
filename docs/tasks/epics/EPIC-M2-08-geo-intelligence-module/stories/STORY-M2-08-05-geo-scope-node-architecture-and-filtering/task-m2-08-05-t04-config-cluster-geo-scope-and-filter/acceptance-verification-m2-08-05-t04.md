# Acceptance verification — TASK-M2-08-05-T04

- **Task:** CLUSTER_GEO_SCOPE env and CLUSTER_GEO_FILTER validation
- **Result:** PASS
- **Evidence:** `config/schema.py` exposes `cluster_geo_scope: tuple[str, str] | None`; `parse_cluster_geo_filter` enum + default `country`; `example.env` documents both vars
- **Commands:** `python3 -m pytest tests/test_config_loading.py tests/test_req35_geo_scope_and_filter.py -q -k config`

| AC | Status | Evidence |
|----|--------|----------|
| P0 CLUSTER_GEO_SCOPE optional parse level:value | PASS | `parse_cluster_geo_scope` in `geo/scope.py` |
| P0 CLUSTER_GEO_FILTER enum, default country | PASS | `test_config_loading` asserts `country` |
| P0 AppConfig exposes scope tuple | PASS | `AppConfig.cluster_geo_scope` |
| P1 example.env documented | PASS | REQ-35 comment block |
| P1 config tests valid/invalid | PASS | `test_config_loading.py` |
