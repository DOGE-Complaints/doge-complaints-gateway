# task-gw-req10-01-t03-closed-list-normalize-note

## Task: docs — closed list enum vs normalize vs fail-closed (T03)

## Meta
- **Story:** [STORY-GW-REQ10-01](../STORY-GW-REQ10-01-lifecycle-status-inventory.md)
- **Type:** docs / inventory
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000098
- **Skill declared:** python-pro
- **Depends on:** T01–T02 (inputs)
- **Scaffolded:** 2026-09-28T17:11:07Z
- **Done (P3):** 2026-09-28T17:16:40Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md`

## Purpose
Produce closed list from T01+T02: enum-legal vs to-normalize-to-`accepted` vs unexpected (fail-closed candidates). Feeds REQ10-02 cleanup. Scope #3 · AC-GW-REQ1001-03. No cleanup execution here.

## Code Facts
1. Enum-legal set: `accepted`, `partial_ready`, `ready_for_profile`, `clustered` — `contracts.py:20–24`.
2. Known legacy candidates (code): `RECEIVED` / `received` → ACCEPTED map in `db_supabase.py:185–188`.
3. T01/T02 evidence drives closed list — inventory §T03 (hosted `RECEIVED`×1; unexpected none).

## Gap
Closed — closed list written in inventory note.

## Acceptance / DoD
- [x] Explicit list: enum-legal vs normalize-to-`accepted` vs unexpected fail-closed (AC-GW-REQ1001-03)
- [x] Traceable to T01/T02 evidence (or blocker + code-known legacy only)
- [x] No production backfill / mapper slim in this task
- [x] BULLRUN phases complete when closed

## Where to change
- Closed-list section in inventory evidence note (P3)

## Out of scope
DB query (T01); fixture scan body (T02); gate (T04); REQ10-02 cleanup.
- Overlay bans:
  - Inventory only; stay `dev`.
  - Do not mutate pkg-000097; pointer is pkg-000098.

## Verification commands
```bash
rg -n 'normalize-to-accepted|fail-closed|enum-legal|AC-GW-REQ1001-03' doge-complaints-gateway/docs/analysis/ --glob '*req10*' --glob '*lifecycle*'
```
