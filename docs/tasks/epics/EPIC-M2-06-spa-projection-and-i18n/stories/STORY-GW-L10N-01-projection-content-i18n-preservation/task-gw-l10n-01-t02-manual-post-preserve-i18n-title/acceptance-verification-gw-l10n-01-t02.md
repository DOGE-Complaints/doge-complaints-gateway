# Acceptance — TASK-GW-L10N-01-T02

- **Result:** PASS
- **Date:** 2026-06-15

| AC | Status | Evidence |
|----|--------|----------|
| payload_json.title reflects request i18n | PASS | `test_manual_create_preserves_request_i18n_title` |
| promoted_title still used for bridge aggregate | PASS | `issue_create.py` L376–382 unchanged bridge call |
