# STORY-GW-REQ11-01 — Users+stories JSON fixtures (scale, languages, 2026 curve)

## Meta
- **Key:** `STORY-GW-REQ11-01-fixtures-users-stories-scale`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) · P3 2026-09-29T13:43:36Z · pkg-000100 gate PASS · audit T06 Done (`gw_req11_01_audit_followup` 2026-09-29T13:50:53Z)
- **Audit follow-up:** [`task-gw-req11-01-t06-audit-g1-as-of-done-ssot`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-01-fixtures-users-stories-scale/task-gw-req11-01-t06-audit-g1-as-of-done-ssot/README.md) · G1 CLOSED P6 2026-09-29T13:50:53Z
- **Тип:** fixtures / dataset generation
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 **GW-11-01/02**, §7.1 D2/D5/D6
- **Justification:** [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md); [`status-simulation-story-data-assembly-2026-09-29.md`](../../../analysis/status-simulation-story-data-assembly-2026-09-29.md)
- **Siblings:** threads `04-…`; spa `20-…`
- **Skill declared (future P3):** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator lock (scale):** 200 users; Gaussian mean 8.5, σ 2.0, clamp [1, 20]; langs 60/30/10; 2026 + breakpoint 2026-09-30; mass ~25% pre / ~75% post
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ11-03
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

## Scope

1. On-disk users + stories JSON at locked scale (200 users; Gaussian mean 8.5 / σ 2.0 / clamp [1, 20] → ~1700 stories order).
2. Language mix measurable ≈ 60% et / 30% ru / 10% en.
3. Timestamps span calendar 2026 with exponential intensity (breakpoint 2026-09-30; ~25% / ~75% mass split).
4. Document relation to (or supersede for life-sim) canvas v0_1/v0_2 — no invent public APIs.

## Out of scope

- Named profiles / HTTP replay / multi-Bearer (→ REQ11-02/03).
- Backdate contract (→ REQ11-04).
- Threads/spa; Identity SPA accounts; SQL dump Pass path.

## Verified current state

### As-of-Done (P3 2026-09-29T13:43:36Z · SSOT sync P6 2026-09-29T13:50:53Z)

| Fact | Path |
|------|------|
| Life-sim users (200) | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` |
| Life-sim stories (1661; mean 8.305; clamp [3,13]⊂[1,20]) | `tests/sandbox/dogestonia_life_sim_stories_v0_1.json` |
| Generator + meta | `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py`; `…_fixtures_v0_1_meta.json` (langs et·ru·en 0.602·0.2926·0.1054; mass pre·post 0.2498·0.7502 @ 2026-09-30) |
| Canvas relation note | `docs/analysis/note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md` |
| Tests | `tests/test_gw_req11_01_life_sim_fixtures.py` |

### Historical (pre-P3)

| Fact | Path |
|------|------|
| Runner loads canvas JSON array → stash→submit | `tests/simulation_runner.py:155-185`, `run_scenario_stash_submit` `:120` |
| Canvas sizes 130 / 18 | `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (len=130), `…_v0_2.json` (len=18) |
| Multi-user / Gaussian / 2026 exp fixtures | **were Absent** (REQ §3) until P3 |

## Target / AC

- [x] **AC-GW-REQ1101-01:** Fixture artifacts on disk (users + stories) at locked scale (D2 / GW-11-01).
- [x] **AC-GW-REQ1101-02:** Language mix measurable ≈ 60/30/10 (D5 / GW-11-02).
- [x] **AC-GW-REQ1101-03:** Timestamps follow 2026 exponential curve per lock (D6 / GW-11-02).
- [x] **AC-GW-REQ1101-04:** Documented how fixtures relate to canvas v0_1/v0_2 for life-sim.

## Code touchpoints

- Life-sim fixtures: paths in As-of-Done above; runner still canvas-shaped until REQ11-03.
- No invent public APIs (`fixture_*` keys on-disk only).

## Dependencies

- Operator scale lock recorded in package INDEX (2026-09-29).
