# 56. Issues server text search on GET /node/issues

Parent: — (gateway-local REQ; no product root in `docs/requirements backlog/`)  
Parent-id: —  
Siblings: none (spa = consumer of existing/new feed UI; threads out of v1)  
Status: **Ready**  
Justification: spa-app/docs/analysis/analysis-server-text-search-issues-comments-complexity-2026-10-10.md; operator locks 2026-10-10 (match A / API A / anonymous / issues-only); FE D-S1 as parity target  
Related (SPA consumer gate): spa-app DUI-Q01/Q12; [STORY-SPA-NF-api-requirements](../../../spa-app/docs/tasks/backlog-stories/next-feed/STORY-SPA-NF-api-requirements.md) + [STORY-SPA-NF-01](../../../spa-app/docs/tasks/backlog-stories/next-feed/STORY-SPA-NF-01-feed-list-toolbar-query.md) — server contract **Ready** (param **`search`**); production live toolbar still DUI-Q12 hide until FE enable wave inside next-feed host; `spa-app/src/router/issueSearchMatch.js`  
Architecture: [`../architecture/TECH-ARCH-issues-server-text-search.md`](../architecture/TECH-ARCH-issues-server-text-search.md) · interview [`../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md`](../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md)  
Backlog: [`../tasks/backlog-stories/req56-issues-server-text-search/INDEX.md`](../tasks/backlog-stories/req56-issues-server-text-search/INDEX.md) · REQ56-01 [`pkg-000111`](../tasks/gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml) · REQ56-02 [`pkg-000112`](../tasks/gateway-active-packages/pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml)  
Validation: [`../analysis/validation-req56-api-docs-vs-as-is-2026-10-10.md`](../analysis/validation-req56-api-docs-vs-as-is-2026-10-10.md)  
Дата: 2026-10-10 · SSOT gateway-only: 2026-10-10T14:01:00Z · tech-arch: 2026-10-10T14:52:31Z · param lock + backlog: 2026-10-10T15:30:33Z · **Ready validation: 2026-10-10T17:20:20Z**  
Method: `.cursor/rules/analysis.mdc` — name ≠ create for indexes (SQL/FTS later spike)  

---

## 1) Goal

Добавить на **`GET /node/issues`** серверный текстовый фильтр по multilingual Issue `title` + `description` с **паритетом D-S1** (как SPA `issueSearchMatch.js`), для анонимного публичного list — чтобы фронт мог слать text query на тот же list endpoint. Без отдельного search endpoint, без comments, без spa/product-root REQ.

## 2) Scope / Out of scope

**In:**
- Text match on list projections; compose with existing structural/geo filters.
- Anonymous access; `status=PUBLISHED` / anti-DRAFT parity with public list (DUI-Q01).
- Tests + runtime/API docs (`API_REFERENCE` / OpenAPI) for locked param **`search`**.

**Out:** Threads/comments search; scope flag; separate search route; inventing alternate query-param names; SPA UI/redesign REQ; product-root REQ in backlog; invite/Connect; changing enum vocabularies; invent SQL/index DDL in v1.

## 3) Operator locks (2026-10-10)

| Theme | Lock |
|-------|------|
| Corpus v1 | **Issues only** |
| Match | **D-S1 parity:** trim; empty/absent → no text restriction; case-insensitive substring; haystack = et+ru+en `title`+`description` ([`issueSearchMatch.js`](../../../spa-app/src/router/issueSearchMatch.js)) |
| API | Extend **`GET /node/issues`**; no separate search endpoint |
| Auth | **Anonymous** public list |
| Public safety | `status=PUBLISHED` + gateway anti-DRAFT (DUI-Q01); text filter does not change status rules (TECH-ARCH DP3) |
| Query param name | **`search`** (Architect Studio DP1 2026-10-10; synced PA.2 2026-10-10T15:30:33Z) |

## 4) Verified current state

### As-of-Done (post REQ56-01/02 · Ready 2026-10-10T17:20:20Z)

| Fact | Evidence |
|------|----------|
| Query param `search` on list | `src/core/api/asgi_app.py:546`, `:566` |
| Handler → `list_projections(..., search=)` | `src/core/api/handlers.py:553`, `:574` |
| D-S1 helper | `src/core/projection/issue_search_match.py` |
| Post-fetch compose | `src/core/projection/read_filters.py:339–383` |
| Tests unit + ASGI | `tests/test_gw_req56_01_issues_list_search_filter.py` |
| API_REFERENCE + OpenAPI | `docs/runtime-docs/api-reference/API_REFERENCE.md` (~L643); `openapi.yaml` (~L1157–1165) |
| Client D-S1 parity target | `spa-app/src/router/issueSearchMatch.js` |

### Historical (pre-implement)

| Fact | Evidence |
|------|----------|
| List params without text; handler without text; gateway text param Absent | pre-P3 snapshot (arch interview / REQ scaffold 2026-10-10T14:01:00Z) |

## 5) Target behavior

1. Accept optional query parameter **`search`** on `GET /node/issues`.  
2. Match per §3 D-S1.  
3. Compose with existing filters; anonymous callers remain valid.  
4. Text filter must not widen exposure vs the same request without `search` (DUI-Q01 / TECH-ARCH DP3).  
5. Response envelope remains issues list success shape (filtered `issues[]`).

## 6) Acceptance criteria

- [x] S1: anonymous list + `search` + PUBLISHED → D-S1 substring matches only — pkg-000111 / `test_gw_req56_01_*`  
- [x] S2: `search` + at least one structural filter works — same  
- [x] S3: no anonymous exposure beyond list rules for the same other params — same (non-widening)  
- [x] S4: no comments search / no separate search endpoint / no spa or product-root REQ required — verified by scope + docs negatives  
- [x] Param **`search`** documented in API_REFERENCE / OpenAPI — pkg-000112  

## 7) Open questions

1. ~~Literal HTTP query-param name~~ — **Closed:** `search`.  
2. Index/strategy for large corpora — spike; not invent index DDL here (TECH-ARCH hybrid: v1 in-memory).  
3. Exact anti-DRAFT enforcement — **Closed for v1 (TECH-ARCH DP3):** status filter remains caller-driven; board-parity uses `status=PUBLISHED`; do not invent issue status `DRAFT`. Verified in `read_filters.py` + tests.

## 8) Dependencies

None on a product-root REQ. Server contract **Ready** — SPA may wire live `search` on `GET /node/issues` inside next-feed host; production toolbar still DUI-Q12 hide until explicit FE enable (not a sibling spa REQ). Backlog: STORY-GW-REQ56-01 / 02 **Done**.
