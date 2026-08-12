# Acceptance verification — TASK-M2-18-03-T22

- **Task:** GAP-AUDIT-REQ41-01 pytest-asyncio dev install
- **Result:** PASS
- **Date:** 2026-05-19
- **Evidence:**
  - `pip install -e ".[dev]"` — `pytest_asyncio 1.3.0` import OK
  - `pytest tests/smoke/test_local_server_async_read.py -q` → **3 skipped** (no `LOCAL_SERVER_URL`; expected, not missing-plugin false pass)
  - `pyproject.toml` dev extras unchanged; `test-offline.yml` already uses `pip install -e ".[dev]"`
  - REQ-41 §7 updated with `pip install -e ".[dev]"` prerequisite for smoke/async

## Verification commands

```bash
cd doge-complaints-gateway && pip install -e ".[dev]"
python3 -c "import pytest_asyncio; print(pytest_asyncio.__version__)"
python3 -m pytest -q tests/smoke/test_local_server_async_read.py
```
