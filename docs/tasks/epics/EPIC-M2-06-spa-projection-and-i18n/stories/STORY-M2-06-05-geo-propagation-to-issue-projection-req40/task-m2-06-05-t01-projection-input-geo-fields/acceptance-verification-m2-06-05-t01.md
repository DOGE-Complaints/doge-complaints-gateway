# Acceptance verification — TASK-M2-06-05-T01

- **Task:** ProjectionInput geo fields
- **Result:** PASS
- **Evidence:** `src/core/projection/input.py` — `geo_lat` … `geo_admin_country`; `test_req40_geo_propagation.py::test_bridge_passes_geo_snapshot_to_projection_input`
- **Commands:** `python3 -m pytest tests/test_req40_geo_propagation.py -q`
