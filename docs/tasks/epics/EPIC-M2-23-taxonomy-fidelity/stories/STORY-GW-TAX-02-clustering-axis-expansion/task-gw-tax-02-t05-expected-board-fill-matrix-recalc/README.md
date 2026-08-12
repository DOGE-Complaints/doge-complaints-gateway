# task-gw-tax-02-t05-expected-board-fill-matrix-recalc

## Meta
- **Story:** [STORY-GW-TAX-02](../STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000055
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Пересчёт `expected-board-fill-matrix` (SEED-02) под composite+новые оси; тесты плотности кластеров (v0_2).

## Code Facts
- Current matrix: 2 cards, `civic_domain` only — [`expected-board-fill-matrix.md`](../../../../EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md)
- Canvas v0_2 — `tests/sandbox/dogestonia_simulation_canvas_v0_2.json` (referenced in matrix)
- No `tests/test_gw_tax_02_*` yet — new test module per backlog T06

## Acceptance / DoD
- [x] Traces parent AC-4: demo board (v0_2) density expectations updated for composite+new axes
- [x] Scope trace: backlog T05 / expected-board-fill-matrix recalc
- [x] [`expected-board-fill-matrix.md`](../../../../EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md) recalculated under composite-primary
- [x] `tests/test_gw_tax_02_*` cluster density tests added (v0_2)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-02-t05.md`](./acceptance-verification-gw-tax-02-t05.md) signed (Date post live-run only)

## Where to change
- [`docs/tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md`](../../../../EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md)
- `tests/test_gw_tax_02_*.py` (new)

## Out of scope
- Runtime cluster engine changes (T01–T04)
- Full story gate (T06)
- GW-TAX-01; GPT-TAX-01

## Verification commands (post live-run only)
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration"
rg -n "composite|civic_domain" doge-complaints-gateway/docs/tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md
```
