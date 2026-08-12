# Acceptance verification — TASK-M2-06-05-T04

- **Task:** extraction policy geo_snapshot
- **Result:** PASS
- **Evidence:** `src/core/projection/extraction_policy.py`; `test_bridge_passes_geo_snapshot_to_projection_input`
- **Commands:** `python3 -m pytest tests/test_req40_geo_propagation.py -q`
