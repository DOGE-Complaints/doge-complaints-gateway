# STORY-GW-REQ11-01 — Users+stories JSON fixtures (scale, languages, 2026 curve)

## Meta
- **Key:** `STORY-GW-REQ11-01-fixtures-users-stories-scale`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** fixtures / dataset generation
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md)
- **Parent product:** REQ11 §3.1–3.2, §6.1 **GW-11-01/02**, §7.1 D2/D5/D6
- **Justification:** [`brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md`](../../../../../../docs/analysis/brief-req-uus-veerenni-demo-life-simulation-2026-09-29.md); [`status-simulation-story-data-assembly-2026-09-29.md`](../../../../analysis/status-simulation-story-data-assembly-2026-09-29.md)
- **decision_ref:** backlog REQ11-01 · REQ55 · brief/status justifications · REQ11 §3.1–3.2/§6.1 GW-11-01/02
- **Skill declared:** python-pro · soft code-documenter
- **Operative package:** [`../../../../gateway-active-packages/pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml`](../../../../gateway-active-packages/pkg-000100-20260929-gw-req11-01-fixtures-users-stories-scale.yaml)
- **Git:** `dev`
- **Operator lock (scale):** 200 users; Gaussian mean 8.5, σ 2.0, clamp [1, 20]; langs 60/30/10; 2026 + breakpoint 2026-09-30; mass ~25% pre / ~75% post
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ11-03
- **Scaffolded:** 2026-09-29T13:22:23Z
- **P3 Done:** 2026-09-29T13:43:36Z · gate PASS · [`run-summary`](../../../../run-reports/run-summary-20260929-1343-gw-req11-01-p3.md)

## Nested tasks (pkg-000100)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-01-t01-users-stories-scale-fixtures`](./task-gw-req11-01-t01-users-stories-scale-fixtures/README.md) | Done |
| T02 | [`task-gw-req11-01-t02-language-mix-60-30-10`](./task-gw-req11-01-t02-language-mix-60-30-10/README.md) | Done |
| T03 | [`task-gw-req11-01-t03-timestamps-2026-exp-curve`](./task-gw-req11-01-t03-timestamps-2026-exp-curve/README.md) | Done |
| T04 | [`task-gw-req11-01-t04-canvas-relation-doc`](./task-gw-req11-01-t04-canvas-relation-doc/README.md) | Done |
| T05 | [`task-gw-req11-01-t05-story-gate`](./task-gw-req11-01-t05-story-gate/README.md) | Done |
| T06 | [`task-gw-req11-01-t06-audit-g1-as-of-done-ssot`](./task-gw-req11-01-t06-audit-g1-as-of-done-ssot/README.md) | Done (P6 G1 CLOSED 2026-09-29T13:50:53Z) |

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

### As-of-Done (P3 2026-09-29T13:43:36Z)

| Fact | Path |
|------|------|
| Life-sim users (200) | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` |
| Life-sim stories (1661) | `tests/sandbox/dogestonia_life_sim_stories_v0_1.json` |
| Generator | `tests/sandbox/generate_dogestonia_life_sim_fixtures_v0_1.py` |
| Meta | `tests/sandbox/dogestonia_life_sim_fixtures_v0_1_meta.json` |
| Canvas relation note | `docs/analysis/note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md` |
| Tests | `tests/test_gw_req11_01_life_sim_fixtures.py` (4 passed) |

### Historical (pre-P3)

| Fact | Path |
|------|------|
| Runner loads canvas JSON array → stash→submit | `tests/simulation_runner.py:155-185`, `run_scenario_stash_submit` `:120` |
| Canvas sizes 130 / 18 | `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (len=130), `…_v0_2.json` (len=18) |
| Multi-user / Gaussian / 2026 exp fixtures | **were Absent** before P3 |

## Target / AC

- [x] **AC-GW-REQ1101-01:** Fixture artifacts on disk (users + stories) at locked scale (D2 / GW-11-01).
- [x] **AC-GW-REQ1101-02:** Language mix measurable ≈ 60/30/10 (D5 / GW-11-02).
- [x] **AC-GW-REQ1101-03:** Timestamps follow 2026 exponential curve per lock (D6 / GW-11-02).
- [x] **AC-GW-REQ1101-04:** Documented how fixtures relate to canvas v0_1/v0_2 for life-sim.

## Code touchpoints

- Fixtures: paths above; runner still canvas-shaped until REQ11-03.
- No invent public APIs (`fixture_*` keys on-disk only).

## Dependencies

- Operator scale lock recorded in package INDEX (2026-09-29).
