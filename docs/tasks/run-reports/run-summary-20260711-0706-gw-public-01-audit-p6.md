# run-summary-20260711-0706-gw-public-01-audit-p6

**Date:** 2026-07-11  
**Story:** STORY-GW-PUBLIC-01 audit follow-up (`run_mode=gw_public_01_audit_followup`)  
**Package:** pkg-000048 unchanged (override only)  
**Result:** PASS (T06)

## Summary

- **T06 (G1):** Session-scoped `_gauth_testclient_request_patch` in `tests/conftest.py` restores `TestClient.request` on pytest session teardown; function-scoped `_gauth_testclient_auto_headers` retains per-test skip via contextvar only.

## Verification

```
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify → ok 5 paths
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" → 568 passed
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py → 5 passed
post-session restore check: TestClient.request === StarletteTestClient.request → ok
```

## Notes

- `gateway-active-package.current.yaml` unchanged (pkg-000048)
- R1/R2/R3 → `activation: none` per plan
