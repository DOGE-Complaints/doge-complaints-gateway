# Acceptance — TASK-GW-GAUTH-01-T04

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Без сервисного токена → 401 | PASS | `test_intake_without_service_token_rejected_not_noop` |
| Только сервис, без user → 401 | PASS | `test_intake_service_only_without_user_token_rejected` |
| Service+user → 202 | PASS | `test_intake_with_service_and_user_token_accepted` |
| Service-only не создаёт за arbitrary submitter | PASS | `test_service_only_does_not_create_story_for_arbitrary_submitter` |
| Env unset → mandatory reject | PASS | `test_intake_rejects_when_service_token_env_unset` |
| Tallin issues two-layer | PASS | `test_tallinn_issues_post_requires_two_layer_auth` |

**Live run:** `pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py` → 6 passed (2026-06-25)
