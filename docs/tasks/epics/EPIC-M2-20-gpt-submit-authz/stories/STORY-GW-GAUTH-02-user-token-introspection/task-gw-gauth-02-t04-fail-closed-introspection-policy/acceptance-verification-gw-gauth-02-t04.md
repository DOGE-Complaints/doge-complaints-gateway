# Acceptance — TASK-GW-GAUTH-02-T04

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Fail-closed on identity down / invalid / active=false | PASS | `UserTokenIntrospectionError` on transport/parse/inactive; `test_inactive_token_rejected_fail_closed`, `test_identity_down_rejected_fail_closed` |
| No payload-submitter fallback | PASS | inactive/down → 401 before handler; `test_missing_identity_config_fail_closed` |
