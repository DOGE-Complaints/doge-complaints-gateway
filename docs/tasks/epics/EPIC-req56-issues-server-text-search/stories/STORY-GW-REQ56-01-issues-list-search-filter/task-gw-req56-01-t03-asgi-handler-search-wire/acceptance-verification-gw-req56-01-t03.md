# acceptance-verification — GW-REQ56-01 T03

- **Date:** 2026-10-10T16:01:13Z
- **Package:** pkg-000111 (immutable)
- **Result:** PASS
- **Evidence:** Optional query param `search` on `GET /node/issues` (`asgi_app.py` `issues_list`) → `handle_issues_list(..., search=)` → `list_projections(..., search=)`. Envelope `data.issues` unchanged. No separate search route. AC-GW-REQ5601-04 · DP1.
