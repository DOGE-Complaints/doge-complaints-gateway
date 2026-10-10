# acceptance-verification — GW-REQ56-01 T05

- **Date:** 2026-10-10T16:01:13Z
- **Package:** pkg-000111 (immutable)
- **Result:** PASS
- **Evidence:** ASGI `TestClient` on `GET /node/issues` — `search`+`status=PUBLISHED` filters; S3 non-widening; whitespace no-restrict; `/node/search` 404. Same suite **10 passed**. AC-GW-REQ5601-01/03/06 · DP3/DP4.
