# task-gw-req11-09-t02-cli-make-thin-wrapper

## Task: implement / tooling — CLI + Make thin wrapper (T02)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:52:44Z
- **Package:** pkg-000107
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-01T10:45:33Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`

## Purpose
Operator CLI + Make entry: `life_sim_seed_threads.py` + `make life-sim-seed-threads`. Smoke `--limit` / dry-run hooks. Scope #3,#8 · AC-02 · AC-04 (entry).

## Code Facts
**As-of-Done (P3 2026-10-01T10:52:44Z):**
1. Present: `tests/sandbox/life_sim_seed_threads.py` + `Makefile` target `life-sim-seed-threads`.
2. Thin wrapper calls Present `seed_representative_issues` (live path); dry-run skips seed HTTP.
3. `--limit` / `LIFE_SIM_SEED_THREADS_DRY_RUN=1` / `--gateway-url` / `--threads-url`.

### Historical (scaffold / pre-P3)
CLI/Make Absent; B-THR-CLI open.

## Gap
**As-of-Done:** closed — CLI + Make entry Present.

## Acceptance / DoD
- [x] CLI/Make entry Present (`life-sim-seed-threads`) (AC-04 entry)
- [x] Thin wrapper → Present `seed_representative_issues` (AC-02)
- [x] Smoke `--limit N` / dry-run where feasible
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_seed_threads.py` + `Makefile`

## Out of scope
Empty-issues gate internals (T01); secrets/actors/handoff body (T03); offline tests (T04); RU manual (T05).

## Verification commands
```bash
ls doge-complaints-gateway/tests/sandbox/life_sim_seed_threads.py
rg -n 'life-sim-seed-threads' doge-complaints-gateway/Makefile
```
