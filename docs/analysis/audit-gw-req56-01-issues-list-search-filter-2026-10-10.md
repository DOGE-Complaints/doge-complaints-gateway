# Hard Audit — STORY-GW-REQ56-01 issues list search filter (D-S1) (2026-10-10)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ56-01-issues-list-search-filter`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md) (T01–T06, **pkg-000111**) · backlog [`…/STORY-GW-REQ56-01-…`](../tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md).  
**Pkg:** [`pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml`](../tasks/gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ56-01.md`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t06-story-gate/story-acceptance-gate-STORY-GW-REQ56-01.md) PASS **2026-10-10T16:01:13Z**.  
**Run-summary:** [`run-summary-20261010-1601-gw-req56-01-p3.md`](../tasks/run-reports/run-summary-20261010-1601-gw-req56-01-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-10T16:07:33Z`. Branch: **`dev`** (gateway git root). Live: `pytest -q tests/test_gw_req56_01_issues_list_search_filter.py` → **10 passed** (0.13s).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1040 / L1043–1054. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; param `search` + D-S1 hybrid; no separate route; 10 tests; 3 gaps (SSOT + AC-02 evidence + bullrun); TASKED-likely = G1 (+ soft G3)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | D-S1 match helper | [`issue_search_match.py`](../../src/core/projection/issue_search_match.py); parity [`spa-app/…/issueSearchMatch.js`](../../../spa-app/src/router/issueSearchMatch.js) (monorepo root) | ✅ PASS |
| **T02** | Post-fetch compose AND | [`filter_projection_rows(..., search=)`](../../src/core/projection/read_filters.py) after structural/geo; store thread InMemory/SQLite/Supabase | ✅ PASS |
| **T03** | ASGI/handler wire `search` | [`asgi_app.issues_list`](../../src/core/api/asgi_app.py) Query + [`handle_issues_list`](../../src/core/api/handlers.py) → `list_projections(search=)` | ✅ PASS |
| **T04** | Unit match + compose | suite units (empty/case/haystack/compose/non-widen) | ✅ PASS |
| **T05** | ASGI production-entry | ASGI filter / non-widen / whitespace / `/node/search` 404 | ✅ PASS |
| **T06** | Gate AC-01…06 | Gate PASS 16:01:13Z | ✅ PASS |

**Verdict product:** GW-REQ56-01 **исполнена по gate framing** (param `search` · D-S1 in-memory · compose AND · no separate route · offline 10).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 (S1) anonymous list + non-empty `search` + `status=PUBLISHED` → D-S1 matches | **PASS** | ASGI `test_req56_01_asgi_search_filters_published`; helper `issue_matches_search_query` |
| AC-02 (S2) `search` + ≥1 structural filter composes (AND) | **PASS**† | Code: search after `_matches_post_fetch_filters` ([`read_filters.py:358–384`](../../src/core/projection/read_filters.py)); unit `test_req56_01_filter_compose_and_with_status` (status AND) — see **G3** |
| AC-03 (S3) adding `search` does not widen vs same params without | **PASS** | unit + ASGI non-widening; NEW excluded under `status=PUBLISHED` |
| AC-04 (S4) no new search route; no comments corpus; envelope unchanged | **PASS** | only `@app.get("/node/issues")` gains `search`; `/node/search` 404; envelope `data.issues` ([`handlers.py:576–578`](../../src/core/api/handlers.py)); helper title+description only |
| AC-05 empty/absent/whitespace → no text restriction | **PASS** | helper empty→True; unit + ASGI whitespace |
| AC-06 unit + ASGI/handler wiring green | **PASS** | **10 passed** live this audit |

† AC-02 product path AND with structural/geo is Present; dedicated unit uses **status** (not type/labels/institution/geo) — residual **G3**.

### Focus re-checks

| Focus | Result |
|-------|--------|
| Param **`search`** | ✅ ASGI Query + handler + stores |
| D-S1 hybrid in-memory | ✅ `issue_search_match` + post-assemble `filter_projection_rows`; no FTS/DDL invent in match path |
| No separate route | ✅ no `/node/search` route; test 404 |
| Tests | ✅ 10 passed |
| Comments / SQL invent | ✅ not in helper/filter path |
| Client parity ref | ✅ Present at repo-root `spa-app/src/router/issueSearchMatch.js` (et/ru/en title+description; trim; case-insensitive includes) |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Helper | `src/core/projection/issue_search_match.py` | ✅ |
| Filter AND | `read_filters.filter_projection_rows(search=)` | ✅ |
| ASGI wire | `asgi_app.issues_list` `search: Query` | ✅ |
| Handler wire | `handlers.handle_issues_list` → `list_projections(search=)` | ✅ |
| Stores | `repositories.py` / `db_sqlite.py` / `db_supabase.py` `search=` → filter | ✅ |
| Protocol | `issue_create.IssueProjectionReadStore.list_projections(search=)` | ✅ |
| Offline tests | `tests/test_gw_req56_01_issues_list_search_filter.py` | ✅ 10 |
| Branch | `dev` | ✅ |
| No SQL FTS in match | no `to_tsvector` / index DDL in helper | ✅ |

---

## 3. Регрессии / gaps

### G1 — Task READMEs (+ pipeline Code touchpoints) still scaffold Absent/Gap vs Done · severity: **LOW** · **TASKED-likely**

T01 Code Facts still «Gateway text match helper Absent (pre-P3)» / Gap «No D-S1 server helper yet» while Status=Done and module Present — [`task-gw-req56-01-t01-…/README.md:21–25`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/task-gw-req56-01-t01-d-s1-match-helper/README.md). T03–T05 Gaps still «Absent (scaffold)». Pipeline §Code touchpoints header «implement in P3» — [`STORY-GW-REQ56-01-….md:74`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md). Backlog/pipeline §Verified already As-of-Done (no Historical split; no stale product Absent).

**Как закрыть:** TASKED docs — As-of-Done vs Historical on task READMEs (+ soft pipeline Code touchpoints); mirror REQ11-08…12.

### G2 — Bullrun §«Актуальная точка» без REQ56-01 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1040 + tasks L1047–1052 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — AC-02 test evidence = status AND, not type/labels/institution/geo · severity: **LOW** · **TASKED-likely** (soft)

REQ/TECH-ARCH AC S2 / DP4 name «structural» filter; gate cites `test_req56_01_filter_compose_and_with_status`. Product AND order already applies search after `_matches_post_fetch_filters` (structural/geo Present). No unit that pairs `search` with e.g. `issue_type`/`labels`.

**Как закрыть:** TASKED test — one compose case with non-status structural param; **or** P5 WAIVE if operator accepts status as sufficient S2 evidence (gate already did for Product Done).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1040 GW-REQ56-01 | 🔵 Done · gate PASS · `search` D-S1 · offline 10 · pkg-000111 | Product Done | PASS |
| T01 | L1047 | ✅ `issue_search_match.py` | Done | PASS |
| T02 | L1048 | ✅ `filter_projection_rows(search=)` AND | Done | PASS |
| T03 | L1049 | ✅ param `search` wired | Done | PASS |
| T04 | L1050 | ✅ unit in test_gw_req56_01 | Done | PASS |
| T05 | L1051 | ✅ ASGI production-entry | Done | PASS |
| T06 | L1052 | ✅ AC-01…06 PASS | Gate PASS | PASS |
| Journal | L2252–2253 | P1 + P3 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | task README / pipeline SSOT scaffold vs Done | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | AC-02 evidence = status not type/labels/geo | **yes** (soft) | test add or WAIVE |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 3.  
**Actionable TASKED-likely:** 2 (G1, G3 soft).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.

### Note (not a gap ID)

[`TECH-ARCH-issues-server-text-search.md` §5](../architecture/TECH-ARCH-issues-server-text-search.md) coexistence still describes list/handler «without text» (as-is snapshot). OpenAPI/API_REFERENCE → REQ56-02 OOS. Not opened as product AC fail.
