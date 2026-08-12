# Acceptance — TASK-GW-TAX-02-T04

- **Result:** PASS
- **Date:** 2026-07-15T11:52:51Z

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| AC-3 per-lens min_size | PASS | `CLUSTER_MIN_SIZE_BY_LENS` in [`schema.py`](../../../../../../../../src/core/config/schema.py) (global `CLUSTER_MIN_SIZE` default unchanged at 5); `_resolve_min_size_guard(lens)` in [`cluster_orchestrator.py`](../../../../../../../../src/core/application/cluster_orchestrator.py); `min_stories` override in [`gates.py`](../../../../../../../../src/core/promotion/gates.py) + [`issue_create.py`](../../../../../../../../src/core/application/issue_create.py); `tests/test_gw_tax_02_cluster_axis_expansion.py` min_size tests |
