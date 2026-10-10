# Hard Audit — STORY-GW-REQ56-02 API docs `search` param (2026-10-10)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ56-02-api-docs-search-param`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/STORY-GW-REQ56-02-api-docs-search-param.md) (T01–T03, **pkg-000112**) · backlog [`…/STORY-GW-REQ56-02-…`](../tasks/backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md).  
**Pkg:** [`pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml`](../tasks/gateway-active-packages/pkg-000112-20261010-gw-req56-02-api-docs-search-param.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ56-02.md`](../tasks/epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-02-api-docs-search-param/task-gw-req56-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ56-02.md) PASS **2026-10-10T16:30:12Z**.  
**Run-summary:** [`run-summary-20261010-1630-gw-req56-02-p3.md`](../tasks/run-reports/run-summary-20261010-1630-gw-req56-02-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-10T16:38:48Z`. Branch: **`dev`**. Live: `rg search` on API_REFERENCE + openapi → Present on `GET /node/issues`; no FTS/index invent near `search`.

> **Природа аудита.** P4 hard audit docs vs AC (docs-only story). Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T03 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1041 / L1043–1051. AC из Target verbatim — **не** invent.

---

## 1. Итог: docs AC PASS; `search` in API_REFERENCE + openapi; AC-03 negatives Present; 3 gaps (co-located status falsehood + stale binding + bullrun); TASKED-likely = G1 (+ soft G3)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | API_REFERENCE `search` | [`API_REFERENCE.md:643`](../runtime-docs/api-reference/API_REFERENCE.md) optional string; D-S1; empty→no text restrict; AND compose; issues-only / no separate route | ✅ PASS |
| **T02** | openapi `search` | [`openapi.yaml:1157–1164`](../runtime-docs/api-reference/openapi.yaml) under `/node/issues` get; required false; D-S1 description | ✅ PASS |
| **T03** | Gate AC-01…03 | Gate PASS 16:30:12Z | ✅ PASS |

**Verdict product (docs):** GW-REQ56-02 **исполнена по gate framing** (`search` documented · OpenAPI param · no comments/separate-route/index invent in search wording).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 API_REFERENCE documents `search` (optional string; D-S1; empty/absent = no text filter) | **PASS** | Query table row [`API_REFERENCE.md:643`](../runtime-docs/api-reference/API_REFERENCE.md); § summary «16-parameter … incl. optional `search`» `:818`; Auth public `:633` |
| AC-02 `openapi.yaml` documents `search` on `GET /node/issues` | **PASS** | [`openapi.yaml:1156–1164`](../runtime-docs/api-reference/openapi.yaml) `name: search` under `/node/issues` get |
| AC-03 Docs do not claim comments search / separate search endpoint / invented index | **PASS** | Explicit negatives in API_REFERENCE `:643` and openapi `:1164`; `rg` no FTS/`to_tsvector`/GIN invent tied to `search`; no `/node/search` path in openapi |

### Focus re-checks

| Focus | Result |
|-------|--------|
| `search` in API_REFERENCE | ✅ |
| `search` in openapi list | ✅ |
| No false claims **in search wording** | ✅ matches REQ56-01 D-S1 (title+description et/ru/en; trim empty→no-op; AND; issues-only) |
| Co-located false claims in same section | ⚠️ see **G1** / **G3** (not AC-03 verbatim) |

### Doc facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| API_REFERENCE section | `### GET /node/issues` + `search` row | ✅ |
| OpenAPI param | `/node/issues` get → `name: search` | ✅ |
| 16 params incl. search | status…geo_postal_code + search = 16 | ✅ |
| No comments/separate/index invent in search text | both docs | ✅ |
| Task README As-of-Done | T01/T02 already split Historical | ✅ (no SSOT Absent residual) |
| Branch | `dev` | ✅ |
| Runtime OOS | docs-only; no filter invent this story | ✅ |

---

## 3. Регрессии / gaps

### G1 — Co-located `status` enum still claims `DRAFT` (false vs governed statuses) · severity: **LOW** · **TASKED-likely** (soft / hygiene)

Same `GET /node/issues` query table documents `status` as `DRAFT`, `PUBLISHED` — [`API_REFERENCE.md:642`](../runtime-docs/api-reference/API_REFERENCE.md). Governed statuses are `NEW` / `IN_REVIEW` / `PUBLISHED` — [`enums.py:9–11`](../../src/core/projection/enums.py); TECH-ARCH / REQ56 lock «do not invent DRAFT». OpenAPI issue schema also `enum: [DRAFT, PUBLISHED]` — [`openapi.yaml:294`](../runtime-docs/api-reference/openapi.yaml). **Not** AC-5602-03 (comments/route/index), but Focus «no false claims» on the edited list surface. Pre-existing; search row itself accurate.

**Как закрыть:** TASKED docs — align status wording with `DOGEIssueStatus` in API_REFERENCE (+ soft openapi schema if in same docs pass); **or** P5 WAIVE out-of-DoD / separate hygiene story.

### G2 — Bullrun §«Актуальная точка» без REQ56-02 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1041 + tasks L1047–1049 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — Stale HTTP binding line refs on list section · severity: **LOW** · **TASKED-likely** (soft)

[`API_REFERENCE.md:632`](../runtime-docs/api-reference/API_REFERENCE.md) claims `asgi_app.py:462` → `handlers.py:385`. Live: `issues_list` ~[`asgi_app.py:529`](../../src/core/api/asgi_app.py); `handle_issues_list` ~[`handlers.py:535`](../../src/core/api/handlers.py). Binding claim false after line drift; search docs did not refresh it.

**Как закрыть:** TASKED docs — refresh binding lines or drop brittle line numbers; **or** WAIVE working-doc hygiene.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1041 GW-REQ56-02 | 🔵 Done · gate PASS · docs-only · pkg-000112 | Product Done | PASS |
| T01 | L1047 | ✅ API_REFERENCE optional `search` | Done | PASS |
| T02 | L1048 | ✅ openapi param on list | Done | PASS |
| T03 | L1049 | ✅ AC-01…03 PASS | Gate PASS | PASS |
| Journal | L2279–2280 | P1 + P3 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | co-located status `DRAFT` false vs enums | **yes** (soft) | same list section / openapi schema |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | stale asgi/handlers line refs | **yes** (soft) | binding hygiene |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 3.  
**Actionable TASKED-likely:** 2 soft (G1, G3).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.

### Note (not a gap ID)

[`TECH-ARCH-issues-server-text-search.md` §5](../architecture/TECH-ARCH-issues-server-text-search.md) coexistence still «list/handler without text» — story OOS (API_REFERENCE + openapi only). Not opened as AC fail.
