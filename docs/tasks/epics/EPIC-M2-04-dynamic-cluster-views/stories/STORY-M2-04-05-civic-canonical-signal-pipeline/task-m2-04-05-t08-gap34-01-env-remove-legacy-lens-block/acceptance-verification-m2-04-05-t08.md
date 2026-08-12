# Acceptance verification — TASK-M2-04-05-T08

- **Task:** GAP-34-01 env legacy lens block removal
- **Result:** PASS
- **Evidence:** `.env` has single civic `CLUSTER_*` block; no `topic_micro` / `lexical` active values
- **Commands:** `python3 -m pytest -q` (261 passed); config load asserts civic six + `cluster_tie_breaker=alpha`
