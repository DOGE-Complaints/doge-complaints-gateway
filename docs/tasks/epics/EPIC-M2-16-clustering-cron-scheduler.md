# EPIC-M2-16: Clustering Cron Scheduler (Requirement 28 + Remote Simulation wave)

## Epic Meta
- Status: In Progress
- Priority: High
- Owner: TBD
- Target: TBD

## Business Goal
Обеспечить устойчивую оркестрацию intake/clustering с поддержкой remote API simulation-прогонов для массовой валидации story intake через реальный HTTP endpoint.

## Scope
### In Scope
- Requirement 28 wave: decoupled clustering cron orchestration.
- Remote API simulation wave: `simulation_runner`, test env-template, one-command launch, geo-ready canvas coverage.

### Out of Scope
- Изменение продуктового API-контракта `POST /intake/stories`.
- Переработка production-логики supabase beyond simulation preparation docs/tools.

## Source Requirements
- [`28-clustering-cron-scheduler.md`](../../requirements/28-clustering-cron-scheduler.md)
- [`remote-api-simulation-gap-2026-05-07.md`](../../analysis/remote-api-simulation-gap-2026-05-07.md)

## Stories

| Key | Story | Type | Status | Scope |
|-----|-------|------|--------|-------|
| M2-16-02 | [Remote API simulation runner and dataset readiness](./EPIC-M2-16-clustering-cron-scheduler/stories/STORY-M2-16-02/STORY-M2-16-02-remote-api-simulation-runner.md) | implement | Todo | GAP-SIM-01..04 closure for remote simulation test-pipeline wave. |
