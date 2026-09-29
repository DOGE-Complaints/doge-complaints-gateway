# Hard Audit — STORY-GW-REQ11-03 profiled API replay + multi-submitter (2026-09-29)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-03-profiled-api-replay-multi-submitter`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md) (T01–T06, **pkg-000102**).  
**Pipeline:** [`…/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md).  
**Pkg:** [`pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml`](../tasks/gateway-active-packages/pkg-000102-20260929-gw-req11-03-profiled-api-replay-multi-submitter.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-03.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter/task-gw-req11-03-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-03.md) PASS **2026-09-29T14:21:44Z** (tooling + blocker).  
**Run-summary:** [`run-summary-20260929-1421-gw-req11-03-p3.md`](../tasks/run-reports/run-summary-20260929-1421-gw-req11-03-p3.md).  
**Operator note:** [`note-gw-req11-03-profiled-api-replay-2026-09-29.md`](./note-gw-req11-03-profiled-api-replay-2026-09-29.md).  
**Прогон этого аудита:** `utc_now: 2026-09-29T14:24:30Z`. Branch: **`dev`**. Live: pytest → **8 passed**; dry-run `--life-sim --max 5` → **5/5**; non-dry-run fail-closed **0/20** pool env; map entries **200** / slots **20** ×10.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L768 / L814–819. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: tooling AC PASS; live fill PASS-via-blocker; Product Done = yes (with residual); 3 gaps; TASKED-likely = G1+G2

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Wire fixtures + profile | `--life-sim` loads REQ11-01 scale + `DEMO_LIFE_SIM_PROFILE`; `assert_fixture_scale` 200/1661 | ✅ PASS |
| **T02** | Pool M=20 bootstrap | [`life_sim_pool_m20.json`](../../tests/sandbox/life_sim_pool_m20.json) 20 slots; env refs only; `test_ac03_pool_*` | ✅ PASS |
| **T03** | Map 200→20 + multi-Bearer | [`life_sim_fixture_to_pool_map_v0_1.json`](../../tests/sandbox/life_sim_fixture_to_pool_map_v0_1.json) 200 entries; [`resolve_pool_slot_bearer_token`](../../tests/simulation_intake_http.py:105) | ✅ PASS |
| **T04** | Wipe→profiled replay runner | [`simulation_runner.py`](../../tests/simulation_runner.py) `main_life_sim` / `--wipe-confirmed`; [`Makefile`](../../Makefile) `simulate-life-sim`; dry-run 5/5 | ✅ PASS *(live HTTP fill blocked)* |
| **T05** | Operator docs no SPA | [`note-gw-req11-03…`](./note-gw-req11-03-profiled-api-replay-2026-09-29.md); Pass=API+JSON | ✅ PASS |
| **T06** | Gate AC-01…04 | Gate PASS 14:21:44Z | ✅ PASS |

**Verdict product:** GW-REQ11-03 **исполнена по gate framing** (tooling + contracts + dry-run). Live multi-submitter fill **not** proven — **operator blocker** `LIFE_SIM_POOL_*` **0/20**.  
**Product Story Done (AC/DoD) = yes** — holds **with** documented blocker + tooling (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay — Product Done vs live pool blocker

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 wipe→profiled replay → pipeline | **PASS-via-blocker** | Tooling: `--wipe-confirmed` + stash→submit path [`post_stash_and_submit_http`](../../tests/simulation_intake_http.py:231); dry-run 5/5. Live non-dry-run: fail-closed `Pool M=20 incomplete: 0/20` — **no** proven HTTP fill this turn. |
| AC-02 fixture scale REQ11-01 | **PASS** | 200 users / 1661 stories; `test_ac02_*` |
| AC-03 pool M=20 map from 200 | **PASS*** | Manifest + map on disk; `% 20` rule; 10/slot; Bearer helper. *Live slots filled: **0/20** (blocker). |
| AC-04 no SPA; API+JSON | **PASS** | note; make target; runner banner «no SPA resident login»; `test_ac04_*` |

### Does Product Done hold with documented blocker?

**Yes — under gate/story DoD as shipped:** AC-01/03 closed via tooling + documented env blocker (gate PASS* + run-summary Operator blocker). Unit/contract **8 passed**; dry-run proves orchestration without HTTP.

**Caveat:** residual live Pass (wipe→real multi-Bearer fill of 1661) still requires admin-bootstrap of 20 pool creds → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Pool size 20 | `life_sim_pool_m20.json` | ✅ |
| Map 200→20 | map `entries` len=200; 10/slot | ✅ |
| `--life-sim` + fail-closed | `simulation_runner.py:200+` / `:217–220` | ✅ |
| `make simulate-life-sim` | `Makefile:38–44` | ✅ |
| Env pool filled | live count **0** | ✅ matches gate |
| Branch | `dev` | ✅ |

---

## 3. Регрессии / gaps

### G1 — Live pool creds 0/20; live HTTP fill unproven · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Fail-closed correct without inventing secrets. Until `LIFE_SIM_POOL_00..19_*` filled, AC-01 literal «stories enter gateway pipeline» remains tooling-only.

**Как закрыть (P5 hint):** TASKED ops — bootstrap 20 verified users + env; re-run non-dry `--life-sim` sample; append evidence. Or WAIVE operator if tooling+blocker accepted as Done for this wave.

### G2 — T01–T04 Code Facts still present-tense «Absent» · severity: **LOW** · **TASKED-likely**

Gap sections say As-of-Done closed, but Code Facts still claim pool/map/replay **Absent** (e.g. T01 `:22`).

**Как закрыть:** TASKED docs — As-of-Done vs Historical on T01–T04 Code Facts (move Absent to Historical only).

### G3 — Bullrun §«Актуальная точка» без REQ11-03 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L768 + tasks L814–819 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L768 GW-REQ11-03 | 🔵 Done · pool M=20 tooling · live 0/20 blocker | Product Done (blocker) | PASS + **G1** |
| T01 | L814 | 🔵 life-sim JSON + profile | Done | PASS |
| T02 | L815 | 🔵 pool env refs | Done | PASS |
| T03 | L816 | 🔵 map + resolve_pool_slot | Done | PASS |
| T04 | L817 | 🔵 `--life-sim` stash→submit | Done | PASS (dry-run) |
| T05 | L818 | 🔵 note Pass=API+JSON | Done | PASS |
| T06 | L819 | 🔵 AC-01…04 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |
| Journal | L2015 | P3 execute | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live pool 0/20; HTTP fill unproven | **yes** (ops) or WAIVE operator | fail-closed correct |
| G2 | Low | T01–T04 Code Facts «Absent» vs Gap As-of-Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
