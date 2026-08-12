# Acceptance verification — TASK-M2-06-06-T07

- **Task:** Geo/time/institution filters
- **Result:** PASS
- **Evidence:** `src/core/projection/read_filters.py` — bbox, district normalization, post-fetch filters (AC-14..20)
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q -k 'ac14 or ac16 or ac20'`
