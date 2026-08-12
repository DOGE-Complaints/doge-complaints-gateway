# Acceptance verification — TASK-M2-18-05-T20

- **Task:** GAP-41-05 live Supabase CI
- **Result:** PASS
- **Date:** 2026-05-18
- **Evidence:**
  - `pyproject.toml` — marker `live_integration` registered
  - `tests/conftest.py` — `pytest_collection_modifyitems` tags `tests/integration/supabase/*`
  - `.github/workflows/test-offline.yml` — `pytest -m "not live_integration"`
  - `.github/workflows/integration-live.yml` — `pytest -m live_integration` on `main`; secrets documented in workflow header
  - `pytest -m live_integration --collect-only` → **10 tests** collected

## Verification

```bash
cd doge-complaints-gateway && python3 -m pytest -q -m live_integration --collect-only
python3 -m pytest -q -m "not live_integration"  # offline CI parity
```
