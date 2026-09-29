# Hard Audit — STORY-GW-REQ11-01 life-sim fixtures users+stories scale (2026-09-29)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-01-fixtures-users-stories-scale`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md) (T01–T05, **pkg-000100**).  
**Pipeline:** [`…/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/STORY-GW-REQ11-01-fixtures-users-stories-scale.md).  
**Pkg:** [`pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml`](../tasks/gateway-active-packages/pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-01.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t05-story-gate/story-acceptance-gate-STORY-GW-REQ11-01.md) PASS **2026-09-29T13:43:36Z**.  
**Run-summary:** [`run-summary-20260929-1343-gw-req11-01-p3.md`](../tasks/run-reports/run-summary-20260929-1343-gw-req11-01-p3.md).  
**Canvas note:** [`note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md`](./note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md).  
**Прогон этого аудита:** `utc_now: 2026-09-29T13:46:28Z`. Branch: **`dev`**. Live: pytest `tests/test_gw_req11_01_life_sim_fixtures.py` → **4 passed**; fixture recompute users=200 / stories=1661 / mean=8.305 / langs et·ru·en 0.602·0.2926·0.1054 / mass pre·post 0.2498·0.7502; canvas v0_1=130 / v0_2=18.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T05 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L766 / L775–779. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: product AC-01…04 / T01–T05 закрыты; 2 OPEN gaps (0 Critical/High/Medium); TASKED-likely = G1

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Users+stories at locked scale | [`dogestonia_life_sim_users_v0_1.json`](../../tests/sandbox/dogestonia_life_sim_users_v0_1.json) **200**; [`…_stories_v0_1.json`](../../tests/sandbox/dogestonia_life_sim_stories_v0_1.json) **1661**; generator + meta on disk; mean **8.305**; clamp observed **[3,13]⊂[1,20]**; `test_ac01_*` | ✅ PASS |
| **T02** | Lang mix ≈60/30/10 | Live fractions et **0.602** / ru **0.2926** / en **0.1054**; meta + `test_ac02_*` | ✅ PASS |
| **T03** | 2026 exp curve / breakpoint / mass | Span 2026-01-01…2026-12-31; bp 2026-09-30; pre **0.2498** / post **0.7502**; density post>pre; `test_ac03_*` | ✅ PASS |
| **T04** | Canvas relation doc | [`note-gw-req11-01…`](./note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md) — life-sim supersedes canvas for multi-user scale; runner still canvas | ✅ PASS |
| **T05** | Gate AC-01…04 | Gate PASS 13:43:36Z | ✅ PASS |

**Verdict product:** GW-REQ11-01 **исполнена по AC** (on-disk fixtures + measurable locks + canvas note; no invent public APIs; runner not rewired — out of scope → REQ11-03).  
**Product Story Done (AC/DoD) = yes. Empty OPEN gap-list = no** (G1 TASKED-likely SSOT; G2 WAIVED-likely operator).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts (findings, not fix)

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 fixtures at locked scale | **PASS** | 200 users; 1661 stories ∈ [1500,1900]; per-user join 200; mean 8.305 ∈ [7,10]; clamp [3,13]⊂[1,20]; generator [`generate_dogestonia_life_sim_fixtures_v0_1.py`](../../tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py); meta seed `20260929` |
| AC-02 langs ≈60/30/10 | **PASS** | |et−0.60|≤0.03 etc. (live + pytest) |
| AC-03 2026 exp curve | **PASS** | breakpoint + mass ±0.02; post density > pre (pytest) |
| AC-04 canvas relation | **PASS** | note on disk; canvas lens 130/18 still true |
| Out: profiles/replay/backdate; invent APIs; wire runner | **PASS** | note «not wired»; story Out of scope |

### Reference code (unchanged consumer)

| Fact | Path | Match? |
|------|------|--------|
| `run_scenario_stash_submit` | `tests/simulation_runner.py:120` | ✅ |
| Canvas JSON load | `tests/simulation_runner.py:170` (story Historical cites `:155–185` span — still contains load) | ✅ load exists |
| Canvas sizes | v0_1=130, v0_2=18 | ✅ |
| Branch | `dev` | ✅ |

---

## 3. Регрессии / gaps

### G1 — Persistent SSOT present-tense vs live post-P3 · severity: **LOW** · **TASKED-likely**

Product shipped; backlog §Verified + T01–T04 Code Facts/Gap still assert pre-P3 absence.

| Artifact | Stale claim | Live fact |
|----------|-------------|-----------|
| Backlog §Verified [`:34–40`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md) | Multi-user / Gaussian / 2026 exp fixtures **Absent** | Files + meta + tests present |
| T01 Code Facts / Gap | «Absent»; Gap «No on-disk… yet» | Done; fixtures on disk |
| T02 Code Facts / Gap | «Absent until T01»; Gap «No measurable 60/30/10…» | Mix measured; DoD `[x]` |
| T03 Code Facts / Gap | «Absent until T01»; Gap «No 2026… curve» | Curve measured |
| T04 Gap | «No written relation… note» | Note exists |
| Pipeline §Verified | Already As-of-Done + Historical | Aligns with live |

**Как закрыть (P5 hint):** TASKED — As-of-Done vs Historical на backlog §Verified + T01–T04 Code Facts/Gap. Docs-only; **не** reopen product unless fixture drift.

### G2 — Bullrun §«Актуальная точка» без REQ11-01 · severity: **LOW** · **WAIVED-likely reason=operator**

Fence: не rewrite §«Актуальная точка». File still EPIC-M2-24 / ES-03 — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). REQ11-01 L766 + T01–T05 L775–779 already 🔵 Done + gate PASS.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L766 GW-REQ11-01 | 🔵 Done pkg-000100 T01–T05 · 200/1661 · langs≈60/30/10 · mass≈25/75 | Product Done | PASS |
| T01 | L775 | 🔵 200 users; 1661 stories; mean 8.305 | Done | PASS |
| T02 | L776 | 🔵 et/ru/en fractions | Done | PASS |
| T03 | L777 | 🔵 breakpoint + mass | Done | PASS |
| T04 | L778 | 🔵 life-sim supersedes canvas for scale | Done | PASS |
| T05 | L779 | 🔵 AC-01…04 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1975 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | backlog §Verified + T01–T04 Code Facts/Gap present-tense | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** 1 (G1).  
**WAVE:** n/a (P4).

Handoff: P5 disposition (G1 TASKED-likely; G2 WAIVED-likely). Не закрывать gaps здесь.
