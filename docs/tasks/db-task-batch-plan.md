# DB Task Batch Plan (Supabase)

Источник gap-ов: `docs/analysis/supabase-db-layer-audit-and-target-state.md`, `docs/analysis/db-gap-register.md`.

## Порядок батчей (обязательный)

1. `TASK-DB-SCHEMA-01`
2. `TASK-DB-CONFIG-01`
3. `TASK-DB-STORIES-01`
4. `TASK-DB-STORY-EMBEDDINGS-01`
5. `TASK-DB-SPA-PROJECTIONS-01`
6. `TASK-DB-SPA-EMBEDDINGS-01`
7. `TASK-DB-RLS-01`
8. `TASK-DB-E2E-01`

## Verification gates для каждого батча

- миграции применяются на clean базе;
- protocol-совместимость репозиториев подтверждена тестами;
- linkage целостность проверена (`story_id -> issue_id -> projection/evidence`);
- embeddings слой готов к поиску/кластеризации;
- RLS/policy проверки пройдены (для соответствующих батчей);
- есть `run-summary-*` запись в `Run Reports Registry`.

## Decision Brief (PM/CTO)

Перед каждым батчем фиксируется:

- `Demo Readiness Impact`
- `Foundation Impact`
- `Deferred Scope`
- `No-hacks check`

## Правило отчетности

После каждого батча:

1. создать `docs/tasks/run-reports/run-summary-YYYYMMDD-HHMM.md`;
2. добавить строку в `docs/tasks/bullrun-launch-index.md` (`Run Reports Registry`);
3. обновить `docs/tasks/db-gap-traceability-matrix.md`.
