# task-gw-req11-08-t04-skip-or-wipe-fixture-auth-provision

## Task: implement / tooling — skip or wipe-fixture-users + provision (T04)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:31:41Z
- **Package:** pkg-000106
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-01T10:23:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`

## Purpose
Modes `skip` (default) or `wipe-fixture-users` (+ confirm); wipe only fixture-derived Auth users; provision path reuse 05; gitignored secrets. Scope #5–#7 · AC-04 · AC-06. Name ≠ create until P3.

## Code Facts
**As-of-Done (P3 2026-10-01T10:31:41Z):**
1. Modes Present: `--mode skip` (default) \| `wipe-fixture-users` (+ `--confirm-wipe-fixture-users` / env); refuse exit 2 without confirm.
2. Wipe targets only fixture-derived Auth users (email/phone derive); not REQ11-06 content.
3. Provision path reuses REQ11-05 `provision_one` (signup → file OTP → `/me`).
4. Secrets `.secrets/` gitignored Present.

### Historical (scaffold / pre-P3)
1. wipe-fixture-users vs skip **Absent**.
2. REQ11-05 provision path Present; secrets `.secrets/` Present; content wipe orthogonal.

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — skip|wipe-fixture-users+confirm; provision_one reuse; secrets gitignored

Historical gap (pre-P3):
Mode switch + fixture-auth wipe Absent.

## Acceptance / DoD
- [x] skip default or wipe-fixture-users with confirm (AC-04)
- [x] Wipe only fixture-derived Auth users; not REQ11-06 content; not non-fixture admins
- [x] Provision path: signup → file OTP → phone_verified; secrets gitignored (AC-06)
- [x] BULLRUN phases complete when closed

## Where to change
- pack-wave CLI modes + secrets write (P3)

## Out of scope
RU manual (T05); invent OTP HTTP; content wipe; commit secrets.
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
# after P3: rg -n 'wipe-fixture|confirm-wipe-fixture|skip' tests/sandbox/life_sim_provision*.py | head -40
```
