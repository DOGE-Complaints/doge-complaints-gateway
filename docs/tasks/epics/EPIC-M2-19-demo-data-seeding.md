# EPIC-M2-19: Demo Data Seeding (Hosted)

## Epic Meta
- Status: Done (Awaiting Commits)
- Priority: High
- Owner: TBD
- Target: Sprint 6
- **Materialized:** 2026-06-21 (P1 backlog_story STORY-GW-SEED-01)

## Business Goal
Наполнить hosted-демо (Railway + Supabase) тестовыми историями через существующий simulation loader так, чтобы сработала cron-кластеризация и дашборд показал issue-карточки; воспроизводимый ops-контур и мануал.

## Problem Statement
После закрытия issues-read-contract (RC-01→06) на hosted остаётся минимальный test-seed (1 карточка). Полное демо-наполнение требует проверки готовности таргета (RC-04 columnar, cron), загрузки историй и верификации записей в `stories`.

## Scope
### In Scope
- STORY-GW-SEED-01: loader + hosted readiness (ops/verify)
- STORY-GW-SEED-02: расширение датасета для кластеризации ≥8/кластер (pipeline pkg-000037)
- STORY-GW-SEED-03: E2E seed-runbook + проверка наполнения доски (backlog Done)
- STORY-GW-SEED-04: runner auth bootstrap email+password → Supabase token (pipeline pkg-000051)

### Out of Scope
- Понижение `CLUSTER_MIN_SIZE`
- Новый ручной триггер кластеризации (код)
- Post-demo tokenization / notifications (M2-11, M2-12)

## Stakeholders
- Product Owner
- Backend / ops
- QA

## Dependencies
- RC-04 columnar-миграции применены на hosted Supabase
- Gateway deployed (Railway) с `DB_BACKEND=supabase`
- [`tests/simulation_runner.py`](../../tests/simulation_runner.py) + canvas v0_1

## Success Metrics
- `GET /ready` → `db_ready: true` на hosted до загрузки
- 130 историй `sim:*` в `stories` после полного прогона
- Доска показывает issue-карточки после cron-кластеризации (SEED-03)
- Hosted re-seed без ручного user-токена после SEED-04 (ops)

## Epic Acceptance Criteria
- SEED-01..04 story gates PASS
- [`seed-demo-data-runbook-ru.md`](../runtime-docs/manuals/seed-demo-data-runbook-ru.md) актуален и воспроизводим

## Risks and Mitigation
- Риск: columnar-миграции не применены на hosted → `/ready` красный.  
  Mitigation: T01 readiness + apply `20260619_1200/1210/1220`.
- Риск: cron выключен → кластеры не формируются.  
  Mitigation: `CLUSTER_CRON_ENABLED=true` в T01.

## Definition of Done
- Hosted demo seed pipeline documented and verified
- Board populated with meaningful issue cards (SEED-03)
- Runner auto-auth via email+password in `.env.test` (SEED-04)

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-SEED-01 | [Loader + hosted readiness](./EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-01-loader-and-hosted-readiness/STORY-GW-SEED-01-loader-and-hosted-readiness.md) | Done (Awaiting Commits) |
| STORY-GW-SEED-02 | [Dataset expansion for clustering (≥8/cluster)](./EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-02-dataset-expansion-for-clustering/STORY-GW-SEED-02-dataset-expansion-for-clustering.md) | Done (Awaiting Commits) |
| STORY-GW-SEED-03 | [E2E seed-runbook + board fill verification](../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) | Done (Awaiting Commits) |
| STORY-GW-SEED-04 | [Runner auth bootstrap (email+password → Supabase token)](./EPIC-M2-19-demo-data-seeding/stories/STORY-GW-SEED-04-runner-auth-bootstrap-email-password/STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) | Done (Awaiting Commits) |

## Decision Ref
- [`interview-seed-demo-data-2026-06-20.md`](../analysis/interview-seed-demo-data-2026-06-20.md) — D-SEED-1..4
- [`backlog-stories/demo-data-seeding/STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md`](./backlog-stories/demo-data-seeding/STORY-GW-SEED-04-runner-auth-bootstrap-email-password.md) — D-SEED04-1..3 (2026-07-11)
- [`backlog-stories/demo-data-seeding/INDEX.md`](./backlog-stories/demo-data-seeding/INDEX.md)
