# Intake/Projection Task Batch Plan (Demo Readiness + Clean Foundation)

## Контекст

План определяет порядок `TASK_BATCH` для закрытия `GAP-IP-001..005` так, чтобы:

1. быстро восстановить demo-critical API flow;
2. не вводить временные архитектурные костыли;
3. сохранить расширяемость для post-demo.

Источник расхождений: `docs/runtime-docs/issue-intake-and-spa-projection-audit.md`.

## Порядок батчей (обязательный)

1. `TASK-INTAKE-HTTP-01`
2. `TASK-STORY-TO-PROJECTION-01`
3. `TASK-SPA-PROJECTION-DATA-01`
4. `TASK-ISSUE-CREATE-HTTP-01`
5. `TASK-E2E-CONTRACT-01`

## Decision Brief (PM/CTO) — перед каждым батчем

Обязательный блок согласования:

- `Demo Readiness Impact`: какой demo-сценарий становится рабочим после батча;
- `Foundation Impact`: какие контракты/слои становятся стабильными;
- `Deferred Scope`: что сознательно переносится, чтобы не размывать батч;
- `No-hacks check`:
  - нет временного дублирования мапперов;
  - нет endpoint без стабильного контракта;
  - нет mock-only веток в production runtime;
  - нет расхождения между docs и фактическим кодом.

## Гейты верификации по батчам

### Batch 1 — Intake HTTP
- HTTP tests: `POST /intake/stories` (200/400).
- Envelope consistency check (trace + error taxonomy).

### Batch 2 — Story->Projection bridge
- Unit tests для bridge-модуля.
- Инварианты обязательных полей `ProjectionInput`.

### Batch 3 — Projection data policy
- Contract tests для `status/type/labels/i18n`.
- Validation tests на запрет placeholder-значений.

### Batch 4 — Issue create HTTP
- HTTP tests create issue endpoint.
- Orchestration tests (без inline бизнес-логики в handler).

### Batch 5 — E2E contract
- Сквозные tests: intake/create -> SPA payload.
- Полный regression прогон существующих smoke/projection suite.

## Acceptance gates (PM/CTO)

- `PM gate`: результат демонстрируем, сценарий понятен стейкхолдерам.
- `CTO gate`: решение не создает одноразовый слой и сохраняет единый source of truth.

## Run-report дисциплина

После каждого `TASK_BATCH`:

1. создать `docs/tasks/run-reports/run-summary-YYYYMMDD-HHMM.md`;
2. добавить строку в `Run Reports Registry` в `bullrun-launch-index.md`;
3. обновить `intake-projection-gap-traceability-matrix.md`.
