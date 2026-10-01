# task-gw-req11-08-t03-wave-state-checkpoint-resume

## Task: implement / tooling — wave-state checkpoint + resume (T03)

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
Wave-state JSON separate from fixture; per fixture_user_id pending|created|verified|failed; checkpoint; resume skips verified. Scope #4 · AC-GW-REQ1108-03. Name ≠ create until P3.

## Code Facts
**As-of-Done (P3 2026-10-01T10:31:41Z):**
1. Wave store Present: `tests/sandbox/life_sim_wave_store.py` → `pack/waves/<wave_id>/state.json`.
2. Statuses pending|created|verified|failed; checkpoint; resume skips `verified`.
3. Never writes status into fixture `users.json`.

### Historical (scaffold / pre-P3)
1. Pack-wave state JSON **Absent**.
2. Must not write status into users.json (constraint already stated).

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — life_sim_wave_store.py wave JSON; resume skips verified

Historical gap (pre-P3):
Wave-state store Absent.

## Acceptance / DoD
- [x] Wave JSON per wave under pack (path lock P3) (AC-03)
- [x] Checkpoint after each success/fail step
- [x] Resume skips entries already `verified`
- [x] BULLRUN phases complete when closed

## Where to change
- `life_sim_packs/<pack_id>/waves/<wave_id>/state.json` (P3)

## Out of scope
Config (T02); wipe/provision (T04); mutate fixture JSON.
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
# after P3: rg -n 'verified|checkpoint|wave' tests/sandbox/life_sim_*wave* | head -40
```
