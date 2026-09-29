# Note — GW-REQ11-03 profiled API replay + multi-submitter (no SPA)

| Field | Value |
|-------|--------|
| **utc** | `2026-09-29T14:21:44Z` (P3 live verify) |
| **Story** | STORY-GW-REQ11-03 · AC-GW-REQ1103-01…04 |
| **Package** | pkg-000102 |
| **Method** | extend `simulation_runner` / `simulation_intake_http`; env refs; no invent public APIs |

## Verdict

**Pass path** = profiled **API+JSON** stash→submit replay of REQ11-01 fixtures through pool **M=20** (map 200→20). **No SPA resident login** per run (K1/K4). Wipe/zero of the connected demo DB is an **operator precondition** (no wipe HTTP API invented).

## Artifacts

| Artifact | Path |
|----------|------|
| Fixtures (REQ11-01) | `tests/sandbox/dogestonia_life_sim_{users,stories}_v0_1.json` |
| Profiles (REQ11-02) | `tests/sandbox/profiles/` + `DEMO_LIFE_SIM_PROFILE` |
| Pool M=20 manifest | [`tests/sandbox/life_sim_pool_m20.json`](../../tests/sandbox/life_sim_pool_m20.json) |
| Map 200→20 | [`tests/sandbox/life_sim_fixture_to_pool_map_v0_1.json`](../../tests/sandbox/life_sim_fixture_to_pool_map_v0_1.json) |
| Helpers | [`tests/sandbox/life_sim_replay_lib.py`](../../tests/sandbox/life_sim_replay_lib.py) |
| Runner | `tests/simulation_runner.py --life-sim` |
| Multi-Bearer | `resolve_pool_slot_bearer_token` in `tests/simulation_intake_http.py` |
| Make | `make simulate-life-sim` / `LIFE_SIM_DRY_RUN=1 make simulate-life-sim` |

## Operator steps (live)

1. Wipe/zero the connected **demo** DB (ops procedure; out of scope to invent HTTP wipe).
2. Admin-bootstrap **20** phone_verified users; set `LIFE_SIM_POOL_00_EMAIL`/`PASSWORD` … `_19_*` in `.env.test` (see `.env.test.example`). Never commit secrets.
3. `export DEMO_LIFE_SIM_PROFILE=local` (or `uus-veerenni` + `GATEWAY_URL`).
4. Confirm wipe: `--wipe-confirmed` or `LIFE_SIM_WIPE_CONFIRMED=1`.
5. Run: `make simulate-life-sim` or  
   `.venv/bin/python tests/simulation_runner.py --life-sim --wipe-confirmed [--max N]`.
6. Flow uses existing `POST /story-drafts` + `POST /story-drafts/{id}/submit` only.

## Mapping rule

`pool_slot = (fixture_user_index) % 20` where `life-sim-user-0001` → index 0. Each of 20 slots gets exactly 10 fixture users.

## Out of scope

- Backdate fixture times (REQ11-04).
- Threads / SPA UI / SQL dump as Pass.
- Inventing undocumented public resident login APIs.
