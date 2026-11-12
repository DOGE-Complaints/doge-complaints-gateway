# task-gw-req11-03-t04-wipe-profiled-replay-runner

## Task: implement — wipe → profiled stash→submit replay (T04)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Package:** pkg-000102
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-09-29T14:13:56Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`

## Purpose
Wipe/zero → profiled stash→submit replay via **extend** `simulation_runner` / `simulation_intake_http`; first fill connected DB. Scope #1+#3 · AC-GW-REQ1103-01.

## Code Facts
1. stash→submit: `tests/simulation_intake_http.py` `post_stash_and_submit_http` (extended, not replaced).
2. **As-of-Done (P3/P6):** `simulation_runner.py --life-sim` + `--wipe-confirmed` / `LIFE_SIM_WIPE_CONFIRMED`; `make simulate-life-sim`; dry-run supported.
3. Make canvas `simulate` still present for legacy canvas path.
4. **Historical (pre-P3):** Profiled life-sim multi-submitter wipe→replay **Absent**.

## Gap
**As-of-Done (P3):** closed — wipe-confirmed → profiled replay path; see gate + run-summary (live fill blocked by G1 WAIVED pool env).  
**Historical:** No wipe/zero → profiled life-sim replay that fills gateway pipeline on first run.

## Acceptance / DoD
- [x] Wipe/zero → profiled replay → stories enter gateway pipeline (AC-GW-REQ1103-01)
- [x] Extends existing runner/HTTP helpers (no parallel invent product APIs)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/simulation_runner.py`, `tests/simulation_intake_http.py`, optional Makefile target (P3)
- Document wipe precondition for operators (cross-link T05)

## Out of scope
Backdate fixture times (REQ11-04); threads/spa; SQL dump Pass; invent public APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000102.
  - No secrets in git.

## Verification commands
```bash
rg -n 'wipe|replay|life_sim|post_stash_and_submit|simulate' doge-complaints-gateway/tests doge-complaints-gateway/Makefile | head -40
```
