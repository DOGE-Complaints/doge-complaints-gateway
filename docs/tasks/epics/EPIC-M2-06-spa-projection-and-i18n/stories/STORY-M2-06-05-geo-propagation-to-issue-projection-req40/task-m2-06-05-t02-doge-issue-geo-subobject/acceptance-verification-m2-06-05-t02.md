# Acceptance verification — TASK-M2-06-05-T02

- **Task:** DOGEIssue geo sub-object
- **Result:** PASS
- **Evidence:** `src/core/projection/dto.py`; AC-2 via `test_req40_ac2_issue_payload_omits_geo_key_when_stories_have_no_geo`
- **Commands:** `python3 -m pytest tests/test_req40_geo_propagation.py -q`
