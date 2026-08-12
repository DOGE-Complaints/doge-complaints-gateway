# Acceptance verification — task-gw-public-01-t04-post-tallinn-issues-without-service-token-offline-green

- **Task:** T04 POST /tallinn/issues without service token → 401; offline suite green
- **Status:** PASS
- **Date:** 2026-07-10

## Checklist

- [x] POST /tallinn/issues without token returns 401 (`@pytest.mark.gauth_raw_client`)
- [x] Full offline pytest suite green (568 passed, `-m "not live_integration"`)
- [x] All T01–T04 tests in test_gw_public_01_public_issues_regression.py PASS
