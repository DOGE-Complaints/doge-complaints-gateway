# task-gw-req11-08-t02-shared-config-fail-closed

## Task: implement / tooling — shared config fail-closed (T02)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:31:41Z
- **Package:** pkg-000106
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-01T10:23:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`

## Purpose
Hard shared settings: `SMS_PROVIDER=file` + readable outbox; email `@dogestonia.me`; Auth Supabase = Identity project. Fail-closed if not. Scope #2 · AC-GW-REQ1108-02. Name ≠ create until P3.

## Code Facts
**As-of-Done (P3 2026-10-01T10:31:41Z):**
1. Dedicated fail-closed module Present: `tests/sandbox/life_sim_provision_config.py`.
2. Hard: `SMS_PROVIDER=file` + readable outbox; email `@dogestonia.me`; Identity Auth Supabase force.
3. No invent `GET /dev/last-otp`.

### Historical (scaffold / pre-P3)
1. OTP file path Present in 05 tooling; dedicated fail-closed shared module **Absent**.
2. Email domain historically dogestonia.com / migrating toward dogestonia.me in lib.

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — life_sim_provision_config.py fail-closed file SMS + @dogestonia.me + Identity Auth

Historical gap (pre-P3):
Dedicated fail-closed shared config module Absent.

## Acceptance / DoD
- [x] Fail-closed unless file SMS + outbox readable (AC-02)
- [x] Email domain hard `@dogestonia.me`
- [x] Auth credentials = Identity Supabase (not gateway content DB)
- [x] BULLRUN phases complete when closed

## Where to change
- shared settings module under tests/sandbox/ (P3)

## Out of scope
CLI pack (T01); wave (T03); wipe/provision (T04); invent OTP HTTP.
- Overlay bans:
  - Stay `dev`.
  - `SMS_PROVIDER=file` only; `@dogestonia.me`; Identity Auth Supabase.
  - Pack `users.json` read-only for status; never invent `GET /dev/last-otp`.
  - Never commit secrets; do not reuse REQ11-07 number.
  - Pointer pkg-000106; do not mutate pkg-000100…105.
  - No product provision execute this APPLY turn.
  - Content wipe = REQ11-06 (orthogonal).

## Verification commands
```bash
rg -n 'SMS_PROVIDER|dogestonia.me|FILE_SMS_OUTBOX' doge-complaints-gateway/tests/sandbox/life_sim_provision*.py | head -40
```
