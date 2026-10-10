# REQ56 issues server text search (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/req56-issues-server-text-search/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`56-issues-server-text-search.md`](../../../requirements/56-issues-server-text-search.md)  
**Parent product:** — (gateway-local; no product-root REQ)  
**Architecture:** [`../../../architecture/TECH-ARCH-issues-server-text-search.md`](../../../architecture/TECH-ARCH-issues-server-text-search.md)  
**Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md`](../../../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md)  
**Justification:** [`../../../../spa-app/docs/analysis/analysis-server-text-search-issues-comments-complexity-2026-10-10.md`](../../../../spa-app/docs/analysis/analysis-server-text-search-issues-comments-complexity-2026-10-10.md)  
**Dashboard:** [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (operator lock: MVP board)  
**Naming:** `STORY-GW-REQ56-*`  
**Updated:** 2026-10-10T16:15:39Z · REQ56-01 P6 audit T07–T08 Done · pkg-000111 unchanged  
**Epic:** [`EPIC-req56-issues-server-text-search.md`](../../epics/EPIC-req56-issues-server-text-search.md) · Active pkg [`pkg-000111`](../../gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml)

---

## Контекст одной фразой

Gateway: optional query param **`search`** on `GET /node/issues` with D-S1 in-memory text match (et+ru+en title+description), composed with existing filters; anonymous; no separate search route; docs in REQ56-02.

---

## Operator locks

| Theme | Decision |
|-------|----------|
| Dashboard | sync `gateway-mvp-dashboard.md` |
| Param name | **`search`** (TECH-ARCH DP1; REQ PA.2 sync) |
| Filter placement | Hybrid v1 in-memory; SQL/index later spike |
| Public safety | Caller `status=PUBLISHED`; text does not change status rules |
| Verify | Unit match+compose + ASGI/handler wiring |
| Package | **new** `req56-issues-server-text-search/` |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-REQ56-01 | [STORY-GW-REQ56-01-issues-list-search-filter.md](./STORY-GW-REQ56-01-issues-list-search-filter.md) → [pipeline](../../epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md) · [pkg-000111](../../gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml) | **Done** P3 gate PASS · P6 G1/G3 CLOSED 2026-10-10T16:15:39Z · G2 WAIVED · offline **11** · backlog kept | — |
| STORY-GW-REQ56-02 | [STORY-GW-REQ56-02-api-docs-search-param.md](./STORY-GW-REQ56-02-api-docs-search-param.md) | ⚪ Todo | REQ56-01 |

---

## Out of package

- SPA UI / DUI-Q12 live search enable  
- Threads/comments search; scope flag; separate search endpoint  
- SQL/FTS/index DDL invent  
- Product-root REQ; ADMIN layers  
