# task-gw-req10-02-t04-remove-debug-io

## Task: implement — remove lifecycle debug file I/O (T04)

## Meta
- **Story:** [STORY-GW-REQ10-02](../STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000099
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-28T17:27:26Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`

## Purpose
Remove absolute debug file I/O to `.cursor/debug-ba94c7.log` (and sibling `#region agent log` in that path) from lifecycle parse — H1 gateway. Scope #3 · AC-GW-REQ1002-04. Cross-cut X-10-02 gateway piece.

## Code Facts
1. **As-of-Done:** No `debug-ba94c7` / `#region agent log` / `.cursor/debug` under `doge-complaints-gateway/src` (`rg` clean); slim `_parse_lifecycle_status` has no file I/O (`db_supabase.py:179–185`).
2. **As-of-Done:** Tests assert no debug path — `tests/test_gw_req10_02_lifecycle_parse.py`.
3. **Historical (pre-P3):** Debug block `:190–221` `#region agent log` writing absolute `.cursor/debug-ba94c7.log` inside `_parse_lifecycle_status` exception path.

## Gap
**Closed (P3 2026-09-28T17:44:10Z):** debug I/O removed; `rg` clean. **G3 SSOT As-of-Done (P6 2026-09-28T17:52:28Z).**

## Acceptance / DoD
- [x] No `.cursor/debug-*.log` writes from production lifecycle path (AC-GW-REQ1002-04)
- [x] `rg` clean under `doge-complaints-gateway/src` for that debug path pattern
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status` (debug block removed at P3)

## Out of scope
Backfill (T01); fixtures (T02); mapper dict slim (T03 — separate AC); tests (T05); gate (T06); H8.
- Overlay bans:
  - Stay `dev`.
  - Do not mutate pkg-000098; pointer is pkg-000099.

## Verification commands
```bash
rg -n 'debug-ba94c7|#region agent log|\.cursor/debug' doge-complaints-gateway/src
```
