# task-gw-req11-01-t03-timestamps-2026-exp-curve

## Task: implement/verify — 2026 exponential timestamps (T03)

## Meta
- **Story:** [STORY-GW-REQ11-01](../STORY-GW-REQ11-01-fixtures-users-stories-scale.md)
- **Type:** implement / verify
- **Status:** 🟢 Done
- **Closed:** 2026-09-29T13:43:36Z
- **Package:** pkg-000100
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-29T13:22:23Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-01-fixtures-users-stories-scale.md`

## Purpose
Timestamps span calendar 2026 with exponential intensity (breakpoint 2026-09-30; ~25% / ~75% mass split). Scope #3 · AC-GW-REQ1101-03.

## Code Facts
1. Operator lock: calendar **2026**; breakpoint **2026-09-30**; mass **~25%** pre / **~75%** post.
2. Canvas fixtures are not this curve: `tests/sandbox/dogestonia_simulation_canvas_v0_*.json`.
3. **As-of-Done:** life-sim `created_at` span 2026-01-01…2026-12-31; pre **0.2498** / post **0.7502**; post density > pre (`test_ac03_*`).
4. **Historical:** Life-sim scale fixtures / 2026 curve were **Absent** until T01/P3.

## Gap
**CLOSED (P3):** 2026 exponential curve + mass split on disk. Present-tense absence moved to Historical (P6 G1 SSOT).

## Acceptance / DoD
- [x] Timestamps follow 2026 exponential curve per lock (AC-GW-REQ1101-03)
- [x] Breakpoint 2026-09-30; ~25% pre / ~75% post mass measurable
- [x] BULLRUN phases complete when closed

## Where to change
- Fixture story timestamp fields / generator (same artifacts as T01)
- Optional verify helper/test for mass split (P3)

## Out of scope
Scale (T01); langs (T02); canvas doc (T04); gate (T05); backdate contract (REQ11-04); invent public APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000100; do not mutate pkg-000099.

## Verification commands
```bash
# P3: histogram / mass split vs 2026-09-30
rg -n '2026-09-30|created_at|timestamp|breakpoint' doge-complaints-gateway/tests doge-complaints-gateway/scripts --glob '*req11*' --glob '*sim*' | head -40
```
