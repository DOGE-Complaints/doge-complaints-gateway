# task-gw-seed-02-t04

## Meta
- **Story:** [STORY-GW-SEED-02](../STORY-GW-SEED-02-dataset-expansion-for-clustering.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000037
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Зафиксировать ожидаемое число issue-карточек по группам (для приёмки SEED-03): issue count per `scenario_group` / cluster theme.

## Code Facts
- Board read API — [`handlers.py`](../../../../../../../src/core/api/handlers.py) `GET /tallinn/issues`
- SEED-03 dependency — [`STORY-GW-SEED-03`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md)
- T03 verify artifact — [`../task-gw-seed-02-t03-local-clustering-and-promotion-verify/cluster-verify-summary.md`](../task-gw-seed-02-t03-local-clustering-and-promotion-verify/cluster-verify-summary.md)
- Runbook — [`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md)

## Acceptance / DoD
- Traces parent AC: зафиксировано ожидаемое наполнение доски
- Artifact [`expected-board-fill-matrix.md`](./expected-board-fill-matrix.md): expected issue count per `scenario_group` and per cluster theme; ties to T01 matrix + T03 actuals
- Minimal runbook cross-ref: v0_2 canvas path in [`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) (one line or § pointer)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifact: `expected-board-fill-matrix.md`
- [`seed-demo-data-runbook-ru.md`](../../../../../../runtime-docs/manuals/seed-demo-data-runbook-ru.md) — v0_2 pointer only

## Out of scope
- Full E2E hosted runbook (SEED-03)
- `src/core/` changes
- Changing v0_1 canvas

## Verification commands
```bash
test -f doge-complaints-gateway/docs/tasks/epics/EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/task-gw-seed-02-t04-expected-board-fill-matrix/expected-board-fill-matrix.md
rg -n "v0_2" doge-complaints-gateway/docs/runtime-docs/manuals/seed-demo-data-runbook-ru.md
```
