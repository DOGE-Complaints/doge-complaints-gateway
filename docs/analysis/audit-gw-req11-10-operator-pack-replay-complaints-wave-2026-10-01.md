# Hard Audit — STORY-GW-REQ11-10 operator pack-wave replay жалоб (2026-10-01)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-10-operator-pack-replay-complaints-wave`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md) (T01–T06, **pkg-000108**) · backlog [`…/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md).  
**Pkg:** [`pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml`](../tasks/gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-10.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/task-gw-req11-10-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-10.md) PASS **2026-10-01T11:35:43Z**.  
**Run-summary:** [`run-summary-20261001-1135-gw-req11-10-p3.md`](../tasks/run-reports/run-summary-20261001-1135-gw-req11-10-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-01T11:38:41Z`. Branch: **`dev`**. Live: pytest → **8 passed**; `make life-sim-replay-pack-wave` без pack → **exit 2**; dry-run `--limit 2` → exit 0, `stories.json` mtime unchanged, `waves/…/replay_state.json` Present; RU manual Present; load-manual pack-wave primary.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L774 / L958–969. AC из Target verbatim — **не** invent.

---

## 1. Итог: tooling AC PASS; live full/LIMIT leftover Supabase Tunnel 403; Product Done = yes (with residual); 3 gaps; TASKED-likely = G2 (+ G1 ops/WAIVE)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Fail-closed pack dir + readonly stories | [`require_life_sim_pack_dir`](../../tests/sandbox/life_sim_replay_lib.py); Make exit **2**; mtime guard | ✅ PASS |
| **T02** | Wave-state checkpoint + resume | [`life_sim_replay_wave_store.py`](../../tests/sandbox/life_sim_replay_wave_store.py) → `replay_state.json`; skip `submitted` | ✅ PASS |
| **T03** | CLI + Make + reuse + Bearer | [`life_sim_replay_pack_wave.py`](../../tests/sandbox/life_sim_replay_pack_wave.py); `_preflight_missing_creds`; reuse lib/runner | ✅ PASS *(live submit leftover)* |
| **T04** | Offline unit tests | [`test_gw_req11_10_replay_pack_wave.py`](../../tests/test_gw_req11_10_replay_pack_wave.py) **8 passed** | ✅ PASS |
| **T05** | RU manual + load-manual primary | [`life-sim-replay-pack-wave-manual-ru.md`](../runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md); load-manual L183/L218 | ✅ PASS |
| **T06** | Gate AC-01…06 | Gate PASS 11:35:43Z | ✅ PASS |

**Verdict product:** GW-REQ11-10 **исполнена по gate framing** (fail-closed pack + wave-state + CLI/Make + RU + units). Live LIMIT=2 / full pack (~1661) submit **blocked** this P3 by Supabase Auth Tunnel **403** (documented leftover).  
**Product Story Done (AC/DoD) = yes** — holds **with** documented leftover (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay — Product Done vs Tunnel 403 leftover

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Fail-closed without `LIFE_SIM_PACK_DIR`; never write stories.json | **PASS** | Make exit 2; CLI SystemExit 2; dry-run mtime unchanged; unit mtime/path guards |
| AC-02 Wave-state per `fixture_story_id`; checkpoint; resume skips `submitted` | **PASS** | `ReplayWaveStore`; unit resume; dry-run created `waves/p4-audit-smoke/replay_state.json` |
| AC-03 Bearer by `fixture_user_id`; fail-closed missing creds | **PASS** | `_preflight_missing_creds` + unit |
| AC-04 Reuse REQ11-03 path; Make Present; smoke `--limit` / full | **PASS*** | CLI + Make Present; dry-run LIMIT=2 OK; *live HTTP submit leftover Tunnel 403 |
| AC-05 RU manual; load-manual pack-wave primary; terminal without chat | **PASS** | RU + load-manual § replay primary / legacy note |
| AC-06 K1; offline pack/wave/creds tests; no invent intake | **PASS** | 8 tests; sources assert no force-cluster invent |

### Does Product Done hold with Tunnel leftover?

**Yes — under gate/story DoD as shipped:** Gate PASS with offline + dry-run + fail-closed evidence; Leftover explicitly documents Supabase Tunnel 403 (auth unreachable). Tooling path green.

**Caveat:** residual live Pass (LIMIT=2 / full pack when Auth reachable) still ops → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| CLI | `life_sim_replay_pack_wave.py` | ✅ |
| Wave store | `life_sim_replay_wave_store.py` | ✅ |
| Pack gate | `require_life_sim_pack_dir` (+ `PACK_DIR`) | ✅ |
| Make | `life-sim-replay-pack-wave` | ✅ |
| RU manual | `life-sim-replay-pack-wave-manual-ru.md` | ✅ |
| Load-manual primary | L183 / L218 | ✅ |
| Fail-closed no pack | Make **exit 2** | ✅ |
| Fixture immutable | stories.json mtime unchanged (dry-run) | ✅ |
| Offline tests | **8 passed** | ✅ |
| Branch | `dev` | ✅ |
| Live full/LIMIT submit | **Tunnel 403 leftover** | ✅ documented |

---

## 3. Регрессии / gaps

### G1 — Live full / LIMIT submit leftover (Supabase Tunnel 403) · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Gate/run-summary Leftover: password-grant to `SUPABASE_URL` → Tunnel connection failed **403 Forbidden**. Dry-run + fail-closed OK; wave can mark `failed` on live attempts. No invent intake/force-cluster.

**Как закрыть (P5 hint):** TASKED ops — when Identity Auth reachable → `LIFE_SIM_PACK_DIR=… make life-sim-replay-pack-wave LIMIT=2` (then optional full); append success counts / wave `submitted`. Or WAIVE operator if tooling+documented leftover accepted as Done for this wave.

### G2 — Backlog (+ pipeline) §Verified still present-tense «Absent» vs Done · severity: **LOW** · **TASKED-likely**

Backlog and pipeline story §Verified (as-of 11:24) still claim wave-state / RU pack-wave manual **Absent** and Make simulate not fail-closed as the only narrative, while Meta Status=Done and artifacts Present. Task READMEs T01–T06 already use As-of-Done + Historical.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog (+ pipeline) §Verified / Code touchpoints (mirror REQ11-08/09).

### G3 — Bullrun §«Актуальная точка» без REQ11-10 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L774 + tasks L962–967 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L774 GW-REQ11-10 | 🔵 Done · gate PASS · CLI+Make · wave · offline 8 · dry-run LIMIT=2 · Tunnel 403 leftover · pkg-000108 | Product Done (leftover) | PASS + **G1** |
| T01 | L962 | ✅ fail-closed pack; never write stories | Done | PASS |
| T02 | L963 | ✅ wave per story; resume submitted | Done | PASS |
| T03 | L964 | ✅ reuse + Bearer + `--limit` | Done | PASS (live leftover → G1) |
| T04 | L965 | ✅ 8 passed | Done | PASS 8 |
| T05 | L966 | ✅ RU + load-manual primary | Done | PASS |
| T06 | L967 | ✅ AC-01…06 PASS | Gate PASS | PASS |
| Journal | L2167 | P3 execute 1135 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live full/LIMIT leftover Tunnel 403 | **yes** (ops) or WAIVE operator | dry-run + fail-closed OK |
| G2 | Low | backlog/pipeline §Verified «Absent» vs Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
