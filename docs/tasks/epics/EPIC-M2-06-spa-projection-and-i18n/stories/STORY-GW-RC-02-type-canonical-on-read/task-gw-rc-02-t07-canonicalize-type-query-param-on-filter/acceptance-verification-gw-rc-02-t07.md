# Acceptance — TASK-GW-RC-02-T07

- **Result:** PASS
- **Date:** 2026-05-29

| AC (parent / audit G1) | Status | Evidence |
|------------------------|--------|----------|
| `?type=improvement` матчит legacy lowercase payload | PASS | `filter_projection_rows` канонизирует `issue_type` через `canonicalize_issue_type_on_read(..., log_unknown=False)` |
| Unit + HTTP tests | PASS | `test_type_filter_matches_legacy_lowercase_query_param`; `test_http_type_filter_accepts_lowercase_query_param` |
| No regressions GW-RC-02 suite | PASS | `505 passed` unit live 2026-05-29 |
