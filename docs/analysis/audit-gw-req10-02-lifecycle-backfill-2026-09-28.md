# Hard Audit — STORY-GW-REQ10-02 lifecycle backfill + mapper cleanup (2026-09-28)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup`](../tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md) (T01–T06, **pkg-000099**).  
**Pipeline:** [`…/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`](../tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md).  
**Pkg:** [`pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml`](../tasks/gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ10-02.md`](../tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t06-story-gate/story-acceptance-gate-STORY-GW-REQ10-02.md) PASS **2026-09-28T17:44:10Z**.  
**Run-summary:** [`run-summary-20260928-1744-gw-req10-02-p3.md`](../tasks/run-reports/run-summary-20260928-1744-gw-req10-02-p3.md).  
**Evidence:** [`evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md`](./evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md).  
**Прогон этого аудита:** `utc_now: 2026-09-28T17:48:08Z`. Branch: **`dev`**. Live: pytest `test_gw_req10_02_lifecycle_parse.py` + repository lifecycle/contract → **24 passed**; `rg` under `src/` for `debug-ba94c7` / `.cursor/debug` / `#region agent log` / `"RECEIVED"` / `"received"` → **clean**. Hosted PostgREST **not** re-polled this turn — AC-01 status from evidence artifact.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T06 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L718 / L742–747. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: AC-02…04 code PASS; AC-01 PASS-via-blocker; Product Done = yes (with residual); 3 OPEN-class gaps (0 Critical/High); TASKED-likely = G1+G3

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Hosted RECEIVED→accepted (or blocker) | [`evidence…§T01`](./evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) — PostgREST OK; `stories` `*/0` ≠ inventory 162; inventory id absent; RECEIVED×0 on current endpoint; **operator blocker** | ✅ PASS *(blocker path)* |
| **T02** | Fixture cleanup if needed | Fixtures **N/A** — re-scan absent RECEIVED/received as data (inventory + evidence §T02) | ✅ PASS |
| **T03** | Slim mapper; no permanent RECEIVED map | [`db_supabase.py:179–185`](../../src/core/infrastructure/db_supabase.py) → `StoryLifecycleStatus(str(raw))` only | ✅ PASS |
| **T04** | Remove debug I/O | No `debug-ba94c7` / agent-log in function; live `rg src` clean | ✅ PASS |
| **T05** | Tests AC-02…04 | [`test_gw_req10_02_lifecycle_parse.py`](../../tests/test_gw_req10_02_lifecycle_parse.py); live **11** + repo suite **24 passed** | ✅ PASS |
| **T06** | Gate AC-01…04 | Gate PASS 17:44:10Z | ✅ PASS |

**Verdict product:** GW-REQ10-02 **исполнена по gate framing** (mapper+debug+tests solid; AC-01 closed via **documented operator blocker**, not proven PATCH of inventory `RECEIVED` row).  
**Product Story Done (AC/DoD) = yes** — holds **with** documented blocker (see §2). **Empty OPEN gap-list = no** (G1 residual hosted cleanup; G2 WAIVED-likely; G3 SSOT TASKED-likely).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts — Product Done vs AC-01 blocker

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Known legacy RECEIVED cleaned (fixtures if required) | **PASS-via-blocker** | Fixtures N/A. Hosted: evidence documents empty `stories` vs inventory 162 — cannot PATCH inventory `story_id=6019633d-…`. Literal «cleaned» **not** fact-proven against inventory project. Gate/story treat documented blocker as AC close for this wave. |
| AC-02 Mapper no permanent RECEIVED special-case | **PASS** | `db_supabase.py:179–185`; test asserts `"RECEIVED"`/`"received"` absent in source |
| AC-03 Unknown fail closed | **PASS** | Strict enum ctor; pytest parametrize `RECEIVED`/`received`/`pending`/… → `ValueError` |
| AC-04 No `.cursor/debug-*.log` from lifecycle path | **PASS** | Code + live `rg src` clean; test `test_src_has_no_cursor_debug_lifecycle_writes` |

### Does Product Done hold with documented blocker?

**Yes — under gate/story DoD as shipped:** AC-01 was closed by writing the operator blocker (reachable but empty/mismatched vs inventory), matching how T01/gate/backlog checkbox annotate `*(hosted operator blocker)*`. Code AC-02…04 are independently verified.

**Caveat (not invent AC):** residual H4 data risk remains when inventory-project credentials return a `RECEIVED` row — slim mapper will now **fail closed** on hydrate (no legacy map). That is intentional post-slim behavior; cleanup still owed against the inventory dataset → **G1**.

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Slim parse | `db_supabase.py:179–185` | ✅ |
| Hydrate call | `db_supabase.py:226` (was :265 pre-slim) | ✅ live |
| Enum ACCEPTED | `contracts.py:21` | ✅ |
| sqlite strict | `db_sqlite.py:225` | ✅ (unchanged) |
| Branch | `dev` | ✅ |

---

## 3. Регрессии / gaps

### G1 — Hosted inventory RECEIVED never proven cleaned · severity: **MEDIUM** · **TASKED-likely**

Evidence: current endpoint empty (`*/0`) vs REQ10-01 inventory 162 / `RECEIVED`×1. No PATCH evidence for inventory id. After mapper slim, any remaining `RECEIVED` in that project will **raise** on read.

**Как закрыть (P5 hint):** TASKED — ops re-point credentials to inventory project; PATCH/DISTINCT until RECEIVED=0; append evidence note. Or WAIVE if operator accepts empty current DB as sufficient and inventory project abandoned. Docs/ops — not mapper reopen.

### G2 — Bullrun §«Актуальная точка» без REQ10-02 · severity: **LOW** · **WAIVED-likely reason=operator**

File still EPIC-M2-24 / ES-03 lead — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). Story/tasks L718 / L742–747 already 🔵 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### G3 — Persistent SSOT present-tense in T01/T03/T04 READMEs · severity: **LOW** · **TASKED-likely**

