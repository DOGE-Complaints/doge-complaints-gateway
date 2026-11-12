# task-gw-req10-02-t03-slim-lifecycle-mapper

## Task: implement — slim `_parse_lifecycle_status` (T03)

## Meta
- **Story:** [STORY-GW-REQ10-02](../STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000099
- **Skill declared:** python-pro
- **Depends on:** T01 (prefer data cleaned first)
- **Scaffolded:** 2026-09-28T17:27:26Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`

## Purpose
Slim `_parse_lifecycle_status`: remove permanent growing legacy dict (`RECEIVED`/`received`). Unknown values still raise / fail closed. Scope #2 · AC-GW-REQ1002-02 · AC-GW-REQ1002-03. Prefer remove special-case; no dual-path.

## Code Facts
1. **As-of-Done:** Parser slim — `src/core/infrastructure/db_supabase.py:179–185` → `StoryLifecycleStatus(str(raw))` only; unknown → `ValueError`.
2. **As-of-Done:** Hydrate call — `_parse_lifecycle_status(...)` at `db_supabase.py:226` inside `_story_record_from_supabase_row`.
3. **As-of-Done:** Enum — `contracts.py:20–24`; sqlite already strict — `db_sqlite.py:225` (no legacy map).
4. **Historical (pre-P3):** Parser span `:179–224`; permanent legacy dict `:185–188` (`RECEIVED`/`received` → ACCEPTED); hydrate call was `:265`.

## Gap
**Closed (P3 2026-09-28T17:44:10Z):** permanent RECEIVED special-case removed; fail-closed kept. **G3 SSOT As-of-Done (P6 2026-09-28T17:52:28Z).**

## Acceptance / DoD
- [x] Mapper no longer depends on permanent RECEIVED special-case (AC-GW-REQ1002-02)
- [x] Unknown lifecycle values still fail closed (AC-GW-REQ1002-03)
- [x] No expanding legacy synonyms; no dual-path complexity
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status` `:179–185`

## Out of scope
Data backfill (T01); fixture confirm (T02); debug I/O removal (T04 — may be same file, separate task); tests (T05); gate (T06); H8.
- Overlay bans:
  - Stay `dev`.
  - Do not mutate pkg-000098; pointer is pkg-000099.
  - Prefer T01 before this task.

## Verification commands
```bash
rg -n 'RECEIVED|received|_parse_lifecycle_status' doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
