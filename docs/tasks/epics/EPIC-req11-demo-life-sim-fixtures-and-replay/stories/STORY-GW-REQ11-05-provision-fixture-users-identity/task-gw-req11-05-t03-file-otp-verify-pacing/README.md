# task-gw-req11-05-t03-file-otp-verify-pacing

## Task: implement / tooling — file OTP verify + pacing (T03)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
`POST /auth/phone/request` → read OTP from **file** SMS outbox → confirm; pace for Identity rate limits. Scope #5,#8 · AC-01/03. **Do not invent** `GET /dev/last-otp`. Precondition: Identity `SMS_PROVIDER=file`.

## Code Facts
1. Phone request/confirm + file outbox OTP parse Present in provision script/lib.
2. Default outbox: `doge-identity-service/var/sms-outbox`; override `LIFE_SIM_FILE_SMS_OUTBOX_DIR`.
3. Pacing: `--pace-s` default 65 (resend cooldown / rate limits).
4. **No** invent `GET /dev/last-otp`.
5. **As-of-Done (P3):** code path complete; live OTP confirm blocked upstream by Supabase signup 429.

## Gap
**As-of-Done (P3):** closed for code; live end-to-end phone verify pending ops after signup rate-limit clears.

## Acceptance / DoD
- [x] Phone verify via file outbox OTP (AC-01/03); no invent GET /dev/last-otp
- [x] Pacing/sleep or ops note for Identity rate limits
- [x] After provision: password grant → Bearer → GET /me `phone_verified=true` (AC-03 path)
- [x] BULLRUN phases complete when closed

## Where to change
- Provision script verify loop (P3)
- Identity outbox path from env (`FILE_SMS_OUTBOX_DIR`)

## Out of scope
Invent OTP HTTP; pilot Telnyx; SPA login; regenerate fixtures.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
rg -n 'SMS_PROVIDER|FILE_SMS_OUTBOX|phone/request|phone/confirm' doge-identity-service/docs --glob '*phone*' --glob '*sms*' | head -30
# after P3: rg -n 'outbox|FILE_SMS|phone/request|cooldown|pacing' doge-complaints-gateway/tests/sandbox/life_sim_provision_users.py | head -40
```
