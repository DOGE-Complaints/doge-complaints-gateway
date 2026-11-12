# task-gw-req10-01-t02-fixture-sqlite-scan

## Task: docs — fixture/sqlite legacy lifecycle scan (T02)

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
Scan sqlite fixtures / seed SQL used by gateway tests for legacy `RECEIVED`/`received` (and any other non-enum strings). Record present/absent. Scope #2 · AC-GW-REQ1001-02. Inventory only — no fixture rewrite (→ REQ10-02 if needed).

## Code Facts
1. Enum canon: `contracts.py:20–24`.
2. sqlite hydrate: `StoryLifecycleStatus(str(...))` only — `db_sqlite.py:225` (no legacy map).
3. Supabase legacy map (context only): `db_supabase.py:185–188`.
4. Scan result: `RECEIVED`/`received` **absent** as fixture/SQL data; mapper-only — inventory §T02.

## Gap
Closed — scan result written.

## Acceptance / DoD
- [x] Fixture/sqlite scan result: legacy `RECEIVED`/`received` present or absent (AC-GW-REQ1001-02)
- [x] Note any other non-enum strings found
- [x] No production mapper / fixture cleanup in this task
- [x] BULLRUN phases complete when closed

## Where to change
- Evidence note / scan table (P3; may live in same analysis artifact as T01 or sibling)
- Read-only: `tests/`, seed SQL, sqlite fixtures under gateway

## Out of scope
DB DISTINCT (T01); closed list (T03); gate (T04); backfill/mapper slim (REQ10-02).
- Overlay bans:
  - Inventory only; stay `dev`.
  - Do not mutate pkg-000097; pointer is pkg-000098.

## Verification commands
```bash
rg -n 'RECEIVED|received|lifecycle_status' doge-complaints-gateway/tests doge-complaints-gateway/supabase --glob '*.{sql,py,json,yml,yaml}' | head -50
```
