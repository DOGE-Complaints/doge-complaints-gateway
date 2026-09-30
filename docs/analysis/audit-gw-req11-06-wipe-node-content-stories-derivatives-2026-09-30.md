# Hard Audit — STORY-GW-REQ11-06 wipe node content stories + derivatives + threads (2026-09-30)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-06-wipe-node-content-stories-derivatives`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) (T01–T06, **pkg-000105**).  
**Pipeline:** [`…/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md).  
**Pkg:** [`pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml`](../tasks/gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-06.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/task-gw-req11-06-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-06.md) PASS **2026-09-30T07:56:35Z**.  
**Run-summary:** [`run-summary-20260930-0756-gw-req11-06-p3.md`](../tasks/run-reports/run-summary-20260930-0756-gw-req11-06-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-09-30T07:59:07Z`. Branch: **`dev`**. Live: pytest → **8 passed**; no-confirm → **REFUSED**; `--dry-run` → ordered plan (gateway readiness + threads); script/Make Present; invent wipe HTTP on gateway ASGI → **not found**; Identity/`auth.users` DELETE paths → **absent** in wipe sources.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L771 / L881–890. AC из backlog Target verbatim — **не** invent.

---

## 1. Итог: AC PASS; Product Done = yes; live DELETE 204 (gate); 3 gaps (docs SSOT); TASKED-likely = G1+G2

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Script + confirm gate | [`life_sim_wipe_node_content.py`](../../tests/sandbox/life_sim_wipe_node_content.py) + [`life_sim_wipe_lib.py`](../../tests/sandbox/life_sim_wipe_lib.py); `make life-sim-wipe-node-content`; refuse without confirm | ✅ PASS |
| **T02** | FK-safe gateway deletes | `GATEWAY_DELETE_ORDER` = `REQUIRED_READINESS_TABLES` only; PostgREST DELETE; unit assert vs product frozenset | ✅ PASS |
| **T03** | Threads tables wipe | marks → comments → threads; optional `THREADS_SUPABASE_*` | ✅ PASS |
| **T04** | Dry-run + operator docs | `--dry-run`; manual §5 Present links | ✅ PASS *(§8 inventory residual → G2)* |
| **T05** | Offline unit tests | [`test_gw_req11_06_wipe_node_content.py`](../../tests/test_gw_req11_06_wipe_node_content.py) **8 passed** | ✅ PASS |
| **T06** | Gate AC-01…04 | Gate PASS 07:56:35Z; live 204 gateway+threads | ✅ PASS |

**Verdict product:** GW-REQ11-06 **исполнена** (wipe tooling + confirm + ordered deletes + docs §5 + units + live smoke 204 per gate/run-summary).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no** (docs SSOT residuals).  
**Confirm (operator ask):** invent wipe HTTP → **not present**; Identity wipe → **not present**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Script+Make; refuse without confirm | **PASS** | Present; `main([])` exit 2 REFUSED; Make target |
| AC-02 Gateway stack + threads; no Identity | **PASS** | Plan = readiness + 3 threads tables; FORBIDDEN substrings; source has no `auth.users` DELETE; gate live 204 |
| AC-03 Manual wipe links + dry-run | **PASS*** | §5 Present + dry-run cmds; *§8 inventory still «ожидаем Done» → **G2** |
| AC-04 Offline/unit + ordered deletes | **PASS** | 8 tests; dry-run lists full plan |

### Does Product Done hold?

**Yes.** Gate PASS without LIVE blocker class of REQ11-05; run-summary live wipe **OK (204)**. Residuals are documentation SSOT only.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Wipe script + lib | `life_sim_wipe_node_content.py`, `life_sim_wipe_lib.py` | ✅ |
| Make | `Makefile` `life-sim-wipe-node-content` | ✅ |
| Confirm gate | `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1` | ✅ |
| Gateway order = readiness | unit + frozenset sync | ✅ |
| Threads order | marks→comments→threads | ✅ |
| No Identity DELETE | tests + source grep | ✅ |
| No wipe HTTP invent | ASGI no wipe route; script = PostgREST client only | ✅ |
| Manual §5 Present | `life-sim-demo-node-load-manual-ru.md:142+` | ✅ |
| Branch | `dev` | ✅ |
| pytest | **8 passed** | ✅ |

---

## 3. Регрессии / gaps

### G1 — Backlog + T01 Code Facts still present-tense «Absent» · severity: **LOW** · **TASKED-likely**

Backlog §Verified / Code touchpoints still claim wipe script **Absent** while Status=Done and artifacts Present ([`STORY-GW-REQ11-06…md:48–72`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)). T01 Code Facts `:20–21` still «Target Absent» / «Make Absent»; Gap mixes «As-of-Done closed» with residual «Script/Make not Present». Pipeline As-of-Done table is correct.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog Verified + Code touchpoints + T01 (mirror REQ11-05 T08 pattern).

### G2 — Manual §8 inventory still «ожидаем Done оператора» · severity: **LOW** · **TASKED-likely**

[`life-sim-demo-node-load-manual-ru.md:209`](../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) Wipe row still future-tense while §5 documents **Present** script/Make (AC-03 core path OK).

**Как закрыть:** TASKED docs — align §8 inventory to Present/Done (one-line).

### G3 — Bullrun §«Актуальная точка» без REQ11-06 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L771 + tasks L885–890 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L771 GW-REQ11-06 | 🔵 Done · gate PASS · wipe Present · pkg-000105 | Product Done | PASS + **G1** (backlog SSOT) |
| T01 | L885 | ✅ script+Make confirm | Done | PASS (+ Code Facts Absent → G1) |
| T02 | L886 | ✅ readiness deletes; no Identity | Done | PASS |
| T03 | L887 | ✅ threads order | Done | PASS |
| T04 | L888 | ✅ dry-run + manual | Done | PASS (+ **G2** §8) |
| T05 | L889 | ✅ offline tests | Done | PASS 8 |
| T06 | L890 | ✅ AC-01…04 PASS | Gate PASS | PASS |
| Journal | L2087 | P3 execute 0756 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | backlog/T01 «Absent» vs Done | **yes** | As-of-Done / Historical |
| G2 | Low | manual §8 inventory stale | **yes** | Present vs «ожидаем Done» |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 3.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
