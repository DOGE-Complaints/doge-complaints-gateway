# Story acceptance gate — STORY-M2-18-01

- **Story:** Cross-layer contract zones J–N (REQ-39)
- **Package:** `pkg-000020-20260518-req39-cross-layer-contract-testing.yaml` (paths 1–5)
- **Result:** PASS
- **Date:** 2026-05-18

## AC checklist (REQ-39 §17)

| AC | Status | Evidence |
|----|--------|----------|
| AC-39-3 Zone J — 4 tests | PASS | `tests/test_clustering_pipeline_contract.py` |
| AC-39-4 Zone K — 4 tests | PASS | `tests/test_geo_propagation_contract.py` |
| AC-39-5 Zone L — 4 tests | PASS | `tests/test_issue_projection_store_contract.py` |
| AC-39-6 Zone M — 8 tests | PASS | `tests/test_filter_projection_rows_contract.py` |
| AC-39-7 Zone N — 6 tests | PASS | `tests/test_e2e_sandbox_full_pipeline.py` |
| Offline only | PASS | no `tests/integration` in run |
| `gateway_resolve_queue.py --verify` paths 1–5 | PASS | pkg-000020 |

## Verification command

```bash
cd doge-complaints-gateway && python3 -m pytest -q \
  tests/test_issue_projection_store_contract.py \
  tests/test_filter_projection_rows_contract.py \
  tests/test_clustering_pipeline_contract.py \
  tests/test_geo_propagation_contract.py \
  tests/test_e2e_sandbox_full_pipeline.py
```

Result: **30 passed** (2026-05-18).
