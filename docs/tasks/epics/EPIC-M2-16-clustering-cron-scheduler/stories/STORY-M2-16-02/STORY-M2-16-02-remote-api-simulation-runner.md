# STORY-M2-16-02: Remote API simulation runner and dataset readiness

## Meta
- Key: `STORY-M2-16-02`
- Parent Epic: [`../../../EPIC-M2-16-clustering-cron-scheduler.md`](../../../EPIC-M2-16-clustering-cron-scheduler.md)
- Type: Technical Story
- Status: Implemented (Awaiting Commit)
- Stream: M2 Remote Simulation
- Requirement reference: [`remote-api-simulation-gap-2026-05-07.md`](../../../../../analysis/remote-api-simulation-gap-2026-05-07.md)
- Skill declared: `python-pro`

## Story Goal
Закрыть GAP-SIM-01..04: добавить remote simulation runner, отдельный test env-шаблон, one-command запуск и покрытие `location_query` для geo-сценариев в simulation canvas.

## AC / DoD
- [x] AC-SIM-01: есть `tests/simulation_runner.py` с запуском по `.env.test`, отправкой `POST /intake/stories`, итоговым summary и exit code policy.
- [x] AC-SIM-02: создан и задокументирован `.env.test.example` для remote simulation.
- [x] AC-SIM-03: добавлен one-command запуск симуляции (`make simulate` или shell target) и он документирован.
- [x] AC-SIM-04: сценарии с гео в canvas содержат `location_query` (или эквивалентный поддерживаемый источник), чтобы geo-линза не падала в `unknown` из-за пропуска поля.

## Nested tasks

| Order | Slug | Task folder |
|-------|------|-------------|
| 1 | primary | `task-m2-16-02-remote-simulation-primary` |
| 2 | T01 | `task-m2-16-02-t01-simulation-runner` |
| 3 | T02 | `task-m2-16-02-t02-env-test-template` |
| 4 | T03 | `task-m2-16-02-t03-single-command-launch` |
| 5 | T04 | `task-m2-16-02-t04-geo-location-query-coverage` |

## Task Artifacts
- primary: [`./task-m2-16-02-remote-simulation-primary/README.md`](./task-m2-16-02-remote-simulation-primary/README.md)
- T01: [`./task-m2-16-02-t01-simulation-runner/README.md`](./task-m2-16-02-t01-simulation-runner/README.md)
- T02: [`./task-m2-16-02-t02-env-test-template/README.md`](./task-m2-16-02-t02-env-test-template/README.md)
- T03: [`./task-m2-16-02-t03-single-command-launch/README.md`](./task-m2-16-02-t03-single-command-launch/README.md)
- T04: [`./task-m2-16-02-t04-geo-location-query-coverage/README.md`](./task-m2-16-02-t04-geo-location-query-coverage/README.md)
- Acceptance (story): [`./task-m2-16-02-remote-simulation-primary/acceptance-verification-STORY-M2-16-02.md`](./task-m2-16-02-remote-simulation-primary/acceptance-verification-STORY-M2-16-02.md)
- Phase log (story): [`./task-m2-16-02-remote-simulation-primary/BULLRUN-PHASE-LOG.md`](./task-m2-16-02-remote-simulation-primary/BULLRUN-PHASE-LOG.md)
