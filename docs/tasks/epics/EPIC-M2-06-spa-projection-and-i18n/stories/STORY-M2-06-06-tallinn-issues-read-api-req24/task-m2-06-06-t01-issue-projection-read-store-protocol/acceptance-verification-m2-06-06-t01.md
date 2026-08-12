# Acceptance verification — TASK-M2-06-06-T01

- **Task:** IssueProjectionReadStore protocol
- **Result:** PASS
- **Evidence:** `src/core/application/issue_create.py` — `IssueProjectionReadStore` Protocol; full `list_projections` / `get_projection` signatures
- **Commands:** `python3 -c "from core.application.issue_create import IssueProjectionReadStore; print('ok')"`
