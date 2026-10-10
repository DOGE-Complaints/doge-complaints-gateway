# Story acceptance gate — STORY-GW-REQ56-02

- **Story:** Document `search` on GET /node/issues
- **Package:** `pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml`
- **Result:** PASS
- **Date:** 2026-10-10T16:30:12Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ5602-01: API_REFERENCE documents `search` (optional string; D-S1; empty/absent = no text filter) | PASS | `API_REFERENCE.md` query table + §9 16-param; T01 acceptance |
| AC-GW-REQ5602-02: `openapi.yaml` documents `search` on `GET /node/issues` | PASS | `openapi.yaml` `name: search` under list get; T02 acceptance |
| AC-GW-REQ5602-03: Docs do not claim comments search / separate search endpoint / invented index | PASS | Explicit negatives in both docs (issues-only; same list route; no index/DDL invent) |

## Commands (live verification 2026-10-10T16:30:12Z)

```text
--verify ok 3 (pkg-000112)
rg search in API_REFERENCE.md + openapi.yaml → Present on list
utc_now: 2026-10-10T16:30:12Z
stay_on_branch: dev · no push · no P8
docs-only · no runtime · no comments/separate route/index claims
```
