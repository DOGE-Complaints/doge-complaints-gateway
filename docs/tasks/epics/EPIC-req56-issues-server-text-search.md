# EPIC-req56-issues-server-text-search: Issues server text search (gateway)

## Epic Meta
- Status: 🟢 Done (REQ56-01 Done pkg-000111; REQ56-02 Done pkg-000112 P3 2026-10-10T16:30:12Z)
- Priority: High (REQ56 public list search)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`req56-issues-server-text-search/`](../backlog-stories/req56-issues-server-text-search/INDEX.md)
- **Parent REQ:** [`56-issues-server-text-search.md`](../requirements/56-issues-server-text-search.md)
- **Architecture:** [`../architecture/TECH-ARCH-issues-server-text-search.md`](../architecture/TECH-ARCH-issues-server-text-search.md)
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — operator lock MVP board
- **Git:** `dev`
- **Scaffolded:** 2026-10-10T15:52:08Z
- **Updated:** 2026-10-10T16:50:05Z (REQ56-02 P6 audit T04–T05 Done · pkg-000112 unchanged)

## Problem Statement

Gateway: optional query param **`search`** on `GET /node/issues` with D-S1 in-memory text match (et+ru+en title+description), composed with existing structural/geo filters; anonymous public list; no separate search route; no comments search; no SQL/FTS invent in v1. Docs (API_REFERENCE/OpenAPI) Done via REQ56-02.

## Soft (backlog)

- Soft (backlog): REQ56-01 issues list search filter — **Done** P3 2026-10-10T16:01:13Z pkg-000111 T01–T06 gate PASS
- Soft (backlog): REQ56-02 API docs search param — **Done** P3 · P6 G1/G3 CLOSED 2026-10-10T16:50:05Z · G2 WAIVED · pkg-000112 unchanged

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ56-01 | [pipeline](./EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md) → [backlog](../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md) · [pkg-000111](../gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml) | 🔵 Done P3 2026-10-10T16:01:13Z |
| STORY-GW-REQ56-02 | [pipeline](./EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/STORY-GW-REQ56-02-api-docs-search-param.md) → [backlog](../backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md) · [pkg-000112](../gateway-active-packages/pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml) | 🟢 Done P3 gate PASS 2026-10-10T16:30:12Z |

## Operator locks

| Theme | Lock |
|-------|------|
| Param | **`search`** (TECH-ARCH DP1) |
| Placement | Hybrid v1 in-memory post-assemble (DP2) |
| Safety | Text does not change status rules; board-parity `status=PUBLISHED` (DP3) |
| Verify | Unit match+compose + ASGI/handler wiring (DP4) |
