# DB Task Batch Plan (Supabase-native Wave)

Источник gap-ов: `docs/analysis/supabase-db-layer-audit-and-target-state.md`, `docs/analysis/db-gap-register.md`, `.cursor/plans/supabase_native_gap_wave_70b16d80.plan.md`.

## Порядок батчей (обязательный)

1. Batch 1 (foundation): `TASK-DB-CONFIG-SUPABASE-02` -> `TASK-DB-SUPABASE-REPOS-02`
2. Batch 2 (operability/security): `TASK-DB-READINESS-SUPABASE-02` -> `TASK-DB-RLS-VALIDATION-02`
3. Batch 3 (unit coverage): `TASK-TEST-UNIT-API-APP-01` -> `TASK-TEST-UNIT-INFRA-CONFIG-01` -> `TASK-TEST-UNIT-DOMAIN-FLOWS-01`
4. Batch 4 (live DB integration): `TASK-TEST-INTEGRATION-SUPABASE-LIVE-01`
5. Batch 5 (formal gates): `TASK-TEST-COVERAGE-GATE-01`

## Verification gates для каждого батча

- backend-switch контракт и fail-fast env-проверки подтверждены;
- supabase-native repositories protocol-совместимы и используются при `DB_BACKEND=supabase`;
- readiness отражает connectivity/schema/policy статус без false-positive;
- RLS/policy проверки пройдены на live Supabase bucket;
- unit buckets (api+app, infra+config, domain flows) обязательны;
- live integration bucket пройден (`tests/integration/supabase`);
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
3. обновить `docs/tasks/db-gap-traceability-matrix.md`;
4. обновить `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`.
