# Hard Audit — STORY-GW-REQ10-01 lifecycle_status inventory (2026-09-28)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ10-01-lifecycle-status-inventory`](../tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md) (T01–T04, **pkg-000098**).  
**Pipeline:** [`…/STORY-GW-REQ10-01-lifecycle-status-inventory.md`](../tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/STORY-GW-REQ10-01-lifecycle-status-inventory.md).  
**Pkg:** [`pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml`](../tasks/gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ10-01.md`](../tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t04-story-gate/story-acceptance-gate-STORY-GW-REQ10-01.md) PASS **2026-09-28T17:16:40Z**.  
**Run-summary:** [`run-summary-20260928-1716-gw-req10-01-p3.md`](../tasks/run-reports/run-summary-20260928-1716-gw-req10-01-p3.md).  
**Inventory evidence:** [`inventory-gw-req10-01-lifecycle-status-2026-09-28.md`](./inventory-gw-req10-01-lifecycle-status-2026-09-28.md).  
**Прогон этого аудита:** `utc_now: 2026-09-28T17:20:10Z`. Branch: **`dev`**. Fixture/SQL/`*.db` re-scan + code line verify (enum/mapper/sqlite). Hosted DISTINCT **not** re-polled this turn — AC-01 satisfied by written inventory artifact (P3).

> **Природа аудита.** P4 hard audit evidence vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T04 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L717 / L724–727. AC из backlog/pipeline Target verbatim — **не** invent.

---

## 1. Итог: product AC-01…03 / T01–T04 закрыты; 2 OPEN gaps (0 Critical/High/Medium); TASKED-likely = 0

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Written DISTINCT inventory (or blocker) | [`inventory…§T01`](./inventory-gw-req10-01-lifecycle-status-2026-09-28.md) — 162 rows; 4 distinct; DB reachable; no blocker | ✅ PASS |
| **T02** | Fixture/sqlite `RECEIVED`/`received` present/absent | Re-scan: **absent** as fixture/SQL data; no checked-in `*.db`/`*.sqlite`; tests use `StoryLifecycleStatus.*` | ✅ PASS |
| **T03** | Closed list enum / normalize / fail-closed | [`inventory…§T03`](./inventory-gw-req10-01-lifecycle-status-2026-09-28.md); enum [`contracts.py:20–24`](../../src/core/domain/contracts.py); legacy map [`db_supabase.py:185–188`](../../src/core/infrastructure/db_supabase.py) | ✅ PASS |
| **T04** | Gate AC-01…03 | Gate PASS 17:16:40Z | ✅ PASS |

**Verdict product:** GW-REQ10-01 **исполнена по AC** (inventory-only; no mapper/backfill).  
**Product Story Done (AC/DoD) = yes. Empty OPEN gap-list = no** (G1 WAIVED-likely out-of-DoD debug I/O; G2 WAIVED-likely operator bullrun lead).  
**WAVE:** n/a (P4).

---

## 2. AC overlay facts (findings, not fix)

| AC (backlog Target) | Result | Evidence |
|---------------------|--------|----------|
| AC-01 written inventory of hosted/test DISTINCT (or blocker) | **PASS** | Inventory §T01 on disk; counts claimed: `clustered` 140, `ready_for_profile` 20, `RECEIVED` 1, `accepted` 1; `partial_ready` 0; lowercase `received` 0. P4 did **not** re-query PostgREST → live delta **Unknown** this turn (artifact exists → AC met). |
| AC-02 fixture/sqlite scan RECEIVED/received | **PASS** | `rg` over `tests/` + `supabase/**/*.sql`: no lifecycle fixture values `RECEIVED`/`received`. Column DDL only — [`000_full_init.sql:13`](../../supabase/bootstrap/000_full_init.sql), [`20260423_1500_init_db_wave.sql:12`](../../supabase/migrations/20260423_1500_init_db_wave.sql). No checked-in sqlite DB files. Mapper-only keys [`db_supabase.py:186–187`](../../src/core/infrastructure/db_supabase.py). sqlite hydrate strict [`db_sqlite.py:225`](../../src/core/infrastructure/db_sqlite.py). |
| AC-03 closed list normalize vs fail-closed | **PASS** | Inventory §T03: **enum-legal** = 4 StrEnum values; **normalize-to-accepted** = `RECEIVED`,`received`; **unexpected** = none observed in hosted DISTINCT. |
| Out: cleanup/mapper slim/debug → REQ10-02; H8 skip | **PASS** | Story Out of scope; inventory Non-goals; no product mapper change in this story (legacy map + debug I/O still present — expected). |

### Code facts re-verified (reference, not product change)

| Fact | Path | Match inventory/story? |
|------|------|------------------------|
| Enum 4 values | `contracts.py:20–24` | ✅ |
| Legacy map RECEIVED/received → ACCEPTED | `db_supabase.py:185–188` | ✅ |
| Hydrate uses parser | `db_supabase.py:265` | ✅ |
| sqlite no legacy map | `db_sqlite.py:225` | ✅ |
| Branch policy | `git branch --show-current` → **`dev`** | ✅ (stay default-dev-only) |

### Observation — debug agent log (out of REQ10-01 DoD)

[`db_supabase.py:190–221`](../../src/core/infrastructure/db_supabase.py) `#region agent log` writes absolute path under `.cursor/debug-ba94c7.log`. Story Out of scope / inventory Non-goals: debug removal → **REQ10-02**. **Not** an AC fail for inventory story.

---

## 3. Регрессии / gaps

### G1 — Debug I/O + permanent RECEIVED map still in product · severity: **LOW** · **WAIVED-likely reason=out-of-DoD**

Inventory story correctly left mapper/debug untouched. Dirt remains for REQ10-02 (backfill + slim). Does **not** reopen AC-01…03.

**Как закрыть:** not in this story — follow STORY-GW-REQ10-02 (already ⚪ Todo on bullrun L718). No TASKED against REQ10-01 AC.

### G2 — Bullrun §«Актуальная точка» без REQ10-01 · severity: **LOW** · **WAIVED-likely reason=operator**

Fence / overlay: не rewrite §«Актуальная точка». File still starts with EPIC-M2-24 / ES-03 — [`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md). REQ10-01 story row L717 + T01–T04 L724–727 already 🔵 Done + gate PASS.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

### Note — context path drift (not a story gap)

Operator fence listed gate under `docs/tasks/run-reports/task-gw-req10-01-t04-story-gate/…` — **path absent on disk**. Canonical gate: epic task folder (run-summary + bullrun L717 link correctly). Informational only.

### Note — SSOT present-tense

Backlog + pipeline §Verified already point to inventory + Known DISTINCT; T01–T03 Code Facts / Gap Closed. **No G1-style SSOT TASKED** this wave.

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L717 GW-REQ10-01 | 🔵 Done pkg-000098 T01–T04 P3 17:16:40Z · inventory only | Product Done | PASS |
| T01 | L724 | 🔵 hosted DISTINCT 162/4; RECEIVED×1 | Done | PASS (artifact) |
| T02 | L725 | 🔵 RECEIVED/received absent as fixture data | Done | PASS (re-scan) |
| T03 | L726 | 🔵 enum vs normalize vs fail-closed | Done | PASS |
| T04 | L727 | 🔵 AC-GW-REQ1001-01…03 PASS | Gate PASS | PASS |
| REQ10-02 | L718 | ⚪ Todo (unblocked) | n/a this story | noted |
| §Актуальная точка | L17–20 | EPIC-M2-24 / ES-03 lead | n/a (fence) | **G2** WAIVED-likely |
| Journal | L1923 | P3 execute entry | present | PASS |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Low | debug I/O + RECEIVED map remain | **no** (WAIVED-likely out-of-DoD → REQ10-02) | do not reopen inventory AC |
| G2 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 0 · Low 2.  
**Actionable TASKED-likely:** **0**.  
**WAVE:** n/a (P4).

Handoff: P5 disposition (likely WAIVE G1 out-of-DoD + G2 operator). Не закрывать gaps здесь.
