# Acceptance verification — TASK-M2-04-06-T01

- **Task:** cluster `alpha_score` module
- **Result:** PASS
- **Evidence:** `src/core/cluster/alpha.py`; classification + narrative + geo dimensions per REQ-36 §2.2
- **Commands:** `python3 -c "from core.cluster.alpha import alpha_score"`; `pytest tests/test_alpha_score.py -q` (subset green)
