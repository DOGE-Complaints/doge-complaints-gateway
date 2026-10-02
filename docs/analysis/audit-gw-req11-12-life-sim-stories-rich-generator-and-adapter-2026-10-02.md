# Hard Audit — STORY-GW-REQ11-12 life-sim rich generator + adapter v2 (2026-10-02)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) (T01–T07, **pkg-000110**) · backlog [`…/STORY-GW-REQ11-12-…`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md).  
**Pkg:** [`pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml`](../tasks/gateway-active-packages/pkg-000110-20261002-gw-req11-12-life-sim-stories-rich-generator-and-adapter.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-12.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter/task-gw-req11-12-t07-story-gate/story-acceptance-gate-STORY-GW-REQ11-12.md) PASS **2026-10-02T09:10:26Z**.  
**Run-summary:** [`run-summary-20261002-0910-gw-req11-12-p3.md`](../tasks/run-reports/run-summary-20261002-0910-gw-req11-12-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-02T09:12:03Z`. Branch: **`dev`**. Live: pytest `test_gw_req11_12*` + `test_gw_req11_10*` → **15 passed**; pack `ls-20261002T0906Z-veerenni-v2-rich` Present · **1661/1661** unique bodies · 14 flat keys · users **200** · langs et/ru/en **1000/486/175**; `require_life_sim_pack_dir` fail-closed OK; load-manual Partial→Pass Present.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T07 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L776 / L1013–1023. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; diversity full uniqueness; fail-closed intact; 2 gaps (SSOT + bullrun); TASKED-likely = G1

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Generator v2 + scale locks | [`life_sim_stories_v2_lib.py`](../../tests/sandbox/life_sim_stories_v2_lib.py) + [`generate_life_sim_pack_stories_v2.py`](../../tests/sandbox/generate_life_sim_pack_stories_v2.py); 200 users / 1661 stories / lang lock | ✅ PASS |
| **T02** | Diversity composed templates | **1661/1661** unique `body`; no LLM markers as author | ✅ PASS |
| **T03** | params.json foci / defaults | pack `params.json` Present; unit consume vs defaults | ✅ PASS |
| **T04** | Adapter prefer v2 + thin 6-key | [`life_sim_story_to_intake_payload`](../../tests/sandbox/life_sim_replay_lib.py); fail-closed restored | ✅ PASS |
| **T05** | Offline tests + REQ11-10 smoke | [`test_gw_req11_12_…`](../../tests/test_gw_req11_12_stories_v2_generator_adapter.py) + req11-10 → **15 passed** | ✅ PASS |
| **T06** | Pack dir SSOT + Partial→Pass docs | pack under `life_sim_packs/`; load-manual L145–148 / L222 | ✅ PASS |
| **T07** | Gate AC-01…06 | Gate PASS 09:10:26Z | ✅ PASS |

**Verdict product:** GW-REQ11-12 **исполнена по gate framing** (v2 generator + diversity + adapter prefer + pack under packs + offline).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Generator emits v2; scale/lang/2026 locks | **PASS** | Pack row keys include join + `title_i18n`/`description_i18n`/`summary_i18n`/`session_language`/`location_query`/`canonical_*`/`institution_i18n`; users=200; langs 1000/486/175 |
| AC-02 Diversity ≥ N unique bodies; no LLM | **PASS** | unique_bodies **1661/1661**; lib docstring «No LLM»; no openai/anthropic imports in generator paths |
| AC-03 params.json foci/tags; empty → defaults | **PASS** | pack `params.json` Present; unit `test_params_foci_consumed_vs_defaults` |
| AC-04 Adapter prefers v2; 6-key thin remains | **PASS** | `_coerce_i18n_map` + prefer fields; thin path unit; fail-closed `require_life_sim_pack_dir` Present |
| AC-05 Offline schema/diversity/round-trip + REQ11-10 smoke | **PASS** | **15 passed** (12+10 suites) |
| AC-06 Pack under `life_sim_packs/<id>/`; Partial→Pass manual | **PASS** | `ls-20261002T0906Z-veerenni-v2-rich`; load-manual Partial (6-key) vs Pass (v2) |

### Focus re-checks

| Focus | Result |
|-------|--------|
| Unique bodies | ✅ 1661/1661 |
| Pack under `life_sim_packs` | ✅ |
| Adapter prefer v2 + 6-key thin | ✅ |
| Fail-closed pack dir intact | ✅ `require_life_sim_pack_dir` raises without env |
| Offline tests | ✅ 15 passed |
| No invent HTTP / gpt_signals / axis IDs | ✅ (gate/out-of-scope; adapter docstring) |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| v2 lib / CLI | `life_sim_stories_v2_lib.py`, `generate_life_sim_pack_stories_v2.py` | ✅ |
| Adapter | `life_sim_replay_lib.life_sim_story_to_intake_payload` | ✅ |
| Fail-closed | `require_life_sim_pack_dir` + `PACK_DIR` alias | ✅ |
| Ref pack | `life_sim_packs/ls-20261002T0906Z-veerenni-v2-rich/` | ✅ |
| Offline tests | `test_gw_req11_12_…` | ✅ |
| Load-manual Partial→Pass | `life-sim-demo-node-load-manual-ru.md` | ✅ |
| Branch | `dev` | ✅ |
| Legacy 6-key pack | still Present (Partial path) | ✅ orthogonal |

---

## 3. Регрессии / gaps

### G1 — Backlog (+ pipeline) §Verified still scaffold present-tense vs Done · severity: **LOW** · **TASKED-likely**

Backlog [`STORY-GW-REQ11-12…md:52–61`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md) and pipeline §Verified (as-of P1 scaffold) still claim generator = 6-key + ~15 BLURBS / unique bodies **15**/1661 while Meta Status=Done and disk shows v2 pack **1661/1661**. Task READMEs lack consistent As-of-Done/Historical split (T01 no As-of-Done markers).

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog (+ pipeline) §Verified / Code Facts (mirror REQ11-08…11).

### G2 — Bullrun §«Актуальная точка» без REQ11-12 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L776 + tasks L1017–1023 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L776 GW-REQ11-12 | 🔵 Done · gate PASS · diversity 1661/1661 · pack v2-rich · offline 15 · pkg-000110 | Product Done | PASS |
| T01 | L1017 | ✅ emit flat v2; scale locks | Done | PASS |
| T02 | L1018 | ✅ 1661/1661 unique bodies | Done | PASS |
| T03 | L1019 | ✅ params / civic defaults | Done | PASS |
| T04 | L1020 | ✅ prefer v2; 6-key thin | Done | PASS |
| T05 | L1021 | ✅ offline + REQ11-10 smoke | Done | PASS 15 |
| T06 | L1022 | ✅ pack SSOT + Partial→Pass | Done | PASS |
| T07 | L1023 | ✅ AC-01…06 PASS | Gate PASS | PASS |
| Journal | L2223 | P3 execute 0910 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | backlog/pipeline §Verified scaffold vs Done | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** 1 (G1).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
