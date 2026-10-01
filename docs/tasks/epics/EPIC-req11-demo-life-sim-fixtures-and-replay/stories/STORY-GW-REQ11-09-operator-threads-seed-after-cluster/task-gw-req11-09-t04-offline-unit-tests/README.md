# task-gw-req11-09-t04-offline-unit-tests

## Task: test — offline unit tests (T04)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** test
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:52:44Z
- **Package:** pkg-000107
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-01T10:45:33Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`

## Purpose
Offline units: empty-issues refuse; handoff parse; actor join hygiene. Scope #8 · AC-06 offline.

## Code Facts
**As-of-Done (P3 2026-10-01T10:52:44Z):**
1. `tests/test_gw_req11_09_seed_threads.py` — **9 passed**.
2. Covers empty-issues fail-closed, handoff density parse, service-token refuse, Make target Present, closed_http_seed import.

### Historical (scaffold / pre-P3)
Gateway offline tests for threads-seed CLI Absent.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] Offline test: empty-issues refuse (AC-06)
- [x] Offline test: handoff parse (`issue_id` + `density`)
- [x] Offline test: actor join hygiene / service-token refuse
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/test_gw_req11_09_seed_threads.py`

## Out of scope
Live cluster/seed full (leftover if issues empty).

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_09_seed_threads.py
```
