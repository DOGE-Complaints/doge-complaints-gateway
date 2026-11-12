# task-gw-req11-05-t06-offline-unit-tests

## Task: test — offline unit tests (T06)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** test
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:15:05Z
- **Package:** pkg-000104
- **Skill declared:** python-pro
- **Depends on:** T01–T02 helpers extractable
- **Scaffolded:** 2026-09-29T18:09:49Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md`

## Purpose
Offline/unit: email/phone derivation, password strength, secrets path hygiene. AC-GW-REQ1105-06 offline. Live provision via ops/`--limit` smoke (gate/T03).

## Code Facts
1. Offline tests Present: `tests/test_gw_req11_05_provision_fixture_users.py` — **10 passed**.
2. Covers email/phone, password strength, secrets hygiene, OTP parse, fixture bearer mock, pool flag.

## Gap
**As-of-Done (P3):** closed.

## Acceptance / DoD
- [x] Unit tests for email/phone derivation + password ≥24 + secrets path hygiene (AC-06 offline)
- [x] No secrets committed by tests
- [x] BULLRUN phases complete when closed

## Where to change
- New/extended pytest under `tests/` (P3); import helpers from provision module

## Out of scope
Live Telnyx; invent OTP HTTP; full N=200 as unit test.
- Overlay bans:
  - Stay `dev`.
  - 200 users 1:1; CSPRNG ≥24; gitignored secrets; supersede pool M=20; rate-limit pacing; K1 no SPA resident login.
  - OTP via Identity `SMS_PROVIDER=file` disk outbox — **no invent** `GET /dev/last-otp`.
  - Pointer pkg-000104; do not mutate pkg-000100…103.
  - No invent OTP HTTP; no pilot Telnyx; no regenerate fixtures; never commit secrets.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
# after P3:
# cd doge-complaints-gateway && python -m pytest tests/ -k life_sim_provision -q --tb=short
```
