# Hard Audit — STORY-GW-REQ11-02 named profiles local + Uus Veerenni (2026-09-29)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-02-named-profiles-local-uus-veerenni`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md) (T01–T04, **pkg-000101**).  
**Pipeline:** [`…/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni.md).  
**Pkg:** [`pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml`](../tasks/gateway-active-packages/pkg-000101-20260929-gw-req11-02-named-profiles-local-uus-veerenni.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-02.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-02-named-profiles-local-uus-veerenni/task-gw-req11-02-t04-story-gate/story-acceptance-gate-STORY-GW-REQ11-02.md) PASS **2026-09-29T14:00:57Z**.  
**Run-summary:** [`run-summary-20260929-1400-gw-req11-02-p3.md`](../tasks/run-reports/run-summary-20260929-1400-gw-req11-02-p3.md).  
**Selection note:** [`note-gw-req11-02-profile-selection-2026-09-29.md`](./note-gw-req11-02-profile-selection-2026-09-29.md).  
**Прогон этого аудита:** `utc_now: 2026-09-29T14:04:04Z`. Branch: **`dev`**. Live: pytest `tests/test_gw_req11_02_named_profiles.py` → **4 passed**; `select_profile` ids=`local`,`uus-veerenni`; ports 8100/8000/8001/8080/5173; default=`local`; `assert_no_secret_literals` OK.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T04 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L767 / L795–798. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: product AC-01…03 / T01–T04 закрыты; 2 OPEN gaps (0 Critical/High/Medium); TASKED-likely = G1

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Profile `local` + local-five ports | [`local.json`](../../tests/sandbox/profiles/local.json); ports match [`local-five-serve-and-health.sh:17–23`](../../../scripts/shell/local-five-serve-and-health.sh); `test_ac01_*` | ✅ PASS |
| **T02** | Profile `uus-veerenni` env refs | [`uus-veerenni.json`](../../tests/sandbox/profiles/uus-veerenni.json); `GATEWAY_URL`/`GATEWAY_API_TOKEN`; example host = `.env.test.example:13`; `test_ac02_*` | ✅ PASS |
| **T03** | Env refs only + selection doc | `*_env` names; note on disk; `DEMO_LIFE_SIM_PROFILE`; `test_ac03_*` + selection test | ✅ PASS |
| **T04** | Gate AC-01…03 | Gate PASS 14:00:57Z | ✅ PASS |

**Verdict product:** GW-REQ11-02 **исполнена по AC** (selectable profiles + env refs + selection note; runner not rewired — out of scope → REQ11-03).  
**Product Story Done (AC/DoD) = yes. Empty OPEN gap-list = no** (G1 TASKED-likely SSOT; G2 WAIVED-likely operator).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts (findings, not fix)

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 `local` selectable + local-five URL/env refs | **PASS** | [`index.json`](../../tests/sandbox/profiles/index.json) + [`local.json`](../../tests/sandbox/profiles/local.json); loader [`demo_life_sim_profiles.py`](../../tests/sandbox/profiles/demo_life_sim_profiles.py) `select_profile("local")`; ports 8100/8000/8001/8080/5173 |
| AC-02 Uus Veerenni selectable + documented URL/env refs | **PASS** | [`uus-veerenni.json`](../../tests/sandbox/profiles/uus-veerenni.json); `documented_example_url` = `.env.test.example` host; no `api_token` literal field |
| AC-03 secrets in env; profiles env names only | **PASS** | `assert_no_secret_literals`; collect `*_env`; note secrets policy; `rg` no JWT/`sk-` literals in profile JSON values |
| Out: fixtures; replay; invent APIs | **PASS** | note §Out of scope; runner still direct `GATEWAY_URL` [`simulation_runner.py:152–153`](../../tests/simulation_runner.py) |

### Reference facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| local-five SERVICES ports | `scripts/shell/local-five-serve-and-health.sh:17–23` | ✅ |
| Runner env contract | `tests/simulation_runner.py:152–153` (+ user Bearer) | ✅ |
| Make simulate | `Makefile:31–32` | ✅ |
| Branch | `dev` | ✅ |

---

## 3. Регрессии / gaps

### G1 — Persistent SSOT present-tense in T01–T03 Code Facts/Gap · severity: **LOW** · **TASKED-likely**

Product shipped; T01–T03 still assert pre-P3 absence in Code Facts/Gap while As-of-Done sections list artifacts.

| Artifact | Stale claim | Live fact |
|----------|-------------|-----------|
| T01 Code Facts / Gap | selector **Absent**; Gap «No selectable `local`…» | `local.json` + registry + loader; DoD `[x]` |
| T02 Code Facts / Gap | selector **Absent**; Gap open present-tense | `uus-veerenni.json` present |
| T03 Gap | «No written selection procedure…» | note on disk |
| Backlog / pipeline §Verified | Already **Present** | Aligns with live |

**Как закрыть (P5 hint):** TASKED — As-of-Done vs Historical на T01–T03 Code Facts/Gap (move «Absent» / open Gap to Historical). Docs-only; **не** reopen product.

### G2 — Bullrun §«Актуальная точка» без REQ11-02 · severity: **LOW** · **WAIVED-likely reason=operator**

File still EPIC-M2-24 / ES-03 — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). Story L767 + T01–T04 L795–798 already 🔵 Done + gate PASS.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L767 GW-REQ11-02 | 🔵 Done pkg-000101 T01–T04 · local+uus-veerenni env refs | Product Done | PASS |
| T01 | L795 | 🔵 `local.json` ports | Done | PASS |
| T02 | L796 | 🔵 `uus-veerenni.json` env refs | Done | PASS |
| T03 | L797 | 🔵 `DEMO_LIFE_SIM_PROFILE` + note | Done | PASS |
| T04 | L798 | 🔵 AC-01…03 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1994 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | T01–T03 Code Facts/Gap present-tense vs As-of-Done | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** 1 (G1).  
**WAVE:** n/a (P4).

Handoff: P5 disposition (G1 TASKED-likely; G2 WAIVED-likely). Не закрывать gaps здесь.
