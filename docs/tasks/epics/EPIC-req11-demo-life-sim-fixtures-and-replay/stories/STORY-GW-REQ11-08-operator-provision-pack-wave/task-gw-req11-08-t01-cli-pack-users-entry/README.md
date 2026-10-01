# task-gw-req11-08-t01-cli-pack-users-entry

## Task: implement / tooling — CLI + pack users entry (T01)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:31:41Z
- **Package:** pkg-000106
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-01T10:23:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`

## Purpose
CLI entry + Make/shell: read pack `users.json` via `LIFE_SIM_PACK_DIR`; refactor/reuse Present provision into clean entry; never write provision status into fixture JSON. Scope #1,#3 · AC-GW-REQ1108-01. Name ≠ create until P3.

## Code Facts
**As-of-Done (P3 2026-10-01T10:31:41Z):**
1. Pack-wave CLI Present: `tests/sandbox/life_sim_provision_pack_wave.py` + `make life-sim-provision-pack-wave`.
2. Reads pack `users.json` via `LIFE_SIM_PACK_DIR` / `--pack-dir`; never writes provision status into fixture (mtime guard).
3. Reuses REQ11-05 `life_sim_provision_users.provision_one` / lib.
4. Flat `dogestonia_life_sim_users_v0_1.json` still Absent as SSOT (pack is source).

### Historical (scaffold / pre-P3)
1. Present reuse only: `life_sim_provision_users.py`, `life_sim_provision_lib.py`, `make life-sim-provision-users`.
2. Pack users Present; pack-wave CLI / clean layout **Absent**.

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — CLI pack users + Make entry Present; never writes users.json

Historical gap (pre-P3):
Pack-wave CLI entry + fixture-status isolation not Present.

## Acceptance / DoD
- [x] CLI/Make reads pack `users.json` (AC-01)
- [x] Never writes provision statuses into fixture `users.json`
- [x] Reuse/refactor Present 05 tooling into one clear entry (layout lock P3)
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_provision_pack_wave.py` (or refactor of provision_users) + Make (P3)

## Out of scope
Shared config (T02); wave-state (T03); wipe/skip provision (T04); RU manual (T05); tests (T06); gate (T07).
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
ls doge-complaints-gateway/tests/sandbox/life_sim_packs/*/users.json | head
# after P3: rg -n 'LIFE_SIM_PACK_DIR|users.json' tests/sandbox/life_sim_provision*.py | head -40
```
