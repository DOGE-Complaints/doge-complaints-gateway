# task-gw-req11-01-t04-canvas-relation-doc

## Task: docs — relation to canvas v0_1/v0_2 for life-sim (T04)

## Meta
- **Story:** [STORY-GW-REQ11-01](../STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Closed:** 2026-09-29T13:43:36Z
- **Package:** pkg-000100
- **Skill declared:** python-pro
- **Depends on:** T01 (prefer fixtures exist or paths named)
- **Scaffolded:** 2026-09-29T13:22:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`

## Purpose
Document relation to (or supersede for life-sim) canvas v0_1/v0_2 — no invent public APIs. Scope #4 · AC-GW-REQ1101-04.

## Code Facts
1. Canvas: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (len=130), `…_v0_2.json` (len=18).
2. Runner: `tests/simulation_runner.py:155-185` loads `SIMULATION_CANVAS_PATH`; `run_scenario_stash_submit` `:120`.
3. **As-of-Done:** relation note `docs/analysis/note-gw-req11-01-life-sim-vs-canvas-2026-09-29.md` — life-sim supersedes canvas for multi-user scale; canvas remains runner scenario array.
4. REQ11-03 consumes fixtures for replay (out of this task).
5. **Historical:** no written life-sim vs canvas relation note pre-P3 T04.

## Gap
**CLOSED (P3):** canvas relation note on disk. Present-tense «no note» moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Documented how fixtures relate to canvas v0_1/v0_2 for life-sim (AC-GW-REQ1101-04)
- [x] No invent public APIs
- [x] Doc path under gateway docs (analysis/runtime/tests README — chosen at P3)
- [x] BULLRUN phases complete when closed

## Where to change
- New/updated note under `doge-complaints-gateway/docs/analysis/` or adjacent runtime/tests doc (P3)
- Optional cross-link from story Verified / package INDEX

## Out of scope
Fixture generation (T01–T03); gate (T05); invent APIs; profiles/replay/backdate.
- Overlay bans:
  - Stay `dev`.
  - Docs-only; pointer pkg-000100.

## Verification commands
```bash
rg -n 'v0_1|v0_2|life-sim|canvas|supersede' doge-complaints-gateway/docs --glob '*req11*' --glob '*sim*' | head -40
```
