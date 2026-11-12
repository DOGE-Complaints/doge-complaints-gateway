# task-gw-req11-03-t01-wire-fixtures-and-profile

## Task: implement — wire life-sim fixtures + named profile (T01)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Package:** pkg-000102
- **Skill declared:** python-pro
- **Depends on:** REQ11-01 + REQ11-02 Done (on disk)
- **Scaffolded:** 2026-09-29T14:13:56Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`

## Purpose
Load REQ11-01 life-sim JSON + REQ11-02 named profile selection into the replay driver. Scope #3 · AC-GW-REQ1103-02. Do **not** regenerate fixtures.

## Code Facts
1. Life-sim users/stories: `tests/sandbox/dogestonia_life_sim_{users,stories}_v0_1.json` (Present).
2. Profiles: `tests/sandbox/profiles/` + `demo_life_sim_profiles.py` / `DEMO_LIFE_SIM_PROFILE` (Present).
3. **As-of-Done (P3/P6):** `--life-sim` loads fixtures + `select_profile` / `DEMO_LIFE_SIM_PROFILE` via `life_sim_replay_lib` + `simulation_runner.main_life_sim`.
4. **Historical (pre-P3):** Runner loaded canvas scenario array only; multi-fixture submitters / pool map Absent.

## Gap
**As-of-Done (P3):** closed — fixtures+profile wired; see gate + run-summary.  
**Historical:** Replay driver not wired to life-sim fixtures + named profile selection.

## Acceptance / DoD
- [x] Replay path can select profile + load REQ11-01 fixture scale (AC-GW-REQ1103-02)
- [x] No fixture regeneration in this task
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/simulation_runner.py` and/or new helper under `tests/` (P3)
- Consume `tests/sandbox/profiles/` + life-sim JSON paths

## Out of scope
Pool bootstrap (T02); map/Bearer (T03); wipe→replay loop (T04); docs (T05); gate (T06); backdate; invent APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000102; do not mutate pkg-000100/101.
  - No secrets in git.

## Verification commands
```bash
rg -n 'life_sim|DEMO_LIFE_SIM_PROFILE|profiles/' doge-complaints-gateway/tests --glob '*sim*' --glob '*profile*' | head -40
ls doge-complaints-gateway/tests/sandbox/dogestonia_life_sim_*_v0_1.json doge-complaints-gateway/tests/sandbox/profiles/
```
