# Acceptance verification — TASK-M2-18-05-T23

- **Task:** GAP-AUDIT-REQ41-02 Supabase secret naming docs
- **Result:** PASS
- **Date:** 2026-05-19
- **Evidence:**
  - REQ-41 §7: таблица GitHub Secret `SUPABASE_TEST_SERVICE_ROLE_KEY` → runner env `SUPABASE_TEST_SERVICE_ROLE`
  - REQ-41 §4 приоритеты GAP-41-05 row aligned
  - `integration-live.yml` header cross-ref to REQ-41 §7

## Verification commands

```bash
rg 'SUPABASE_TEST_SERVICE_ROLE_KEY' doge-complaints-gateway/docs/requirements/41-testing-production-coverage-target-state.md
rg 'REQ-41' doge-complaints-gateway/.github/workflows/integration-live.yml
```
