# Note — GW-REQ11-05 provision 200 fixture users (Identity file OTP + secrets)

| Field | Value |
|-------|--------|
| **utc** | `2026-09-29T18:15:05Z` (P3 live verify) |
| **Story** | STORY-GW-REQ11-05 · AC-GW-REQ1105-01…06 |
| **Package** | pkg-000104 |
| **Method** | Supabase signup + Identity `SMS_PROVIDER=file` outbox OTP; gitignored secrets; wire `--life-sim` 1:1 |

## Verdict

**Pass path** = provision verified API accounts for fixture users → secrets file → `--life-sim` resolves **own** Bearer (not `fixture % 20` pool). **K1:** no SPA resident login. **Never** invent `GET /dev/last-otp`. **Never commit** `.secrets/`.

## Preconditions

| Item | Value |
|------|--------|
| Identity | up; `SMS_PROVIDER=file`; `APP_PROFILE` ≠ `pilot` |
| Outbox | `FILE_SMS_OUTBOX_DIR` or default `doge-identity-service/var/sms-outbox` (override `LIFE_SIM_FILE_SMS_OUTBOX_DIR`) |
| Supabase | `SUPABASE_URL` + `SUPABASE_ANON_KEY` (same as SPA signup) |
| Confirm email / signup | Supabase may rate-limit email (`over_email_send_rate_limit`); wait/retry. Prefer demo project with confirm-email off for automation. Emails: `life.sim.user.NNNN@dogestonia.com` |
| Rate limits | Identity `PHONE_RESEND_COOLDOWN_S` (default 60) + `RATE_LIMIT_PHONE_REQUEST_*` — script default `--pace-s 65` |
| Secrets | `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json` (gitignored) |

## Artifacts

| Artifact | Path |
|----------|------|
| Provision script | `tests/sandbox/life_sim_provision_users.py` |
| Helpers | `tests/sandbox/life_sim_provision_lib.py` |
| Secrets dir | `tests/sandbox/.secrets/` (gitignored) |
| Replay wire | `tests/simulation_runner.py --life-sim` + `resolve_fixture_user_bearer_token` |
| Pool M=20 | **deprecated** for new Pass (`life_sim_pool_m20.json`); emergency `LIFE_SIM_USE_POOL_M20=1` |
| Make | `make life-sim-provision-users` / `make simulate-life-sim` |
| Offline tests | `tests/test_gw_req11_05_provision_fixture_users.py` |

## Operator steps

1. Ensure Identity `SMS_PROVIDER=file` and outbox path writable/readable.
2. Smoke: `make life-sim-provision-users LIMIT=2` (or full without LIMIT; long due to pacing).
3. Confirm secrets file exists under `.secrets/` and is **not** staged (`git status --ignored`).
4. Optional verify: password grant → `GET {identity}/me` shows `phone_verified=true`.
5. Wipe demo DB → `LIFE_SIM_DRY_RUN=1 make simulate-life-sim` (offline) or live `--life-sim --wipe-confirmed --max N`.
6. Env: `LIFE_SIM_USERS_CREDS` optional override to a specific generation file.

## Out of scope

- Invent HTTP OTP backdoor.
- Pilot / Telnyx SMS for this automation.
- Regenerate REQ11-01 fixtures.
- SPA resident login as Pass requirement.
