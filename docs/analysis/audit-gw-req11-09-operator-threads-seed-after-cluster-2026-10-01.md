# Hard Audit — STORY-GW-REQ11-09 operator threads seed after cluster (2026-10-01)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-09-operator-threads-seed-after-cluster`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) (T01–T06, **pkg-000107**) · backlog [`…/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md).  
**Pkg:** [`pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml`](../tasks/gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-09.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/task-gw-req11-09-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-09.md) PASS **2026-10-01T10:52:44Z**.  
**Run-summary:** [`run-summary-20261001-1052-gw-req11-09-p3.md`](../tasks/run-reports/run-summary-20261001-1052-gw-req11-09-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-01T10:56:18Z`. Branch: **`dev`**. Live: pytest → **9 passed**; `GATEWAY_URL=http://127.0.0.1:8000` dry-run → **exit 2** fail-closed (empty `/node/issues`); Make target Present; RU manual Present; B-THR-CLI Closed in load manual.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L773 / L931–942. AC из Target verbatim — **не** invent.

---

## 1. Итог: tooling AC PASS; live full seed leftover (empty issues); Product Done = yes (with residual); 3 gaps; TASKED-likely = G2 (+ G1 ops/WAIVE)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Fail-closed empty issues | [`life_sim_seed_threads_lib.require_nonempty_handoffs`](../../tests/sandbox/life_sim_seed_threads_lib.py); CLI exit **2** live + unit | ✅ PASS |
| **T02** | CLI + Make thin wrapper | [`life_sim_seed_threads.py`](../../tests/sandbox/life_sim_seed_threads.py) + `make life-sim-seed-threads`; `--limit` / `--dry-run` | ✅ PASS |
| **T03** | Secrets actors + handoff + seed | Bearer by `fixture_user_id`; `refuse_service_token_as_actor`; `seed_representative_issues` file-import | ✅ PASS *(full seed not run)* |
| **T04** | Offline unit tests | [`test_gw_req11_09_seed_threads.py`](../../tests/test_gw_req11_09_seed_threads.py) **9 passed** | ✅ PASS |
| **T05** | RU manual + B-THR-CLI | [`life-sim-threads-seed-manual-ru.md`](../runtime-docs/manuals/life-sim-threads-seed-manual-ru.md); load-manual B-THR-CLI **Closed** | ✅ PASS |
| **T06** | Gate AC-01…06 | Gate PASS 10:52:44Z | ✅ PASS |

**Verdict product:** GW-REQ11-09 **исполнена по gate framing** (fail-closed + thin wrapper + secrets actors + RU manual + units). Live **full** seed after non-empty cluster issues **not** executed this P3 (documented leftover — local `/node/issues` empty).  
**Product Story Done (AC/DoD) = yes** — holds **with** documented leftover (see §2). **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay — Product Done vs live full-seed leftover

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Fail-closed without non-empty issues; documented order | **PASS** | exit 2 live empty issues; manual § порядок load; unit `test_empty_issues_fail_closed` |
| AC-02 Thin wrapper → Present `seed_representative_issues` | **PASS** | CLI calls `import_closed_http_seed().seed_representative_issues`; unit asserts import |
| AC-03 Actors = secrets Bearer by `fixture_user_id`; not service token | **PASS** | `refuse_service_token_as_actor` + units; no SERVICE_API_TOKEN as actor |
| AC-04 Handoff `issue_id`+`density`; Make/CLI Present | **PASS** | `handoffs_from_issue_rows`; Make `life-sim-seed-threads`; density None → lib FLOOR OK |
| AC-05 RU manual; terminal smoke/full; load-manual link; B-THR-CLI closed | **PASS** | RU manual Present; load-manual L185/L203/L220 Closed |
| AC-06 No pack JSON mutate; K1; offline tests | **PASS** | `never_write_pack_json` + docstring; 9 tests; Bearer actors |

### Does Product Done hold with live leftover?

**Yes — under gate/story DoD as shipped:** Gate PASS with offline + live fail-closed evidence; run-summary / gate Leftover explicitly lists full seed until operator cluster. Tooling path green.

**Caveat:** residual live Pass (full seed after non-empty issues) still ops → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| CLI | `tests/sandbox/life_sim_seed_threads.py` | ✅ |
| Lib | `tests/sandbox/life_sim_seed_threads_lib.py` | ✅ |
| Make | `life-sim-seed-threads` | ✅ |
| RU manual | `life-sim-threads-seed-manual-ru.md` | ✅ |
| B-THR-CLI | load-manual **Closed** | ✅ |
| closed_http_seed reuse | `doge-threads/.../closed_http_seed.py` file-import | ✅ |
| Fail-closed exit | **2** when empty issues | ✅ |
| Offline tests | **9 passed** | ✅ |
| Branch | `dev` | ✅ |
| Live full seed | **not** run (issues empty) | ✅ leftover |

---

## 3. Регрессии / gaps

### G1 — Live full seed not run (empty `/node/issues`) · severity: **MEDIUM** · **TASKED-likely** (ops) / WAIVE-able

Run-summary / gate Leftover: local `GET /node/issues` → `issues=[]` → fail-closed (correct). Full seed after wipe→provision→replay→cluster **not** executed this P3. No invent force-cluster.

**Как закрыть (P5 hint):** TASKED ops — load order until non-empty issues → `make life-sim-seed-threads` (optional `LIMIT=2`); append comments/reactions counts. Or WAIVE operator if tooling+documented leftover accepted as Done for this wave.

### G2 — Backlog §Verified still present-tense «Absent» vs Done · severity: **LOW** · **TASKED-likely**

Backlog [`STORY-GW-REQ11-09…md:58–73`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md) §Verified (as-of 10:18) still claims Operator CLI / Make **Absent** and B-THR-CLI open while Meta Status=Done and artifacts Present. Pipeline already splits As-of-Done vs Historical. Task READMEs T01–T05 use As-of-Done + Historical correctly.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog §Verified / Code touchpoints (mirror REQ11-08 T08).

### G3 — Bullrun §«Актуальная точка» без REQ11-09 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L773 + tasks L935–940 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L773 GW-REQ11-09 | 🔵 Done · gate PASS · CLI+Make · B-THR-CLI Closed · offline 9 · leftover full seed · pkg-000107 | Product Done (leftover) | PASS + **G1** |
| T01 | L935 | ✅ exit 2 empty issues | Done | PASS |
| T02 | L936 | ✅ CLI+Make; `--limit` | Done | PASS |
| T03 | L937 | ✅ Bearer + `seed_representative_issues` | Done | PASS (full seed leftover → G1) |
| T04 | L938 | ✅ 9 passed | Done | PASS 9 |
| T05 | L939 | ✅ RU + B-THR-CLI Closed | Done | PASS |
| T06 | L940 | ✅ AC-01…06 PASS | Gate PASS | PASS |
| Journal | L2140 | P3 execute 1052 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | live full seed not run (empty issues) | **yes** (ops) or WAIVE operator | fail-closed exit 2 OK |
| G2 | Low | backlog §Verified «Absent» vs Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
