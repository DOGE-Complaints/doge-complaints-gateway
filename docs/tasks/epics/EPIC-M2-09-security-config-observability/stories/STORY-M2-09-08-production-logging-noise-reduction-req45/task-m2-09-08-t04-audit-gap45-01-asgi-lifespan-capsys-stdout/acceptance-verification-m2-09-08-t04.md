# Acceptance verification — TASK-M2-09-08-T04

- **Task:** audit GAP-01 — asgi lifespan capsys INFO → stdout.
- **Result:** PASS
- **Evidence (code):**
  - `tests/test_asgi_lifespan_cron.py` L83 — `assert "shutdown.lifecycle" in captured.out`
  - `tests/test_asgi_lifespan_cron.py` L99 — `assert "startup.persistence_backend backend=in_memory" in captured.out`
  - `tests/test_asgi_lifespan_cron.py` L115 — `assert "startup.persistence_backend backend=supabase" in captured.out`
- **Commands:**
  - `cd doge-complaints-gateway && python3 -m pytest -q tests/test_asgi_lifespan_cron.py`
- **Output:** all tests in module passed (2026-05-29 run).
