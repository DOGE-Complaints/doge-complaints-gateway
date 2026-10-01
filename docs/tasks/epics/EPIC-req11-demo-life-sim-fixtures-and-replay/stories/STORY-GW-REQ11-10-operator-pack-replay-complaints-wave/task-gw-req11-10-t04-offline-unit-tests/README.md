# task-gw-req11-10-t04-offline-unit-tests

## Task: test — offline unit tests (T04)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** test
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:35:43Z
- **Package:** pkg-000108
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Decision Ref:** backlog STORY-GW-REQ11-10

## Purpose
Offline tests pack gate / wave resume / missing creds. AC-06.

## Code Facts
**As-of-Done (P3 2026-10-01T11:35:43Z):**
1. `tests/test_gw_req11_10_replay_pack_wave.py` — **8 passed**.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] Pack gate refuse covered
- [x] Wave checkpoint/resume covered
- [x] Missing-creds fail-closed covered
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/test_gw_req11_10_replay_pack_wave.py`

## Out of scope
Live full pack HTTP.

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_10_replay_pack_wave.py
```
