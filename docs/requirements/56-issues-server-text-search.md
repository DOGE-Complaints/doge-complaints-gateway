# 56. Issues server text search on GET /node/issues

Parent: — (gateway-local REQ; no product root in `docs/requirements backlog/`)  
Parent-id: —  
Siblings: none (spa = consumer of existing/new feed UI; threads out of v1)  
Status: Draft — awaiting PA.2  
Justification: spa-app/docs/analysis/analysis-server-text-search-issues-comments-complexity-2026-10-10.md; operator locks 2026-10-10 (match A / API A / anonymous / issues-only); FE D-S1 as parity target  
Related (SPA consumer gate): spa-app DUI-Q01/Q12; [STORY-SPA-NF-api-requirements](../../../spa-app/docs/tasks/backlog-stories/next-feed/STORY-SPA-NF-api-requirements.md) + [STORY-SPA-NF-01](../../../spa-app/docs/tasks/backlog-stories/next-feed/STORY-SPA-NF-01-feed-list-toolbar-query.md) — live search ❌ / DUI-Q12 hide **while this REQ status ≠ Ready** (current: Draft — awaiting PA.2); FE glue after Ready inside next-feed host; `spa-app/src/router/issueSearchMatch.js`  
Architecture: [`../architecture/TECH-ARCH-issues-server-text-search.md`](../architecture/TECH-ARCH-issues-server-text-search.md) · interview [`../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md`](../analysis/zeya888.target-tech-arch-interview-issues-server-text-search-2026-10-10.md)  
Backlog: [`../tasks/backlog-stories/req56-issues-server-text-search/INDEX.md`](../tasks/backlog-stories/req56-issues-server-text-search/INDEX.md)  
Дата: 2026-10-10 · SSOT gateway-only: 2026-10-10T14:01:00Z · tech-arch materialize: 2026-10-10T14:52:31Z · param lock + backlog: 2026-10-10T15:30:33Z  
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

| Fact | Evidence |
|------|----------|
| List query params: status/type/labels/institution/dates/geo only | `src/core/api/asgi_app.py` `issues_list` (~528–546) |
| Handler → `list_projections(...)` without text | `src/core/api/handlers.py` `handle_issues_list` (~535–573) |
| Issue text in projection jsonb | `title_json` / `description_json` (`supabase/bootstrap/000_full_init.sql`) |
| Client D-S1 match rules (target parity) | `spa-app/src/router/issueSearchMatch.js` |
| Text query param on gateway | **Absent** (pre-implement) |

## 5) Target behavior

1. Accept optional query parameter **`search`** on `GET /node/issues`.  
2. Match per §3 D-S1.  
3. Compose with existing filters; anonymous callers remain valid.  
4. Text filter must not widen exposure vs the same request without `search` (DUI-Q01 / TECH-ARCH DP3).  
5. Response envelope remains issues list success shape (filtered `issues[]`).

## 6) Acceptance criteria

- [ ] S1: anonymous list + `search` + PUBLISHED → D-S1 substring matches only  
- [ ] S2: `search` + at least one structural filter works  
- [ ] S3: no anonymous exposure beyond list rules for the same other params  
- [ ] S4: no comments search / no separate search endpoint / no spa or product-root REQ required  
- [ ] Param **`search`** documented in API_REFERENCE / OpenAPI  

## 7) Open questions

1. ~~Literal HTTP query-param name~~ — **Closed:** `search` (DP1 + PA.2 sync 2026-10-10T15:30:33Z).  
2. Index/strategy for large corpora — spike; not invent index DDL here (TECH-ARCH hybrid: v1 in-memory).  
3. Exact anti-DRAFT enforcement — **Target (TECH-ARCH DP3):** status filter remains caller-driven; board-parity uses `status=PUBLISHED`; do not invent issue status `DRAFT`. Present vs residual gap verified at implement against `read_filters.py`.

## 8) Dependencies

None on a product-root REQ. SPA may enable live search **only after this REQ status = Ready** (DUI-Q12) inside existing FE packages (next-feed NF-01 / api-req) — not a sibling REQ. Until then next-feed story package stays Ready for P1.3 **without** live search. Backlog: STORY-GW-REQ56-01 → STORY-GW-REQ56-02.
