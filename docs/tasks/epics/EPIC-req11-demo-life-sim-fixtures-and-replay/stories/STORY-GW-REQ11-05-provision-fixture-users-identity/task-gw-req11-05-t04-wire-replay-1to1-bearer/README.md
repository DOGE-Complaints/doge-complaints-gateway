# task-gw-req11-05-t04-wire-replay-1to1-bearer

## Task: implement / tooling — wire replay 1:1 Bearer (T04)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** T01–T03 (secrets file available)
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
`--life-sim` resolve Bearer from secrets by `fixture_user_id` (1:1); supersede/deprecate pool M=20 for new Pass. Scope #9 · AC-GW-REQ1105-04.

## Code Facts
1. `resolve_fixture_user_bearer_token` Present in `simulation_intake_http.py`.
2. `--life-sim` prefers secrets 1:1; pool M=20 only if `LIFE_SIM_USE_POOL_M20=1`.
3. Pool manifest `schema_note` marked deprecated.
4. Dry-run: Auth label shows secrets-1:1 with ready count.

## Gap
**As-of-Done (P3):** closed for wire; live stash→submit needs provisioned secrets after signup unblocked.

## Acceptance / DoD
- [x] Replay submits with fixture user’s own Bearer from secrets (AC-04)
- [x] Pool M=20 deprecated for new Pass (docs/INDEX; file may remain)
- [x] No SPA resident login required (K1)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_replay_lib.py`, `tests/simulation_runner.py`, optionally `tests/simulation_intake_http.py` (P3)

## Out of scope
Regenerate fixtures; invent OTP HTTP; delete pool file unless wave says; product SPA login.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
rg -n 'resolve_pool_slot_bearer_token|LIFE_SIM_POOL|POOL_MANIFEST|fixture_user_id' doge-complaints-gateway/tests/sandbox/life_sim_replay_lib.py doge-complaints-gateway/tests/simulation_runner.py | head -40
# after P3: rg -n 'secrets|generation_id|1:1|life_sim_users_creds' doge-complaints-gateway/tests/sandbox/life_sim_replay_lib.py | head -40
```
