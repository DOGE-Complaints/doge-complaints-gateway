# task-gw-req11-01-t01-users-stories-scale-fixtures

## Task: implement — users + stories JSON at locked scale (T01)

## Meta
- **Story:** [STORY-GW-REQ11-01](../STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Type:** implement / fixtures
- **Status:** 🟢 Done
- **Closed:** 2026-09-29T13:43:36Z
- **Package:** pkg-000100
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-29T13:22:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`

## Purpose
On-disk users + stories JSON at locked scale (200 users; Gaussian mean 8.5 / σ 2.0 / clamp [1, 20] → ~1700 stories order). Scope #1 · AC-GW-REQ1101-01. Paths chosen at P3 (name ≠ create until then).

## Code Facts
1. Runner loads canvas JSON → stash→submit: `tests/simulation_runner.py:155-185`, `run_scenario_stash_submit` `:120` (unchanged consumer).
2. Canvas sizes: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (len=130), `…_v0_2.json` (len=18).
3. **As-of-Done:** life-sim fixtures on disk — `dogestonia_life_sim_users_v0_1.json` (200); `…_stories_v0_1.json` (1661); mean 8.305; clamp [3,13]⊂[1,20]; generator `generate_dogestonia_life_sim_fixtures_v0_1.py`.
4. Operator lock: 200 users; Gaussian mean 8.5, σ 2.0, clamp [1, 20].
5. **Historical:** Multi-user / Gaussian / 2026 exp fixtures were **Absent** pre-P3 (story Verified / REQ §3).

## Gap
**CLOSED (P3):** fixtures at locked scale on disk. Present-tense absence claims moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Fixture artifacts on disk (users + stories) at locked scale (AC-GW-REQ1101-01)
- [x] Scale matches operator lock (200; Gaussian 8.5/σ2.0/[1,20] → ~1700 stories order)
- [x] New fixture paths named/created at P3 only (name ≠ create before P3)
- [x] BULLRUN phases complete when closed

## Where to change
- New fixture JSON paths under gateway tests/sandbox or agreed P3 location (chosen at P3)
- Optional generator script under `scripts/` or `tests/` (P3)

## Out of scope
Language mix assert (T02); timestamps curve (T03); canvas relation doc (T04); gate (T05); profiles/replay/backdate (REQ11-02/03/04); invent public APIs.
- Overlay bans:
  - Stay `dev`.
  - Do not mutate pkg-000099; pointer is pkg-000100.
  - Fixtures only this story.

## Verification commands
```bash
# P3: count users==200; stories≈1700 order; Gaussian per-user counts in [1,20]
rg -n 'users|stories|gaussian|8\.5' doge-complaints-gateway/tests doge-complaints-gateway/scripts --glob '*req11*' --glob '*sim*' | head -40
```
