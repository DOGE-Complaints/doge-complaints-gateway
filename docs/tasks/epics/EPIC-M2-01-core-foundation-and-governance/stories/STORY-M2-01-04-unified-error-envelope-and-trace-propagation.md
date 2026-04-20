# STORY-M2-01-04: Unified Error Envelope and Trace Propagation

## Meta
- Key: `STORY-M2-01-04`
- Parent Epic: [`EPIC-M2-01-core-foundation-and-governance.md`](../../EPIC-M2-01-core-foundation-and-governance.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Foundation

## Story Goal
Стандартизировать формат ошибок и трассировку запросов (`trace_id`) на всей границе API.

## Scope
- единый `ErrorEnvelope`;
- генерация/проброс `trace_id`;
- унификация error mapping;
- contract tests для error shape.

## AC / DoD
- [ ] Все API-ошибки возвращаются в едином `ErrorEnvelope`.
- [ ] `trace_id` присутствует в каждом ответе и логах.
- [ ] Ошибки валидации/доменные/инфраструктурные маппятся предсказуемо.
- [ ] Добавлены contract tests для error shape и trace propagation.
- [ ] Документация API-ошибок обновлена.

## Task Artifacts
- Task workspace: [`../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/README.md`](../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/README.md)
- Phase log: [`../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/BULLRUN-PHASE-LOG.md`](../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/acceptance-verification-STORY-M2-01-04.md`](../../../task-m2-01-04-unified-error-envelope-and-trace-propagation/acceptance-verification-STORY-M2-01-04.md)
