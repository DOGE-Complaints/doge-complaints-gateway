# task-gw-req11-12-t05-offline-tests-schema-diversity-roundtrip

## Task: test — offline schema / diversity / round-trip / REQ11-10 smoke (T05)

## Meta
- **Story:** [STORY-GW-REQ11-12](../STORY-GW-REQ11-12-life-sim-stories-rich-generator-and-adapter.md)
- **Type:** test
- **Status:** 🟢 Done
- **Package:** pkg-000110
- **Skill declared:** python-pro
- **Depends on:** soft T01–T04
- **Scaffolded:** 2026-10-02T09:02:38Z
- **Decision Ref:** backlog STORY-GW-REQ11-12

## Purpose
Offline tests: schema presence (v2 keys); diversity gates; adapter round-trip → valid stash narrative shape; smoke that REQ11-10 pack reader still accepts pack. Scope #6 · **AC-GW-REQ1112-05**.

## Code Facts
1. REQ11-10 pack-wave Present — `life_sim_replay_pack_wave` / Make.
2. Intake Narrative shape — `src/core/intake/contracts.py`.

## Gap
No offline suite for v2 schema/diversity/adapter round-trip yet (scaffold).

## Acceptance / DoD
- [x] Schema v2 keys asserted
- [x] Diversity gate asserted
- [x] Adapter round-trip → narrative shape
- [x] REQ11-10 pack-read smoke still accepts pack
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-12-t05.md` signed (P3)

## Where to change
- New/extend `tests/test_gw_req11_12_*.py` (P3 lock path)

## Out of scope
Live full fill; invent HTTP; ops docs (T06).

## Verification commands
```bash
# P3 example
cd doge-complaints-gateway && python -m pytest tests/test_gw_req11_12*.py -q
```
