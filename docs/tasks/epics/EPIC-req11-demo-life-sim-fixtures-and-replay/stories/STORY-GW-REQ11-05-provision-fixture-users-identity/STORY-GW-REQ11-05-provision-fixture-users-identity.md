# STORY-GW-REQ11-05 — Provision 200 fixture users (Identity + secrets file)

## Meta
- **Key:** `STORY-GW-REQ11-05-provision-fixture-users-identity`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Тип:** tooling / auth provision for life-sim
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4 (multi-fixture submitter), §6 Open Q3; **GW-11-06**
- **decision_ref:** backlog REQ11-05 · REQ55 §4/§6 · GW-11-06 · REQ11 §3.3/§7.2 K1/K4 · operator lock 200 1:1 + file OTP
- **Skill declared:** python-pro
- **Operative package:** [`../../../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml`](../../../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml)
- **Git:** `dev`
- **Operator locks:** 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login; OTP via `SMS_PROVIDER=file` (no invent GET /dev/last-otp)
- **Зависит от:** STORY-GW-REQ11-01 (users JSON); soft STORY-GW-REQ11-02
- **Scaffolded:** 2026-09-29T18:09:49Z

## Nested tasks (pkg-000104)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-05-t01-provision-script-signup`](./task-gw-req11-05-t01-provision-script-signup/README.md) | Done |
| T02 | [`task-gw-req11-05-t02-csprng-secrets-gitignore`](./task-gw-req11-05-t02-csprng-secrets-gitignore/README.md) | Done |
| T03 | [`task-gw-req11-05-t03-file-otp-verify-pacing`](./task-gw-req11-05-t03-file-otp-verify-pacing/README.md) | Done |
| T04 | [`task-gw-req11-05-t04-wire-replay-1to1-bearer`](./task-gw-req11-05-t04-wire-replay-1to1-bearer/README.md) | Done |
| T05 | [`task-gw-req11-05-t05-operator-docs-preconditions`](./task-gw-req11-05-t05-operator-docs-preconditions/README.md) | Done |
| T06 | [`task-gw-req11-05-t06-offline-unit-tests`](./task-gw-req11-05-t06-offline-unit-tests/README.md) | Done |
| T07 | [`task-gw-req11-05-t07-story-gate`](./task-gw-req11-05-t07-story-gate/README.md) | Done |
| T08 | [`task-gw-req11-05-t08-audit-g2-as-of-done-ssot`](./task-gw-req11-05-t08-audit-g2-as-of-done-ssot/README.md) | Done · G2 CLOSED P6 |

## Goal

Для всех **200** записей из life-sim users JSON создать **настоящие** аккаунты (email+password), пройти телефонную верификацию так, чтобы submit через gateway принимал их Bearer, записать credentials в **gitignored secrets-файл поколения**, и подключить life-sim replay к **1 fixture user → 1 аккаунт → его Bearer** (без пула 20).

## Scope

1. **Скрипт в gateway sandbox** (target name): `tests/sandbox/life_sim_provision_users.py` + Make target (e.g. `make life-sim-provision-users`) — materialize only on implement.
2. Читать [`dogestonia_life_sim_users_v0_1.json`](../../../../../../tests/sandbox/dogestonia_life_sim_users_v0_1.json); на каждого пользователя: **CSPRNG** пароль (Python `secrets`; **≥24** chars, mixed class acceptable if entropy sufficient).
3. Детерминированные **email** и уникальные **+372** E.164 из `fixture_user_id` (`PHONE_ONE_ACCOUNT_PER_NUMBER=true`).
4. **Signup:** Supabase Auth email+password (`SUPABASE_URL` + `SUPABASE_ANON_KEY`) — тот же контур, что SPA `supabase.auth.signUp` ([`LoginPage.jsx`](../../../../../../../spa-app/src/pages/LoginPage.jsx)).
5. **Verify:** `POST {identity}/auth/phone/request` → читать OTP из **file SMS outbox** → `POST …/confirm`. Precondition Identity: **`SMS_PROVIDER=file`**, `APP_PROFILE` ≠ `pilot` (file forbidden on pilot per PV-10). **Не** полагаться на `SMS_PROVIDER=mock` для HTTP automation (OTP не отдаётся по сети).
6. **Secrets output:** gitignored файл на прогон, target e.g. `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json` (+ `.gitignore` for `.secrets/`). Min fields: `fixture_user_id`, `email`, `password`, `phone_e164`, `generation_id`, `created_at_utc`. **Never commit.**
7. **Idempotency:** prefer **skip-if-email-exists** + refresh/update secrets file entry; else fail-closed with clear error (lock in P1.3).
8. **Rate limits:** pacing for Identity `RATE_LIMIT_PHONE_REQUEST_*` / `PHONE_RESEND_COOLDOWN_S` (sleep or ops note); 200 without pause will fail.
9. **Wire to replay:** supersede pool M=20 — `--life-sim` / bearer resolve читает email+password из secrets file по `fixture_user_id` → password grant → Bearer for stash→submit. [`life_sim_pool_m20.json`](../../../../../../tests/sandbox/life_sim_pool_m20.json) mark **deprecated** in docs/INDEX (do not delete unless implement wave says so).
10. **Smoke:** `--limit` small N and full N=200 ops: login → `GET {identity}/me` with `phone_verified=true` → one successful stash→submit with that Bearer.

