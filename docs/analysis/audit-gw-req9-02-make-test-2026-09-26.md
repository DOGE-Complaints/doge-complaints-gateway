# Hard Audit — STORY-GW-REQ9-02 Makefile `test` + `test-live` (2026-09-26)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ9-02-make-test`](../tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md) (T01–T03, **pkg-000097**).  
**Pipeline:** [`…/STORY-GW-REQ9-02-make-test.md`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md).  
**Pkg:** [`pkg-000097-20260926-gw-req9-02-make-test.yaml`](../tasks/gateway-active-packages/pkg-000097-20260926-gw-req9-02-make-test.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ9-02.md`](../tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/task-gw-req9-02-t03-story-gate/story-acceptance-gate-STORY-GW-REQ9-02.md) PASS **2026-09-26T12:22:28Z**.  
**Run-summary:** [`run-summary-20260926-1222-gw-req9-02-p3.md`](../tasks/run-reports/run-summary-20260926-1222-gw-req9-02-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-09-26T12:27:40Z`. Live: `make -n test` / `make -n test-live` → expected marker lines; offline pytest `-m "not live_integration"` → **886 passed, 4 failed, 18 skipped, 10 deselected**; `pytest -m live_integration --collect-only` → **10/918**.

> **Природа аудита.** P4 hard audit product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T03 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L670 / L696–698. AC из pipeline Target verbatim — **не** invent.

---

## 1. Итог: product AC-01…03 / T01–T03 закрыты; 2 OPEN gaps (0 Critical/High/Medium); TASKED-likely = G1

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | `make test` + PHONY `test`; `-m "not live_integration"` | [`Makefile:1`](../../Makefile), [`:50–51`](../../Makefile); dry-run + live 10 deselected | ✅ PASS |
| **T02** | `make test-live` + PHONY `test-live`; `-m live_integration` | [`Makefile:1`](../../Makefile), [`:53–54`](../../Makefile); collect-only **10/918** | ✅ PASS |
| **T03** | Gate AC-01…03 | Gate PASS 12:22:28Z | ✅ PASS |

**Verdict product:** GW-REQ9-02 **исполнена по AC** (ritual + marker wiring; lock C).  
**Product Story Done (AC/DoD) = yes. Empty OPEN gap-list = no** (G1 TASKED-likely; G2 WAIVED-likely).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts (findings, not fix)

| AC (pipeline Target) | Result | Evidence |
|----------------------|--------|----------|
| AC-01 `make test` + `-m "not live_integration"` | **PASS** | `Makefile:50–51`; dry-run; live 10 `live_integration` deselected |
| AC-02 `.PHONY` includes `test` | **PASS** | `Makefile:1` |
| AC-03 `make test-live` for live_integration | **PASS** | `Makefile:53–54`; PHONY `test-live`; collect-only 10/918 |
| Out: env/SPA (REQ9-01); invent CI; claim Railway from offline | **PASS** | story Out of scope; run-summary honesty; marker only `pyproject.toml:34–35` |

### P3 note — 4 offline fails vs story DoD

| Claim (run-summary / gate) | Audit verdict | Evidence |
|----------------------------|---------------|----------|
| 4 failed = pre-existing / **out of REQ9-02 AC** | **CONFIRMED out of DoD** | AC-01…03 require ritual existence + marker expression, **not** green suite. Out of scope: Railway verify from `make test`. Failures are SSR/bootstrap schema (not Makefile): `tests/test_gw_ssr_09_packs_visible.py::test_schema_packs_root_env_overrides_without_appconfig`; `tests/test_stories_schema_cross_layer_invariant.py::test_story_select_field_names_exist_in_bootstrap_sql`; `tests/test_supabase_bootstrap_schema.py::test_story_select_fields_all_in_bootstrap_sql`; `tests/test_supabase_bootstrap_schema.py::test_story_select_fields_covered_by_bootstrap`. Live re-run 2026-09-26T12:27:40Z: **886 passed / 4 failed** — same class as gate note. |

**Regression note:** suite dirt exists (bootstrap/ssr) but is **outside** this story’s DoD; does **not** reopen AC-01…03.

---

## 3. Регрессии / gaps

### G1 — Backlog §Verified present-tense vs live post-P3 · severity: **LOW** · **TASKED-likely**

Product shipped; backlog §Verified still asserts pre-P3 «no `test`» as current fact.

| Artifact | Stale claim | Live fact |
|----------|-------------|-----------|
| Backlog §Verified [`:38–43`](../tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md) | `.PHONY: … check-env` — **no `test`**; only serve/dev/simulate/check-env | `.PHONY` includes `test` + `test-live`; targets `Makefile:50–54` |
| Pipeline §Verified | Already As-of-Done + Historical | Aligns with live |
| T01/T02 Code Facts / Gap | As-of-Done; Gap Closed | Aligns with live |

**Как закрыть (P5 hint):** TASKED — As-of-Done vs Historical на backlog §Verified (и при необходимости «Техническое решение (projected)» → as-shipped). Docs-only; **не** reopen product unless Makefile drift.

### G2 — Bullrun §«Актуальная точка» без REQ9-02 · severity: **LOW** · **WAIVED-likely reason=operator**

Fence / overlay: не rewrite §«Актуальная точка». Файл всё ещё стартует с EPIC-M2-24 / ES-03 — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). REQ9-02 story row L670 + T01–T03 L696–698 уже 🔵 Done + gate PASS.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L670 GW-REQ9-02 | 🔵 Done pkg-000097 T01–T03 P3 12:22:28Z · lock C | Product Done | PASS |
| T01 | L696 | 🔵 `-m "not live_integration"` + PHONY `test` | Done | PASS |
| T02 | L697 | 🔵 `-m live_integration` + PHONY `test-live` | Done | PASS |
| T03 | L698 | 🔵 AC-GW-REQ902-01…03 PASS | Gate PASS | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1895 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | backlog §Verified present-tense (no `test`) | **yes** | As-of-Done / Historical |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** 1 (G1).  
**4 offline fails:** documented, **out of story DoD** — not a gap against AC-01…03.  
**WAVE:** n/a (P4).

Handoff: P5 disposition (G1 TASKED-likely; G2 WAIVED-likely). Не закрывать gaps здесь.
