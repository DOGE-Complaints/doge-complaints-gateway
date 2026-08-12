# Story acceptance gate — STORY-M2-18-03

- **Story:** Local real HTTP smoke (REQ-41)
- **Package:** `pkg-000021-20260518-req41-production-test-coverage.yaml` (paths 1–2 of 7)
- **Result:** PASS
- **Date:** 2026-05-18

## AC checklist (REQ-41 §5)

| AC | Status | Evidence |
|----|--------|----------|
| AC-41-1 LS-01..06 | PASS | `tests/smoke/test_local_server_smoke.py` (live run) |
| AC-41-4 AC-01..03 | PASS | `tests/smoke/test_local_server_async_read.py` (live run) |
| Skip without `LOCAL_SERVER_URL` | PASS | 11 skipped in offline `pytest` |
| pkg-000021 paths 1–2 | PASS | T15, T16 acceptance-verification |

## Verification commands

```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/smoke/
# offline: 11 skipped

LOCAL_SERVER_URL=http://127.0.0.1:8000 python3 -m pytest -q tests/smoke/
# live: 11 passed (2026-05-18)
```
