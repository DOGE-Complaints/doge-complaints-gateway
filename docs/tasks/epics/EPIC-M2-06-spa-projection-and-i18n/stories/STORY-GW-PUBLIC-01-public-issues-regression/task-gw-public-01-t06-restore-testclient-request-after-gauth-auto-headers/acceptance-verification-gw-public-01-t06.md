# Acceptance verification — task-gw-public-01-t06-restore-testclient-request-after-gauth-auto-headers

- **Task:** T06 restore TestClient.request after gauth auto-headers patch
- **Status:** PASS
- **Date:** 2026-07-11

## Checklist

- [x] `TestClient.request` restored after pytest session (`_gauth_testclient_request_patch` session finalizer; post-run assert vs `StarletteTestClient.request`)
- [x] Offline suite green (`pytest -q -m "not live_integration"`) — **568 passed**
- [x] PUBLIC-01 module 5/5 unchanged (`tests/test_gw_public_01_public_issues_regression.py`)

## Evidence

- Change: `doge-complaints-gateway/tests/conftest.py` — session patch + restore; function-scoped contextvar skip only
- Run-summary: [`run-summary-20260711-0706-gw-public-01-audit-p6.md`](../../../../run-reports/run-summary-20260711-0706-gw-public-01-audit-p6.md)
