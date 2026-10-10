# task-gw-req56-02-t02-openapi-search-param

## Task: docs — OpenAPI `search` param (T02)

## Meta
- **Story:** [STORY-GW-REQ56-02](../STORY-GW-REQ56-02-api-docs-search-param.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000112
- **Skill declared:** python-pro
- **Soft skill:** code-documenter
- **Depends on:** soft T01
- **Scaffolded:** 2026-10-10T16:25:31Z
- **Done:** 2026-10-10T16:30:12Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md`

## Purpose
Add query param **`search`** to `GET /node/issues` in existing `openapi.yaml` (no invent new package tree). Align with D-S1 / empty→no-op. **AC-GW-REQ5602-02**.

## Code Facts
### As-of-Done (P3 2026-10-10T16:30:12Z)
1. `openapi.yaml` `GET /node/issues` parameters include optional `search` (D-S1; empty→no-op; issues list only).
2. No new OpenAPI package tree; no `/search` path invent.

### Historical (pre-P3 / scaffold)
1. Text param on list Absent.

## Gap
**Closed:** `search` parameter Present on list operation.

## Acceptance / DoD
- [x] `openapi.yaml` documents optional `search` on `GET /node/issues`
- [x] No new OpenAPI package tree invent
- [x] No comments / separate route / invent index claims
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req56-02-t02.md` signed (P3)

## Where to change
- `docs/runtime-docs/api-reference/openapi.yaml`

## Out of scope
API_REFERENCE prose (T01); gate (T03); runtime code; SQL index docs.

## Verification commands
```bash
rg -n "/node/issues|search" doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml | head -40
```
