# Hard Audit — STORY-GW-REQ11-11 life-sim stories fixture contract v2 (2026-10-02)

**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями.  
**Scope:** [`STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) (T01–T05, **pkg-000109**) · backlog [`…/STORY-GW-REQ11-11-…`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md).  
**Pkg:** [`pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml`](../tasks/gateway-active-packages/pkg-000109-20261002-gw-req11-11-life-sim-stories-fixture-contract-v2.yaml).  
**Gate:** [`story-acceptance-gate-STORY-GW-REQ11-11.md`](../tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2/task-gw-req11-11-t05-story-gate/story-acceptance-gate-STORY-GW-REQ11-11.md) PASS **2026-10-02T08:53:45Z**.  
**Run-summary:** [`run-summary-20261002-0853-gw-req11-11-p3.md`](../tasks/run-reports/run-summary-20261002-0853-gw-req11-11-p3.md).  
**Прогон этого аудита:** `utc_now: 2026-10-02T08:55:22Z`. Branch: **`dev`**. Mapping note Present; pack still **6 keys** × **1661**; story task tree = **md-only**; Intake `Narrative` fields cited in note exist in [`contracts.py`](../../src/core/intake/contracts.py).

> **Природа аудита.** P4 hard audit docs/product vs AC. Реализацию не предлагаю — только findings.  
> **Bullrun:** §«Актуальная точка» **не** переписывался. Touchpoints story / T01–T05 актуализированы **в этом отчёте** (§4) относительно [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) L775 / L985–995. AC из Target verbatim — **не** invent.

---

## 1. Итог: docs contract AC PASS; mapping note Present; no generator/adapter in 11 deliverable; 3 gaps; TASKED-likely = G2 (+ G1 workspace)

| Таск | Claim | Подтверждение | Статус |
|------|-------|---------------|--------|
| **T01** | Flat keys + join + content | Note §1–3 | ✅ PASS |
| **T02** | Out-of-fixture + scale locks | Note §5–6 | ✅ PASS |
| **T03** | Mapping note fixture→Narrative | [`note-gw-req11-11-…-2026-10-02.md`](./note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md) §4 | ✅ PASS |
| **T04** | Compat Partial vs v2 Pass | Note §7; pack 6-key Partial on disk | ✅ PASS |
| **T05** | Gate AC-01…05 | Gate PASS 08:53:45Z | ✅ PASS |

**Verdict product (docs-only framing):** GW-REQ11-11 **исполнена по gate** — contract note covers AC-01…05; successor implement = **REQ11-12**.  
**No generator/adapter leaked into 11 deliverable:** story folder has only `.md`; run-summary / gate / note §8 / §Consumer handoff state implement → 12; no new generator/adapter module under this story.  
**Product Story Done (AC/DoD) = yes**. **Empty OPEN gap-list = no**.  
**WAVE:** n/a (P4).

---

## 2. AC overlay

| AC | Result | Evidence |
|----|--------|----------|
| AC-01 Flat layout + join + Narrative-aligned content keys | **PASS** | Note §1–3: flat lock; join `fixture_story_id`/`fixture_user_id`/`created_at`/`language`; content keys incl. i18n / `session_language` / `location_query` / `canonical_*` / `institution_i18n` |
| AC-02 Out of fixture list | **PASS** | Note §5: no `story_id` / lifecycle / `submitter_*` / `payload_hash` / invent axis IDs / invent `gpt_signals` |
| AC-03 Mapping table in named analysis note | **PASS** | Note §4 Present at locked path; maps to intake `Narrative` fields Present in `contracts.py` (`original_text`, `summary`, `canonical_labels`, …) |
| AC-04 Compat: 6-key Partial; v2 Pass once 12 | **PASS** | Note §7; disk pack keys = 6 (`body`,`created_at`,`fixture_story_id`,`fixture_user_id`,`language`,`title`) len **1661** |
| AC-05 Scale locks + pack ≠ StoryRecord | **PASS** | Note §6 restates 200 / Gauss 8.5·σ2·[1,20] / 60/30/10 / 2026 curve; ≠ `StoryRecord` dump |

### Generator / adapter leak check (focus)

| Check | Result |
|-------|--------|
| Mapping note Present | ✅ `docs/analysis/note-gw-req11-11-life-sim-stories-fixture-v2-to-narrative-2026-10-02.md` |
| Story task artifacts | ✅ markdown only under `STORY-GW-REQ11-11-…/` |
| New generator/adapter file for v2 in this story | **Absent** (by design → 12) |
| Pack regenerated to v2 in this story | **No** — still 6-key |
| Gate / run-summary claim docs-only | ✅ |

### Code facts re-verified

| Fact | Path | Match? |
|------|------|--------|
| Mapping note | `note-gw-req11-11-…-2026-10-02.md` | ✅ |
| Pack 6-key × 1661 | `…/stories.json` | ✅ |
| Thin adapter cite (pre-existing) | `life_sim_story_to_intake_payload` | ✅ Present (cite-only) |
| Intake Narrative | `src/core/intake/contracts.py` | ✅ fields align with note |
| Branch | `dev` | ✅ |
| §Актуальная точка | still EPIC-M2-24 / ES-03 | ✅ untouched |

---

## 3. Регрессии / gaps

### G1 — Uncommitted workspace drift on `life_sim_replay_lib.py` · severity: **MEDIUM** · **TASKED-likely** (ops / restore) · not AC invent for 11

`git status`: **`M tests/sandbox/life_sim_replay_lib.py`**. Diff (working tree) **removes** `require_life_sim_pack_dir` and `PACK_DIR` alias from `resolve_life_sim_pack_dir` — sibling **REQ11-10** fail-closed standard. This is **not** a v2 rich-adapter leak into 11; it is **workspace drift** orthogonal to docs-only Done claim. If committed as-is → regression risk for pack-wave replay.

**Как закрыть (P5 hint):** restore/discard dirty (or land only under intentional story that owns the change). Do **not** attribute to REQ11-11 AC reopen.

### G2 — Backlog §Verified still scaffold present-tense vs Done · severity: **LOW** · **TASKED-likely**

Backlog [`STORY-GW-REQ11-11…md:59–69`](../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-11-life-sim-stories-fixture-contract-v2.md) §Verified still «as of scaffold» (6-key / generator / adapter facts) without As-of-Done vs Historical split, while Meta Status=Done and mapping note Present. Pipeline already has As-of-Done + Historical. Task READMEs T01–T05 use As-of-Done.

**Как закрыть:** TASKED docs — As-of-Done vs Historical on backlog §Verified (mirror REQ11-08…10).

### G3 — Bullrun §«Актуальная точка» без REQ11-11 · severity: **LOW** · **WAIVED-likely reason=operator**

[`bullrun-launch-index.md:17–20`](../tasks/bullrun-launch-index.md) still EPIC-M2-24 / ES-03. Story L775 + tasks L989–993 Done.

**Как закрыть:** не в этой P4-волне (WAIVED operator).

---

## 4. Task / story touchpoints (bullrun актуализация — статус в отчёте)

Факт-проверка строк [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) vs disk (P4 **не** правил файл; §Актуальная точка untouched).

| ID | Bullrun row | Bullrun claim | Product vs AC | Audit |
|----|-------------|---------------|---------------|-------|
| Story | L775 GW-REQ11-11 | 🔵 Done · gate PASS · docs contract + mapping note · pkg-000109 · successor 12 | Product Done (docs) | PASS |
| T01 | L989 | ✅ AC-01 flat + join + content | Done | PASS |
| T02 | L990 | ✅ AC-02 + AC-05 | Done | PASS |
| T03 | L991 | ✅ AC-03 · note | Done | PASS |
| T04 | L992 | ✅ AC-04 | Done | PASS |
| T05 | L993 | ✅ AC-01…05 PASS | Gate PASS | PASS |
| Journal | L2193 | P3 execute 0853 | present | PASS |
| §Актуальная точка | L17–20 | EPIC-M2-24 lead | n/a | **G3** WAIVED-likely |

---

## 5. Gap list for P5 disposition

| ID | Sev | Kind | TASKED-likely | Notes |
|----|-----|------|---------------|-------|
| G1 | Medium | uncommitted `life_sim_replay_lib` removes pack-dir fail-closed | **yes** (ops restore) | not 11 adapter leak; sibling-10 risk |
| G2 | Low | backlog §Verified scaffold vs Done | **yes** | As-of-Done / Historical |
| G3 | Low | bullrun MVP lead | **no** (WAIVED-likely operator) | do not rewrite §Актуальная точка |

**Counts:** Critical 0 · High 0 · Medium 1 · Low 2.  
**Actionable TASKED-likely:** up to 2 (G1, G2).  
**WAVE:** n/a (P4).

Handoff: P5 disposition. Не закрывать gaps здесь.
