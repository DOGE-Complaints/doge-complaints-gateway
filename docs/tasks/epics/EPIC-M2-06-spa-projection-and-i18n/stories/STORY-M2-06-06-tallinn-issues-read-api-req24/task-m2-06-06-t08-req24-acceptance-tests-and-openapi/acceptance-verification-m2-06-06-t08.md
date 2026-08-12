# Acceptance verification — TASK-M2-06-06-T08

- **Task:** REQ-24 acceptance + OpenAPI
- **Result:** PASS
- **Evidence:** `tests/test_req24_tallinn_issues_read_api.py`; `docs/runtime-docs/api-reference/openapi.yaml` `/tallinn/issues` paths (AC-1..20, AC-13)
- **Commands:** `python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q`