| Artifact | Stale claim | Live fact |
|----------|-------------|-----------|
| T01 Gap [`README`](../tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t01-hosted-lifecycle-backfill/README.md) | «still has at least one RECEIVED row until P3 cleanup» | Done + blocker; current endpoint RECEIVED×0 / empty |
| T03 Code Facts / Gap | Legacy dict `:185–188` still present | Slim `:179–185`; Gap should be Closed As-of-Done |
| T04 Code Facts / Gap | Debug `:190–221` still present | Removed; `rg` clean |
| Pipeline Code touchpoints | hydrate `:265`; parse `:179-224` | hydrate `:226`; parse `:179–185` |

**Как закрыть:** TASKED docs-only As-of-Done vs Historical on T01/T03/T04 (+ optional pipeline line-number touchpoints).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L718 GW-REQ10-02 | 🔵 Done pkg-000099 T01–T06 · hosted AC-01 operator blocker | Product Done (blocker) | PASS + **G1** residual |
| T01 | L742 | 🔵 operator blocker — stories empty vs inventory | Done (blocker) | PASS + **G1** |
| T02 | L743 | 🔵 fixtures N/A | Done | PASS |
| T03 | L744 | 🔵 RECEIVED dict removed; fail-closed | Done | PASS (code) |
| T04 | L745 | 🔵 debug-ba94c7 removed; rg clean | Done | PASS |
| T05 | L746 | 🔵 11 passed (+24 w/ repo) | Done | PASS (re-run 24) |
| T06 | L747 | 🔵 AC-01…04 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1943 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | hosted inventory RECEIVED cleanup unproven | **yes** (ops/evidence) | or WAIVE if inventory project abandoned |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |
| G3 | Low | T01/T03/T04 (+pipeline lines) SSOT present-tense | **yes** | As-of-Done / Historical docs-only |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** 2 (G1, G3).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