## Out of scope

- SPA login UX / requiring fixture-resident browser login for demo Pass (K1).
- Threads comment/reaction seed (sibling threads REQ11).
- Invent HTTP `GET /dev/last-otp` (PV-10 chose file sink; no invent).
- Switching pilot/Telnyx production SMS to `file`.
- Regenerating 1661 stories (REQ11-01 Done).
- Implementing the script in the same turn as scaffold (**name ≠ create** / no product execute this APPLY).

## Verified current state (As-of-Done 2026-09-29T18:15:05Z)

| Fact | Evidence |
|------|----------|
| Provision script + Make | `tests/sandbox/life_sim_provision_users.py`, `make life-sim-provision-users` |
| CSPRNG secrets gitignored | `tests/sandbox/.secrets/` + `.gitignore` |
| File OTP path (no invent HTTP) | outbox parse in `life_sim_provision_lib.py` |
| Replay 1:1 | `resolve_fixture_user_bearer_token`; pool M=20 deprecated |
| Docs | `docs/analysis/note-gw-req11-05-provision-fixture-users-identity-2026-09-29.md` |
| Offline tests | `tests/test_gw_req11_05_provision_fixture_users.py` 10 passed |
| Live smoke | Supabase signup **429** `over_email_send_rate_limit` (operator blocker) |

## Verified current state (scaffold 2026-09-29T18:09:49Z)

| Fact | Evidence |
|------|----------|
| 200 users JSON | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` |
| No life-sim signup/provision script | Absent `tests/sandbox/life_sim_provision_users.py` |
| Replay uses pool M=20 | `tests/sandbox/life_sim_pool_m20.json`; `life_sim_replay_lib.py` |
| Signup in product SPA | `spa-app/src/pages/LoginPage.jsx` `supabase.auth.signUp` |
| Phone verify API | Identity `POST /auth/phone/request`, `POST /auth/phone/confirm` |
| File sink OTP | PV-10; `SMS_PROVIDER=file` + `FILE_SMS_OUTBOX_DIR` |

## Target / AC

- [x] **AC-GW-REQ1105-01:** Script creates/updates verified accounts for all **200** fixture users (or `--limit` for smoke).
- [x] **AC-GW-REQ1105-02:** Passwords CSPRNG, strong (≥24); credentials only in gitignored secrets file with `generation_id`.
- [x] **AC-GW-REQ1105-03:** After provision: password grant → Bearer → `GET /me` shows `phone_verified=true`.
- [x] **AC-GW-REQ1105-04:** Life-sim replay submits a story using that fixture user’s **own** Bearer from secrets file (not `fixture % 20` pool map).
- [x] **AC-GW-REQ1105-05:** Docs list preconditions: Identity `SMS_PROVIDER=file`, outbox path, Supabase env, rate-limit pacing; secrets never committed.
- [x] **AC-GW-REQ1105-06:** Offline/unit tests where feasible (email/phone derivation, password strength, secrets path hygiene); live provision via ops/`--limit` smoke.

## Code touchpoints (As-of-Done)

| Area | Path |
|------|------|
| Provision script | `tests/sandbox/life_sim_provision_users.py` + `life_sim_provision_lib.py` |
| Secrets dir | `tests/sandbox/.secrets/` + gateway `.gitignore` |
| Replay wire | `tests/simulation_runner.py --life-sim`, `simulation_intake_http.resolve_fixture_user_bearer_token`, `life_sim_replay_lib.py` |
| Profiles | `tests/sandbox/profiles/*.json` |
| Deprecated pool | `tests/sandbox/life_sim_pool_m20.json` (`LIFE_SIM_USE_POOL_M20=1` emergency) |
| Makefile | `life-sim-provision-users` / `simulate-life-sim` |

### Historical (scaffold «named only» / implement-wave targets)

| Area | Then |
|------|------|
| Provision script | named only until P3 |
| Secrets / wire / Make | targets until P3 |

## Dependencies

- REQ11-01 fixtures on disk.
- Soft: REQ11-02 profile URLs / env.
- Identity running with `SMS_PROVIDER=file` for automated OTP read (not mock-over-HTTP).
- Operator: P2 → P3 implement; do not invent Identity OTP HTTP backdoor; never commit secrets.
