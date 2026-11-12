# task-gw-req11-06-t03-threads-tables-wipe

## Task: implement / tooling — threads tables wipe (T03)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
Wipe verified threads persistence tables only, child→parent: `thread_reaction_marks` → `thread_comments` → `thread_threads`. Optional `THREADS_SUPABASE_*` if separate project. Scope #3 · AC-GW-REQ1106-02 (threads). Name ≠ create until P3.

## Code Facts
1. Verified names: `doge-threads/src/core/infrastructure/supabase_discussion_mappers.py` (`thread_threads`, `thread_comments`); `supabase_marks_mappers.py` (`thread_reaction_marks`).
2. Delete order: marks → comments → threads.
3. Optional override env for separate threads Supabase project (do not invent HTTP wipe API).

## Gap
**As-of-Done (P3):** closed.

No threads wipe path in gateway sandbox script.

## Acceptance / DoD
- [x] Wipes only the three verified threads tables (AC-02 threads)
- [x] Child→parent order
- [x] Optional THREADS_SUPABASE_* documented
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_wipe_node_content.py` (threads delete plan; P3)

## Out of scope
Gateway deletes (T02); dry-run/docs (T04); tests (T05); gate (T06); invent extra threads tables; invent wipe HTTP; Identity DELETE.
- Overlay bans:
  - Stay `dev`.
  - Confirm: `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`.
  - Threads tables: only the three verified names.
  - No Identity DELETE; no invent wipe HTTP.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
rg -n 'THREAD_TABLE|COMMENT_TABLE|MARKS_TABLE|thread_' doge-threads/src/core/infrastructure/supabase_*mappers.py | head -30
# after P3: assert wipe script threads list = marks, comments, threads
```
