# task-gw-req10-02-t05-lifecycle-parse-tests

## Task: tests — lifecycle parse / fail-closed / no-debug (T05)

## Meta
- **Story:** [STORY-GW-REQ10-02](../STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000099
- **Skill declared:** python-pro
- **Depends on:** T03–T04
- **Scaffolded:** 2026-09-28T17:27:26Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`

## Purpose
Pytest covering: mapper without permanent RECEIVED special-case; unknown values fail closed; no debug path under `src/`. AC-GW-REQ1002-02…04. Exact test file(s) chosen at P3 via Grep (story: Unknown until Grep).

## Code Facts
1. Parser under test: `db_supabase.py:179–224` / hydrate `:265`.
2. Enum: `contracts.py:20–24`.
3. Existing lifecycle tests may exist under `tests/` — discover at P3 (do not invent names in P1).

## Gap
No dedicated post-slim/post-debug-removal coverage locked to this story yet.

## Acceptance / DoD
- [x] Tests assert no permanent RECEIVED map dependency (AC-02)
- [x] Tests assert unknown → fail closed (AC-03)
- [x] `rg`/assert no `.cursor/debug-*` writes from lifecycle path (AC-04)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/` (new or extend existing — Grep at P3)
- Possibly minimal helpers only if needed

## Out of scope
Product backfill ops (T01); invent public APIs; H8; gate (T06).
- Overlay bans:
  - Stay `dev`.
  - Do not mutate pkg-000098; pointer is pkg-000099.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/ -k 'lifecycle or parse_lifecycle or story_repository' --maxfail=20
rg -n 'debug-ba94c7|#region agent log' doge-complaints-gateway/src
```
