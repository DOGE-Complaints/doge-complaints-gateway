# task-gw-req11-08-t06-offline-unit-tests

## Task: test — offline unit tests (T06)

## Meta
- **Story:** [STORY-GW-REQ11-08](../STORY-GW-REQ11-08-operator-provision-pack-wave.md)
- **Type:** test
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:31:41Z
- **Package:** pkg-000106
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Scaffolded:** 2026-10-01T10:23:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-08-operator-provision-pack-wave.md`

## Purpose
Offline units: config fail-closed, wave checkpoint/resume, email domain `@dogestonia.me`. Scope #8 · AC-GW-REQ1108-06 offline. Name ≠ create until P3.

## Code Facts
1. No `test_gw_req11_08_*` yet.
2. REQ11-05 offline tests Present as pattern.

## Gap
**As-of-Done (P3 2026-10-01T10:31:41Z):** closed — tests/test_gw_req11_08_provision_pack_wave.py 6 passed

Historical gap (pre-P3):
Offline pack-wave tests Absent.

## Acceptance / DoD
- [x] Offline tests cover config fail-closed + wave resume + email domain (AC-06)
- [x] pytest green for offline suite
- [x] Assert no invent last-otp HTTP paths
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/test_gw_req11_08_*.py` (P3)

## Out of scope
Live full-200 as Pass requirement; gate file (T07).
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
# after P3: cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_08_*.py
```
