# task-gw-req11-10-t03-cli-make-reuse-replay-bearer

## Task: implement / tooling — CLI + Make + reuse replay + Bearer (T03)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:35:43Z
- **Package:** pkg-000108
- **Skill declared:** python-pro
- **Depends on:** T01, T02
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Decision Ref:** backlog STORY-GW-REQ11-10

## Purpose
CLI + Make `life-sim-replay-pack-wave`; reuse lib/runner; Bearer by `fixture_user_id` fail-closed missing; smoke `--limit`. AC-03 · AC-04.

## Code Facts
**As-of-Done (P3 2026-10-01T11:35:43Z):**
1. `tests/sandbox/life_sim_replay_pack_wave.py` + Make Present.
2. Reuses `simulation_runner.run_life_sim_payload_stash_submit` + backdate helper.
3. `_preflight_missing_creds` fail-closed; dry-run LIMIT=2 ok on pack 1661.
4. Live LIMIT=2 leftover: Supabase login Tunnel 403 (auth unreachable) — full pack submit not completed this P3.

## Gap
**As-of-Done:** closed for product entry; live full leftover documented.

## Acceptance / DoD
- [x] Bearer by `fixture_user_id`; fail-closed missing (AC-03)
- [x] Reuses REQ11-03 path; Make Present (AC-04)
- [x] Smoke `--limit` / dry-run
- [x] No invent intake/force-cluster
- [x] BULLRUN phases complete when closed

## Where to change
- `life_sim_replay_pack_wave.py` · Makefile

## Out of scope
Auth provision; threads; invent APIs.

## Verification commands
```bash
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<id> LIFE_SIM_REPLAY_PACK_WAVE_DRY_RUN=1 make life-sim-replay-pack-wave LIMIT=2
```
