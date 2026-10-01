# task-gw-req11-10-t01-fail-closed-pack-dir-readonly-stories

## Task: implement / tooling — fail-closed pack dir + read-only stories (T01)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:35:43Z
- **Package:** pkg-000108
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md`

## Purpose
Hard fail-closed `LIFE_SIM_PACK_DIR` / `PACK_DIR`; read pack `stories.json` only; never write replay statuses into fixture. Scope #2 · AC-GW-REQ1110-01.

## Code Facts
**As-of-Done (P3 2026-10-01T11:35:43Z):**
1. `life_sim_replay_lib.require_life_sim_pack_dir()` fail-closed; Make `life-sim-replay-pack-wave` exit 2 without pack.
2. CLI mtime guard `_assert_never_write_stories_json`.
3. Offline: `test_require_pack_dir_fail_closed`, `test_make_fail_closed_without_pack_dir` PASS.

### Historical (scaffold / pre-P3)
Pack-wave replay fail-closed Absent; `simulate-life-sim` optional pack.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] CLI/Make STOP without pack (AC-01)
- [x] Reads pack `stories.json`
- [x] Never writes statuses into fixture `stories.json`
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_replay_lib.py` · `life_sim_replay_pack_wave.py` · Makefile

## Out of scope
Wave-state (T02); Bearer/reuse (T03); tests suite (T04); RU (T05); gate (T06).

## Verification commands
```bash
make life-sim-replay-pack-wave  # exit 2 without LIFE_SIM_PACK_DIR
```
