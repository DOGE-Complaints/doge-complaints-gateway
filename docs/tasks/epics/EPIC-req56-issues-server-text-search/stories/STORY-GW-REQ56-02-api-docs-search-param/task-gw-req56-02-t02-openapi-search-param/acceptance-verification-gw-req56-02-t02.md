# acceptance-verification — GW-REQ56-02 T02

- **Date:** 2026-10-10T16:30:12Z
- **Package:** pkg-000112 (immutable)
- **Result:** PASS
- **Evidence:** `docs/runtime-docs/api-reference/openapi.yaml` — `GET /node/issues` query param `name: search` (optional string; D-S1; empty/absent/whitespace → no text restriction; AND compose; issues list only — not comments / not separate path). Same file tree; no new OpenAPI package. AC-GW-REQ5602-02.
