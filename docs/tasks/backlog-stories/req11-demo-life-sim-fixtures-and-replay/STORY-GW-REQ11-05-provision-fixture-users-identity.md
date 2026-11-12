# STORY-GW-REQ11-05 — Provision 200 fixture users (Identity + secrets file)

## Meta
- **Key:** `STORY-GW-REQ11-05-provision-fixture-users-identity`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** ✅ Done P3 2026-09-29T18:15:05Z · gate PASS* · live signup 429 blocker · [`pkg-000104`](../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml)
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Operative package:** [`../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml`](../../gateway-active-packages/pkg-000104-20260929-gw-req11-05-provision-fixture-users-identity.yaml)
- **Тип:** tooling / auth provision for life-sim
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) §4 (multi-fixture submitter), §6 Open Q3; **GW-11-06**
- **Parent product:** REQ11 §3.3 Auth model, §7.2 K1/K4
- **Justification:** operator lock 2026-09-29 — real verified accounts for all fixture users + secrets file; supersede pool M=20 for live Pass
- **Siblings:** threads `04-…` (consumes verified Bearer later); spa `20-…` (verify-only; K1 no SPA resident demo login)
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** STORY-GW-REQ11-01 (users JSON); soft STORY-GW-REQ11-02 (profile identity / Supabase env refs)
- **Improves live Pass for:** STORY-GW-REQ11-03 / 04 (replace pool 0/20 blocker with 1:1 creds)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** historical (pre-P3) — paths were targets until implement wave

---

## Goal

Для всех **200** записей из life-sim users JSON создать **настоящие** аккаунты (email+password), пройти телефонную верификацию так, чтобы submit через gateway принимал их Bearer, записать credentials в **gitignored secrets-файл поколения**, и подключить life-sim replay к **1 fixture user → 1 аккаунт → его Bearer** (без пула 20).

---

## Scope

1. **Скрипт в gateway sandbox** (target name): `tests/sandbox/life_sim_provision_users.py` + Make target (e.g. `make life-sim-provision-users`) — materialize only on implement.
2. Читать [`dogestonia_life_sim_users_v0_1.json`](../../../tests/sandbox/dogestonia_life_sim_users_v0_1.json); на каждого пользователя: **CSPRNG** пароль (Python `secrets`; **≥24** chars, mixed class acceptable if entropy sufficient).
3. Детерминированные **email** и уникальные **+372** E.164 из `fixture_user_id` (`PHONE_ONE_ACCOUNT_PER_NUMBER=true`).
4. **Signup:** Supabase Auth email+password (`SUPABASE_URL` + `SUPABASE_ANON_KEY`) — тот же контур, что SPA `supabase.auth.signUp` ([`LoginPage.jsx`](../../../../../spa-app/src/pages/LoginPage.jsx)).
5. **Verify:** `POST {identity}/auth/phone/request` → читать OTP из **file SMS outbox** → `POST …/confirm`. Precondition Identity: **`SMS_PROVIDER=file`**, `APP_PROFILE` ≠ `pilot` (file forbidden on pilot per PV-10). **Не** полагаться на `SMS_PROVIDER=mock` для HTTP automation (OTP не отдаётся по сети).
6. **Secrets output:** gitignored файл на прогон, target e.g. `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json` (+ `.gitignore` for `.secrets/`). Min fields: `fixture_user_id`, `email`, `password`, `phone_e164`, `generation_id`, `created_at_utc`. **Never commit.**
7. **Idempotency:** prefer **skip-if-email-exists** + refresh/update secrets file entry; else fail-closed with clear error (lock in P1.3).
8. **Rate limits:** pacing for Identity `RATE_LIMIT_PHONE_REQUEST_*` / `PHONE_RESEND_COOLDOWN_S` (sleep or ops note); 200 without pause will fail.
9. **Wire to replay:** supersede pool M=20 — `--life-sim` / bearer resolve читает email+password из secrets file по `fixture_user_id` → password grant → Bearer for stash→submit. [`life_sim_pool_m20.json`](../../../tests/sandbox/life_sim_pool_m20.json) mark **deprecated** in docs/INDEX (do not delete unless implement wave says so).
10. **Smoke:** `--limit` small N and full N=200 ops: login → `GET {identity}/me` with `phone_verified=true` → one successful stash→submit with that Bearer.

## Out of scope

