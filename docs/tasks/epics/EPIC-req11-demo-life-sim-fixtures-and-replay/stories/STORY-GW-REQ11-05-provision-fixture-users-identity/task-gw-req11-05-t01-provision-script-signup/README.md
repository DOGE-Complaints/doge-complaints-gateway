# task-gw-req11-05-t01-provision-script-signup

## Task: implement / tooling — provision script signup (T01)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** REQ11-01 users JSON on disk
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
Sandbox script + Make target: read users JSON; deterministic email/+372; Supabase signup loop for 200 (or `--limit`). Scope #1–4 · AC-GW-REQ1105-01 (signup loop). Name ≠ create until P3.

## Code Facts
1. Script Present: `tests/sandbox/life_sim_provision_users.py` + `make life-sim-provision-users`.
2. Helpers Present: `tests/sandbox/life_sim_provision_lib.py` (email/phone/password).
3. Users JSON Present: `tests/sandbox/dogestonia_life_sim_users_v0_1.json` (200).
4. Email domain: `life.sim.user.NNNN@dogestonia.com` (Supabase-valid).
5. **As-of-Done (P3):** signup loop + `--limit` + Make; live smoke blocked by Supabase email rate limit (429).

## Gap
**As-of-Done (P3):** closed for code path. Live full-200 pending ops (rate-limit / confirm-email).

## Acceptance / DoD
- [x] Script/Make can signup fixture users from users JSON (AC-01 signup loop; `--limit` supported)
- [x] Deterministic email + unique +372 E.164 from `fixture_user_id`
- [x] Uses SUPABASE_URL + SUPABASE_ANON_KEY; no secrets committed
- [x] BULLRUN phases complete when closed

## Where to change
- Target: `tests/sandbox/life_sim_provision_users.py` + Makefile `life-sim-provision-users` (P3)
- Read `tests/sandbox/dogestonia_life_sim_users_v0_1.json`

## Out of scope
Secrets file write (T02); file OTP verify (T03); replay wire (T04); docs (T05); unit tests (T06); gate (T07); invent GET /dev/last-otp; Telnyx pilot; regenerate fixtures; SPA resident login.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
ls doge-complaints-gateway/tests/sandbox/dogestonia_life_sim_users_v0_1.json
# after P3:
# ls doge-complaints-gateway/tests/sandbox/life_sim_provision_users.py
# rg -n 'signUp|supabase|fixture_user_id|--limit' doge-complaints-gateway/tests/sandbox/life_sim_provision_users.py | head -40
```
