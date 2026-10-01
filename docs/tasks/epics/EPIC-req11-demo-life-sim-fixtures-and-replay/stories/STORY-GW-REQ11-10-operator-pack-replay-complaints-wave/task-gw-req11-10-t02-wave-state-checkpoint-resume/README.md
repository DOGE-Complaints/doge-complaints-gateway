# task-gw-req11-10-t02-wave-state-checkpoint-resume

## Task: implement / tooling — wave-state checkpoint + resume (T02)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:35:43Z
- **Package:** pkg-000108
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Decision Ref:** backlog STORY-GW-REQ11-10

## Purpose
Wave-state per `fixture_story_id`: pending|submitted|failed; checkpoint; resume skips submitted. AC-02.

## Code Facts
**As-of-Done (P3 2026-10-01T11:35:43Z):**
1. `life_sim_replay_wave_store.ReplayWaveStore` → `waves/<wave_id>/replay_state.json`.
2. Offline `test_wave_checkpoint_and_resume_skips_submitted` PASS.
3. Path gitignored under `life_sim_packs/**/waves/`.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] Wave-state tracks each `fixture_story_id` (AC-02)
- [x] Checkpoint after each complaint
- [x] Resume skips `submitted`
- [x] State outside fixture `stories.json`
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_replay_wave_store.py`

## Out of scope
Pack gate (T01); CLI Bearer (T03); tests (T04); RU (T05); gate (T06).

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_10_replay_pack_wave.py::test_wave_checkpoint_and_resume_skips_submitted
```
