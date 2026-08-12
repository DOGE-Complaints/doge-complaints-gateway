# Acceptance — TASK-GW-GAUTH-01-T02

- **Result:** PASS
- **Date:** 2026-06-25

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Service + user deps on public-content writes | PASS | [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) `_PUBLIC_CONTENT_WRITE_DEPS` on `POST /intake/stories` and `POST /tallinn/issues` |
| `require_public_content_service_auth` + `require_user_token` | PASS | [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) L259–269 |
| `extract_user_token` / `UserTokenMissingError` stub | PASS | [`security.py`](../../../../../../../src/core/api/security.py) |
