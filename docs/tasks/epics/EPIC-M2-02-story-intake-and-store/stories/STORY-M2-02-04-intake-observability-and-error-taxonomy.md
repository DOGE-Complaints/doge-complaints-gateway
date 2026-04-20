# STORY-M2-02-04: Intake Observability and Error Taxonomy

## Meta
- Key: `STORY-M2-02-04`
- Parent Epic: [`EPIC-M2-02-story-intake-and-store.md`](../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Intake
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Сделать intake-поток операционно наблюдаемым: метрики, trace correlation и унифицированная taxonomy ошибок.

## Scope
- structured logging для intake boundary;
- error taxonomy dictionary (validation/domain/infrastructure/internal);
- basic intake telemetry counters;
- tests для error classification и log payload consistency.

## AC / DoD
- [ ] Определена и реализована taxonomy intake ошибок.
- [ ] Логи intake содержат `trace_id` и тип ошибки.
- [ ] Базовые intake метрики определены и обновляются.
- [ ] Ошибки классифицируются единообразно во всех intake handlers baseline.
- [ ] Тесты покрывают классификацию и observability payload.

## Task Artifacts
- Task workspace: [`../../../task-m2-02-04-intake-observability-and-error-taxonomy/README.md`](../../../task-m2-02-04-intake-observability-and-error-taxonomy/README.md)
- Task specification: [`../../../task-m2-02-04-intake-observability-and-error-taxonomy/task-m2-02-04-intake-observability-and-error-taxonomy.md`](../../../task-m2-02-04-intake-observability-and-error-taxonomy/task-m2-02-04-intake-observability-and-error-taxonomy.md)
- Phase log: [`../../../task-m2-02-04-intake-observability-and-error-taxonomy/BULLRUN-PHASE-LOG.md`](../../../task-m2-02-04-intake-observability-and-error-taxonomy/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-02-04-intake-observability-and-error-taxonomy/acceptance-verification-STORY-M2-02-04.md`](../../../task-m2-02-04-intake-observability-and-error-taxonomy/acceptance-verification-STORY-M2-02-04.md)
