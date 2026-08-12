# Acceptance — TASK-GW-GAUTH-03-T04

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| 401 / 403 / 503 separation | PASS | [`require_user_token`](../../../../../../../src/core/api/asgi_app.py) wires gate; inactive→401, unverified→403, identity down→503 |
| No persist on reject | PASS | Gate in `_PUBLIC_CONTENT_WRITE_DEPS` before handler; contract tests assert story count unchanged |
