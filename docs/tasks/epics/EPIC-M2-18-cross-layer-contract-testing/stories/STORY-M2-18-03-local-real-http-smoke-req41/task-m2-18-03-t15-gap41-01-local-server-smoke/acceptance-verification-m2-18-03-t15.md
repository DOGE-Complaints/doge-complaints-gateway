# Acceptance verification — TASK-M2-18-03-T15

- **Task:** GAP-41-01 local server smoke (LS-01..06)
- **Result:** PASS
- **Date:** 2026-05-18
- **Evidence:**
  - `tests/smoke/conftest.py` — `LOCAL_SERVER_URL` guard + `/health` reachability
  - `tests/smoke/test_local_server_smoke.py` — 7 tests (LS-01..06 + uvicorn Server header)
  - Without server: `pytest tests/smoke/test_local_server_smoke.py -q` → 7 skipped
  - With uvicorn (`LOCAL_SERVER_URL=http://127.0.0.1:8000`): **7 passed** (2026-05-18)
  - Offline regression: full suite **402 passed**, 11 smoke skipped

## Verification commands

```bash
# Skip path (no server required for CI offline)
cd doge-complaints-gateway && python3 -m pytest -q tests/smoke/test_local_server_smoke.py

# Live path (operator starts uvicorn per REQ-41 §7)
APP_PROFILE=demo DB_BACKEND=in_memory CLUSTER_CRON_ENABLED=false \
  PYTHONPATH=src python3 -m uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000
LOCAL_SERVER_URL=http://127.0.0.1:8000 python3 -m pytest -q tests/smoke/test_local_server_smoke.py
```
