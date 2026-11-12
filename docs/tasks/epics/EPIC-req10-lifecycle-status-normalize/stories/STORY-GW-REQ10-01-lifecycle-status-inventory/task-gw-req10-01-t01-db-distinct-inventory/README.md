# task-gw-req10-01-t01-db-distinct-inventory

## Task: docs — DISTINCT hosted/test lifecycle_status inventory (T01)

## Meta
- **Story:** [STORY-GW-REQ10-01](../STORY-GW-REQ10-01-lifecycle-status-inventory.md)
- **Type:** docs / inventory
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000098
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-28T17:11:07Z
- **Done (P3):** 2026-09-28T17:16:40Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md`

## Purpose
Inventory distinct `lifecycle_status` values in hosted/test Supabase (operator-accessible). Write evidence under gateway `docs/analysis/` (path chosen at P3; do not invent schema). If DB unreachable → document operator blocker. Scope #1 · AC-GW-REQ1001-01. Inventory only — no backfill.

## Code Facts
1. Enum canon: `StoryLifecycleStatus` — `src/core/domain/contracts.py:20–24`.
2. Distinct live/test DB set: **Known** — see inventory note §T01 (162 rows; 4 distinct; `RECEIVED`×1).
3. Supabase legacy map exists (out of this task): `db_supabase.py:179–224`.
4. Evidence: [`docs/analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md`](../../../../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md).

## Gap
Closed — inventory written; DB reachable (no blocker).

## Acceptance / DoD
- [x] Written inventory of distinct hosted/test `lifecycle_status` values **or** documented operator blocker if DB unreachable (AC-GW-REQ1001-01)
- [x] Evidence path under gateway `docs/analysis/` (chosen at P3; no invent schema)
- [x] No production backfill / mapper change
- [x] BULLRUN phases complete when closed

## Where to change
- New/updated evidence note under `doge-complaints-gateway/docs/analysis/` (P3)
- Read-only DB query (ops)

## Out of scope
Fixture scan (T02); closed list (T03); gate (T04); backfill/mapper slim/debug removal (REQ10-02); invent schema; H8.
- Overlay bans:
  - Inventory only.
  - Stay `dev`.
  - Do not mutate pkg-000097; pointer is pkg-000098.

## Verification commands
```bash
# P3: DISTINCT query evidence or blocker note path
rg -n 'lifecycle_status|DISTINCT|blocker' doge-complaints-gateway/docs/analysis/ --glob '*req10*' --glob '*lifecycle*'
```
