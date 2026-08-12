# Acceptance — TASK-GW-RC-02-T01

- **Result:** PASS
- **Date:** 2026-06-19

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| `GET` list/get отдают `type` в каноне для legacy lowercase | PASS | `canonicalize_issue_type_on_read` in [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py); `test_canonicalize_issue_type_on_read_lowercase_legacy` |
