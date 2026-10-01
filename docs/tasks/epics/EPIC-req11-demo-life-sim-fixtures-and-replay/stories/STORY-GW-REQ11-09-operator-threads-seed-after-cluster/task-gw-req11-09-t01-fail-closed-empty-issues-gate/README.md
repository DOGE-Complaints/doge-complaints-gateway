# task-gw-req11-09-t01-fail-closed-empty-issues-gate

## Task: implement / tooling — fail-closed empty-issues gate (T01)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:52:44Z
- **Package:** pkg-000107
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-01T10:45:33Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`

## Purpose
Hard fail-closed gate: CLI **STOP** if `GET /node/issues` empty / no handoff `issue_id` after clustering. Document order: … → cluster → threads seed. Scope #2 · AC-GW-REQ1109-01.

## Code Facts
**As-of-Done (P3 2026-10-01T10:52:44Z):**
1. `life_sim_seed_threads_lib.require_nonempty_handoffs` + CLI exit **2** when empty.
2. Live local probe: `GATEWAY_URL=http://127.0.0.1:8000` → issues=[] → fail-closed exit 2 (no invent force-cluster).
3. Offline: `test_empty_issues_fail_closed` PASS.

### Historical (scaffold / pre-P3)
Operator empty-issues gate Absent.

## Gap
**As-of-Done:** closed — fail-closed empty issues Present.

## Acceptance / DoD
- [x] CLI STOP when issues empty / no handoff `issue_id` (AC-01)
- [x] Documented load order includes cluster → threads seed
- [x] No invent HTTP force-cluster
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_seed_threads_lib.py` · `life_sim_seed_threads.py`

## Out of scope
CLI Make entry (T02); actors/handoff seed call (T03); tests (T04); RU manual (T05); gate (T06).

## Verification commands
```bash
GATEWAY_URL=http://127.0.0.1:8000 .venv/bin/python tests/sandbox/life_sim_seed_threads.py --dry-run  # exit 2 if empty
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req11_09_seed_threads.py::test_empty_issues_fail_closed
```
