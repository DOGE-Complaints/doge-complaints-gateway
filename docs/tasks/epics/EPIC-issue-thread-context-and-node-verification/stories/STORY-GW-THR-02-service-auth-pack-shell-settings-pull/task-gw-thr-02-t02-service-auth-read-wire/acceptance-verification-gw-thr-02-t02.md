# acceptance-verification — GW-THR-02 T02

- **Date:** 2026-09-21T20:48:13Z
- **Package:** pkg-000094 (immutable)
- **Result:** PASS
- **Evidence:** `GET /node/shell-settings` + `require_public_content_service_auth` in `asgi_app.py`; not in `PUBLIC_ROUTES`; no public ThreadContext route.
