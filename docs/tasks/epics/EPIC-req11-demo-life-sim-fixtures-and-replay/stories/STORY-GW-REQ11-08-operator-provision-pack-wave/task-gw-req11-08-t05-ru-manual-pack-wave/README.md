# task-gw-req11-08-t05-ru-manual-pack-wave

## Task: docs — RU manual pack-wave (T05)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:31:41Z
- **Package:** pkg-000106
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-10-01T10:23:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`

## Purpose
RU manual Present + cross-link from life-sim load manual § provision. Scope #9 · AC-GW-REQ1108-05. Name ≠ create until P3.

## Code Facts
1. Operator RU pack-wave manual Absent.
2. life-sim-demo-node-load-manual-ru.md Present (provision section to cross-link).

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — life-sim-provision-pack-wave-manual-ru.md + load-manual cross-link

Historical gap (pre-P3):
RU pack-wave manual Absent.

## Acceptance / DoD
- [x] Manual Present at target path (AC-05)
- [x] Documents env, pack_id, wipe vs skip, smoke, wave/secrets locations, file SMS preconditions
- [x] Cross-link from load manual § provision
- [x] BULLRUN phases complete when closed

## Where to change
- `docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md` + load manual link (P3)

## Out of scope
Product implement beyond docs; invent OTP HTTP.
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
ls doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-provision-pack-wave-manual-ru.md
# after P3: rg -n 'pack.wave|wipe-fixture|LIFE_SIM_PACK' docs/runtime-docs/manuals/life-sim*.md | head -40
```
