# Hard Audit — STORY-GW-REQ57-03 sweep / retry sense-brief (2026-10-15)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ57-03-sweep-retry-sense-brief`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/STORY-GW-REQ57-03-sweep-retry-sense-brief.md) (T01–T06, **pkg-000115**) · backlog [`…/STORY-GW-REQ57-03-…`](../tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md).  
**Pkg:** [`pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml`](../tasks/gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ57-03.md`](../tasks/epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/task-gw-req57-03-t06-story-gate/story-acceptance-gate-STORY-GW-REQ57-03.md) PASS **2026-10-15T12:03:07Z**.  
**Run-summary:** [`run-summary-20261015-1203-gw-req57-03-p3.md`](../tasks/run-reports/run-summary-20261015-1203-gw-req57-03-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-15T12:06:27Z`. Branch: **`dev`**. Live: `pytest -q tests/test_gw_req57_03_sweep_retry_sense_brief.py` → **5 passed** (0.02s). `--verify` → **ok 6** (pkg-000115).

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L1109 / L1116–1121. AC из Target verbatim — **не** invent.

---

## 1. Итог: product AC PASS; eligible query + cron + ASGI wire + ready skip; 5 tests; 4 gaps (bullrun + soft evidence); TASKED-likely soft = G1/G3/G4

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | eligible pending/failed | [`sense_brief_sweep.py`](../../src/core/application/sense_brief_sweep.py) `is_sweep_eligible` / `list_sweep_eligible_issues` | ✅ PASS |
| **T02** | cron-class job | [`sense_brief_sweep_cron.py`](../../src/core/scheduler/sense_brief_sweep_cron.py) `SenseBriefSweepCronJob` (ClusterCronJob pattern) | ✅ PASS |
| **T03** | ASGI lifespan wire | [`asgi_app.py:229–265`](../../src/core/api/asgi_app.py) start/stop when nudge enabled | ✅ PASS† |
| **T04** | ready no alpha overwrite | eligible excludes ready; re-check before nudge; sweep **never** `save_projection` title/summary | ✅ PASS |
| **T05** | stub suite | [`test_gw_req57_03_sweep_retry_sense_brief.py`](../../tests/test_gw_req57_03_sweep_retry_sense_brief.py) **5 passed** | ✅ PASS |
| **T06** | gate AC-01…03 | Gate PASS 12:03:07Z | ✅ PASS |

† Product wire Present. No ASGI lifespan integration test (see **G1**).

**Verdict product:** GW-REQ57-03 **исполнена по gate framing** (pending/failed re-nudge · ready excluded · ClusterCronJob precedent · HTTP double · no live aibridge).  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-GW-REQ5703-01 failed/missing can complete via sweep (AC-57-06) | **PASS**† | `test_req57_03_sweep_renudges_pending_and_failed` + `test_req57_03_cron_run_once_uses_sweep_service` — re-nudge accept; peer bind completes apply (01/02) |
| AC-GW-REQ5703-02 ready not silently replaced by alpha | **PASS** | `test_req57_03_ready_not_overwritten_by_sweep` + `assert_ready_payload_unchanged`; ready not in eligible; no projection rewrite in sweep |
| AC-GW-REQ5703-03 unit/integration with stubs | **PASS** | **5 passed** this audit · HTTP double only |

† AC-01 evidence = **re-nudge** path (gateway); full pending→ready needs peer bind (out of gateway suite) — residual **G3**.

### Focus re-checks

| Focus | Result |
|-------|--------|
| Eligible `pending` \| `failed` | ✅ `SWEEP_ELIGIBLE_STATUSES` |
| Ready excluded | ✅ `is_sweep_eligible` + live re-check |
| Re-nudge same `generation_version` | ✅ no bump in `run_once` (04 / explicit) |
| Reuse nudge client (02) | ✅ `SenseBriefNudgeService.nudge` |
| Cron precedent | ✅ Thread + interval + `run_once` like ClusterCronJob |
| ASGI lifespan | ✅ gated by `aibridge_sense_brief_nudge_enabled` |
| Interval | ✅ `cluster_cron_interval_s` (no invent env) |
| Sweep ≠ cluster_cron_enabled | ✅ independent gate (nudge flag only) |
| No LLM/image | ✅ outbound nudge only |
| Tests | ✅ 5 passed |
| Branch | ✅ `dev` |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Sweep service | `src/core/application/sense_brief_sweep.py` | ✅ |
| Cron job | `src/core/scheduler/sense_brief_sweep_cron.py` | ✅ |
| Export | `src/core/scheduler/__init__.py` | ✅ |
| ASGI wire | `asgi_app.py` lifespan L229–265 | ✅ |
| Nudge reuse | `sense_brief_nudge.py` | ✅ |
| Offline tests | `tests/test_gw_req57_03_sweep_retry_sense_brief.py` | ✅ 5 |
| No projection write in sweep | `run_once` only calls `nudge` | ✅ |

---

## 3. Регрессии / gaps

### G1 — No ASGI lifespan integration test for sweep cron · severity: **LOW** · **TASKED-likely** (soft)

Suite covers `SenseBriefSweepCronJob.run_once` + service `run_once`; does **not** exercise app lifespan start/stop when `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED=true`. Product wire Present ([`asgi_app.py:229–250`](../../src/core/api/asgi_app.py)). Gate already PASS.

**Как закрыть:** TASKED test — lifespan/deps fixture asserts cron started when nudge enabled (and skipped when disabled); **or** P5 WAIVE if unit cron + read wire sufficient.

### G2 — Bullrun §«Актуальная точка» без REQ57-03 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L1109 + tasks L1116–1121 Done; epic banner + P3 note: §Актуальная точка **не** переписана.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — AC-01 «complete» evidence = re-nudge only (no bind→ready stub) · severity: **LOW** · **TASKED-likely** (soft) / WAIVE-ok info

`test_req57_03_sweep_renudges_pending_and_failed` proves accept HTTP double; does not simulate aibridge bind success → `generation_status=ready`. Gateway sweep cannot alone mark ready (bind = 01). Gate framed re-nudge as AC-01 evidence.

**Как закрыть:** TASKED optional stub bind after sweep for pending→ready; **or** WAIVE info-nonblocking (peer bind owned by 01; AC-01 = recover via re-nudge).

### G4 — T03 AC-trace line refs stale vs sweep block · severity: **LOW** · **TASKED-likely** (docs soft)

T03 Meta AC trace / Purpose cite `asgi_app.py` ~194–220 (cluster cron band); sweep wire is **L229–265**. Code Facts correctly describe lifespan. Soft path-ref drift only.

**Как закрыть:** TASKED docs — update T03 (and backlog Nested T03 Arch/AC if needed) to L229–265 / nudge-enabled gate.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L1109 GW-REQ57-03 | 🔵 Done · gate PASS · suite **5** · pkg-000115 | Product Done | PASS |
| T01 | L1116 | Done · pending/failed eligible | Done | PASS |
| T02 | L1117 | Done · ClusterCronJob precedent · AC-01 | Done | PASS |
| T03 | L1118 | Done · ASGI lifespan | Done (+ G1/G4 residual) | PASS |
| T04 | L1119 | Done · brief-wins · AC-02 | Done | PASS |
| T05 | L1120 | Done · suite **5** | 5 passed this audit | PASS |
| T06 | L1121 | Done · AC-01…03 PASS | Gate PASS | PASS |
| P3 note | L1123 | gate PASS · no §Актуальная точка rewrite | matches | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G2** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | ASGI lifespan wire untested | **yes** (soft) | test add or WAIVE |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | AC-01 = re-nudge not bind→ready | **yes** (soft) / WAIVE info | optional stub or WAIVE |
| G4 | Low | T03 line-ref drift | **yes** (docs) | align ~229–265 |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 4.  
**TASKED-likely (docs):** G4.  
**TASKED-likely (soft test/evidence):** G1, G3.  
**WAIVED-likely:** G2.

**Product Story Done ≠ empty OPEN gap-list** — зафиксировано явно.

---

## 6. Non-goals honored (story Out of scope)

- Bind/nudge first implement → 01/02 — reused, not reinvented.  
- Manual regenerate / version bump → 04.  
- Multi-replica aibridge store — Absent.  
- Live aibridge/LLM — Absent; HTTP double only.  
- No push; immutable pkg-000115 unchanged this audit.
