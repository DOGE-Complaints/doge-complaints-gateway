# task-gw-req11-06-t01-wipe-script-confirm-gate

## Task: implement / tooling — wipe script + confirm gate (T01)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
Sandbox script + Make target scaffold: refuse wipe without `--confirm-wipe` or `LIFE_SIM_WIPE_CONFIRMED=1`. Scope #1,#4 · AC-GW-REQ1106-01. Name ≠ create until P3.

## Code Facts
1. Script Present: `tests/sandbox/life_sim_wipe_node_content.py` + `life_sim_wipe_lib.py`.
2. Make Present: `life-sim-wipe-node-content`.
3. Runner documents precondition `--wipe-confirmed` / `LIFE_SIM_WIPE_CONFIRMED` in `simulation_runner.py` (no DELETE).
4. Confirm: `--confirm-wipe` or `LIFE_SIM_WIPE_CONFIRMED=1`; refuse exit 2 without.
5. **As-of-Done (P3):** confirm gate + Make shipped; gate PASS 2026-09-30T07:56:35Z.

## Gap
**As-of-Done (P3):** closed — Script/Make Present; confirm-gate implemented.

## Acceptance / DoD
- [x] Script + Make present (AC-01)
- [x] Exit non-zero without `--confirm-wipe` and without `LIFE_SIM_WIPE_CONFIRMED=1`
- [x] Accepts either confirm form for destructive path
- [x] BULLRUN phases complete when closed

## Where to change
- Target: `tests/sandbox/life_sim_wipe_node_content.py` + `Makefile` `life-sim-wipe-node-content` (P3)

## Out of scope
Gateway deletes (T02); threads wipe (T03); dry-run/docs (T04); unit tests (T05); gate (T06); invent wipe HTTP API; Identity DELETE; DROP schema.
- Overlay bans:
  - Stay `dev`.
  - Confirm: `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`.
  - Tables: `REQUIRED_READINESS_TABLES` + verified threads only.
  - No Identity `auth.users` DELETE; no invent wipe HTTP.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.
  - No product wipe execute this APPLY turn.

## Verification commands
```bash
# after P3:
# ls doge-complaints-gateway/tests/sandbox/life_sim_wipe_node_content.py
# rg -n 'confirm-wipe|LIFE_SIM_WIPE_CONFIRMED' doge-complaints-gateway/tests/sandbox/life_sim_wipe_node_content.py | head -40
# rg -n 'life-sim-wipe-node-content' doge-complaints-gateway/Makefile | head -10
```
