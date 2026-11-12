# task-gw-req11-06-t05-offline-unit-tests

## Task: test — offline unit tests (T05)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** test
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
Offline/unit or smoke evidence for confirm-gate + ordered delete plan; assert no Identity/`auth.users` paths. AC-GW-REQ1106-04. Name ≠ create until P3.

## Code Facts
1. Target test name pattern: `tests/test_gw_req11_06_*`.
2. Confirm gate and ordered-delete helpers should be unit-testable without live Supabase where feasible.
3. Live wipe is ops/smoke — not required for offline suite.

## Gap
**As-of-Done (P3):** closed.

No `test_gw_req11_06_*` on disk.

## Acceptance / DoD
- [x] Offline tests cover confirm refuse + ordered plan (AC-04)
- [x] Assert wipe code does not reference Identity auth.users delete
- [x] pytest green for offline suite
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/test_gw_req11_06_wipe_node_content.py` (or equivalent; P3)

## Out of scope
Live full wipe as Pass requirement; invent wipe HTTP; Identity DELETE; gate file (T06).
- Overlay bans:
  - Stay `dev`.
  - Confirm + tables locks unchanged.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
# after P3:
# cd doge-complaints-gateway && python -m pytest tests/test_gw_req11_06_*.py -q
```
