# Hard Audit — STORY-GW-REQ11-08 operator provision pack wave (2026-10-01)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-08-operator-provision-pack-wave`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/STORY-GW-REQ11-08-operator-provision-pack-wave.md) (T01–T07, **pkg-000106**) · backlog [`…/STORY-GW-REQ11-08-operator-provision-pack-wave.md`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md).  
**Pkg:** [`pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml`](../tasks/gateway-active-packages/pkg-000106-20261001-gw-req11-08-operator-provision-pack-wave.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-08.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-08-operator-provision-pack-wave/task-gw-req11-08-t07-story-gate/story-acceptance-gate-STORY-GW-REQ11-08.md) PASS **2026-10-01T10:31:41Z**.  
**Run-summary:** [`run-summary-20261001-1031-gw-req11-08-p3.md`](../tasks/run-reports/run-summary-20261001-1031-gw-req11-08-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-01T10:34:20Z`. Branch: **`dev`**. Live: pytest → **6 passed**; dry-run `--limit 2` → exit 0, `users.json` mtime unchanged, wave `state.json` Present; wipe without confirm → **exit 2 REFUSAL**; Make target Present.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T07 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L772 / L905–917. AC из Target verbatim — **не** invent.

---

## 1. Итог: tooling AC PASS; live Auth wipe/full provision not run (documented leftover); Product Done = yes (with residual); 3 gaps; TASKED-likely = G2 (+ G1 ops/WAIVE)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | CLI + pack users entry | [`life_sim_provision_pack_wave.py`](../../tests/sandbox/life_sim_provision_pack_wave.py) + `make life-sim-provision-pack-wave`; mtime guard / never write fixture | ✅ PASS |
| **T02** | Shared config fail-closed | [`life_sim_provision_config.py`](../../tests/sandbox/life_sim_provision_config.py): `SMS_PROVIDER=file`, `@dogestonia.me`, Identity Auth force | ✅ PASS |
| **T03** | Wave-state checkpoint + resume | [`life_sim_wave_store.py`](../../tests/sandbox/life_sim_wave_store.py) → `pack/waves/<id>/state.json`; resume skips `verified` | ✅ PASS |
| **T04** | skip \| wipe-fixture-users + provision | `--mode skip` default; wipe refuse exit 2; reuse REQ11-05 `provision_one` | ✅ PASS *(live wipe/provision not run)* |
| **T05** | RU manual | [`life-sim-provision-pack-wave-manual-ru.md`](../runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md) + load-manual cross-link | ✅ PASS |
| **T06** | Offline unit tests | [`test_gw_req11_08_provision_pack_wave.py`](../../tests/test_gw_req11_08_provision_pack_wave.py) **6 passed** | ✅ PASS |
| **T07** | Gate AC-01…06 | Gate PASS 10:31:41Z | ✅ PASS |

**Verdict product:** GW-REQ11-08 **исполнена по gate framing** (CLI + fail-closed config + wave-state + wipe/skip gate + RU manual + units). Live Identity Auth wipe and full/smoke provision HTTP **not** executed this P3 (run-summary Operator leftover).  
**Product Story Done (AC/DoD) = yes** — holds **with** documented leftover (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay — Product Done vs live Auth leftover

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 CLI reads pack `users.json`; never writes status there | **PASS** | dry-run wave written; fixture mtime unchanged; unit mtime guard |
| AC-02 Shared config: file SMS + `@dogestonia.me` + Identity Auth | **PASS** | config module + units fail-closed |
| AC-03 Wave-state per `fixture_user_id`; checkpoint; resume skips `verified` | **PASS** | wave store + unit resume; dry-run created `waves/p4-audit-smoke/state.json` |
| AC-04 `skip` default or `wipe-fixture-users` (+ confirm); fixture Auth only | **PASS*** | mode switch + refuse exit 2 verified; *live wipe HTTP **not** run (P3 leftover) |
| AC-05 RU manual; terminal smoke/full without chat | **PASS** | manual + Make cmds documented |
| AC-06 Clean layout on REQ11-05 reuse; secrets gitignored; offline tests | **PASS** | pack-wave entry + lib reuse; `.secrets/` + `packs/**/waves/` gitignored; 6 tests |

### Does Product Done hold with live leftover?

**Yes — under gate/story DoD as shipped:** Gate PASS (not PASS*) with offline/dry-run evidence; run-summary explicitly lists live full Auth provision and live wipe as **not** run. Tooling path green.

**Caveat:** residual live Pass (`LIMIT=2` / full pack with Identity `SMS_PROVIDER=file`) still ops → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Pack-wave CLI | `life_sim_provision_pack_wave.py` | ✅ |
| Config module | `life_sim_provision_config.py` | ✅ |
| Wave store | `life_sim_wave_store.py` | ✅ |
| Make | `life-sim-provision-pack-wave` | ✅ |
| RU manual | `life-sim-provision-pack-wave-manual-ru.md` | ✅ |
| Email domain | `@dogestonia.me` (config+lib) | ✅ |
| Wipe refuse | exit **2** without confirm | ✅ |
| Fixture immutable | users.json mtime unchanged this dry-run | ✅ |
| Waves gitignored | `.gitignore:19` `life_sim_packs/**/waves/` | ✅ |
| Branch | `dev` | ✅ |
| pytest | **6 passed** | ✅ |

---

## 3. Регрессии / gaps

### G1 — Live Auth wipe + live provision not run in P3 · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Run-summary Operator leftover: live full Auth provision (200) and live `wipe-fixture-users` **not** executed; only offline refuse + dry-run. Fail-closed tooling correct; no invent OTP HTTP.

**Как закрыть (P5 hint):** TASKED ops — Identity `SMS_PROVIDER=file` up → `LIFE_SIM_PACK_DIR=… make life-sim-provision-pack-wave LIMIT=2` (optional wipe+confirm smoke); append evidence `/me` verified. Or WAIVE operator if tooling+documented leftover accepted as Done for this wave.

### G2 — Backlog §Verified + task Code Facts still present-tense «Absent» · severity: **LOW** · **TASKED-likely**

Backlog §Verified (as-of 10:09) still claims pack-wave state / RU manual / shared config / mode switch **Absent** while Meta Status=Done and artifacts Present. Task READMEs T01–T04 Code Facts still lead with present-tense Absent (then As-of-Done closed + Historical). Pipeline already splits As-of-Done vs Historical.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog Verified + T01–T04 Code Facts (mirror REQ11-05/06 SSOT).

### G3 — Bullrun §«Актуальная точка» без REQ11-08 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L772 + tasks L909–915 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L772 GW-REQ11-08 | 🔵 Done · gate PASS · pack-wave Present · pkg-000106 | Product Done (leftover) | PASS + **G1** |
| T01 | L909 | ✅ pack users; never write fixture | Done | PASS |
| T02 | L910 | ✅ file SMS + `@dogestonia.me` + Identity | Done | PASS |
| T03 | L911 | ✅ wave JSON; skip verified | Done | PASS |
| T04 | L912 | ✅ skip / wipe-fixture + confirm | Done | PASS (refuse); live wipe leftover → G1 |
| T05 | L913 | ✅ RU manual + cross-link | Done | PASS |
| T06 | L914 | ✅ offline tests | Done | PASS 6 |
| T07 | L915 | ✅ AC-01…06 PASS | Gate PASS | PASS |
| Journal | L2113 | P3 execute 1031 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live Auth wipe/full provision not run | **yes** (ops) or WAIVE operator | dry-run + wipe refuse OK |
| G2 | Low | backlog/T0x Code Facts «Absent» vs Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