- SPA login UX / requiring fixture-resident browser login for demo Pass (K1).
- Threads comment/reaction seed (sibling threads REQ11).
- Invent HTTP `GET /dev/last-otp` (PV-10 chose file sink; no invent).
- Switching pilot/Telnyx production SMS to `file`.
- Regenerating 1661 stories (REQ11-01 Done).
- Implementing the script in the same turn as this backlog story (**name ≠ create**).

---

## Verified current state (As-of-Done 2026-09-29T18:19:28Z · P6 G2)

| Fact | Evidence |
|------|----------|
| 200 users JSON | `tests/sandbox/dogestonia_life_sim_users_v0_1.json` |
| Provision script + Make | `tests/sandbox/life_sim_provision_users.py` + `life_sim_provision_lib.py`; `make life-sim-provision-users` |
| Secrets gitignored | `tests/sandbox/.secrets/` + gateway `.gitignore`; never commit |
| File OTP (no invent HTTP) | outbox parse; Identity `SMS_PROVIDER=file`; **no** `GET /dev/last-otp` |
| Replay 1:1 Bearer | `resolve_fixture_user_bearer_token`; `--life-sim` secrets-1:1 |
| Pool M=20 | **deprecated** for new Pass (`life_sim_pool_m20.json` kept; `LIFE_SIM_USE_POOL_M20=1` emergency) |
| Gate / live residual | PASS* 2026-09-29T18:15:05Z; live signup Supabase **429** = G1 WAIVED operator |

### Historical (pre-P3 backlog Verified)

| Fact | Evidence (then) |
|------|-----------------|
| No life-sim signup/provision script | sandbox inventory; sync-mirror 2026-09-29 |
| Replay uses pool M=20 | `life_sim_pool_m20.json`; INDEX lock; STORY-GW-REQ11-03 |
| Signup in product SPA | `spa-app/src/pages/LoginPage.jsx` `supabase.auth.signUp` |
| Phone verify API | Identity `POST /auth/phone/request`, `POST /auth/phone/confirm` |
| `SMS_PROVIDER=mock` — OTP not over HTTP | Identity onboarding runbook |
| File sink writes OTP to disk | PV-10; `SMS_PROVIDER=file` + `FILE_SMS_OUTBOX_DIR` |

---

## Target / AC

- [x] **AC-GW-REQ1105-01:** Script creates/updates verified accounts for all **200** fixture users (or `--limit` for smoke).
- [x] **AC-GW-REQ1105-02:** Passwords CSPRNG, strong (≥24); credentials only in gitignored secrets file with `generation_id`.
- [x] **AC-GW-REQ1105-03:** After provision: password grant → Bearer → `GET /me` shows `phone_verified=true`.
- [x] **AC-GW-REQ1105-04:** Life-sim replay submits a story using that fixture user’s **own** Bearer from secrets file (not `fixture % 20` pool map).
- [x] **AC-GW-REQ1105-05:** Docs list preconditions: Identity `SMS_PROVIDER=file`, outbox path, Supabase env, rate-limit pacing; secrets never committed.
- [x] **AC-GW-REQ1105-06:** Offline/unit tests where feasible (email/phone derivation, password strength, secrets path hygiene); live provision via ops/`--limit` smoke.

---

## Code touchpoints (As-of-Done)

| Area | Path |
|------|------|
| Provision script | `tests/sandbox/life_sim_provision_users.py` + `life_sim_provision_lib.py` |
| Secrets dir | `tests/sandbox/.secrets/` + gateway `.gitignore` |
| Replay wire | `tests/simulation_runner.py --life-sim`, `simulation_intake_http.resolve_fixture_user_bearer_token`, `life_sim_replay_lib.py` |
| Profiles | `tests/sandbox/profiles/*.json` |
| Deprecated pool | `tests/sandbox/life_sim_pool_m20.json` (emergency `LIFE_SIM_USE_POOL_M20=1`) |
| Makefile | `life-sim-provision-users` / `simulate-life-sim` |

### Historical (pre-P3 «named only» targets)

| Area | Then |
|------|------|
| Provision script | named only until implement |
| Secrets / wire / Make | targets until P3 |

---

## Dependencies

- REQ11-01 fixtures on disk.
- Soft: REQ11-02 profile URLs / env.
- Identity running with `SMS_PROVIDER=file` for automated OTP read (not mock-over-HTTP).
- Operator: live signup may hit Supabase email rate limit (G1 WAIVED); do not invent Identity OTP HTTP backdoor; never commit secrets.
