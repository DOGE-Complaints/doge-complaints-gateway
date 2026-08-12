# Acceptance verification — TASK-M2-06-06-T10

- **Task:** Filter edge AC-15/17/18/19 tests
- **Result:** PASS
- **Evidence:** `test_req24_ac15_geo_less_excluded_when_bbox_active`, `test_req24_ac17_geo_district_multi_value_or`, `test_req24_ac18_bbox_and_district_and`, `test_req24_ac19_created_after_before`
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q -k 'ac15 or ac17 or ac18 or ac19'`
