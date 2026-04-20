# STORY-M2-09-03: Structured logging and tracing

## Meta
- Key: `STORY-M2-09-03`
- Parent Epic: [`../../EPIC-M2-09-security-config-observability.md`](../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Todo
- Stream: M2 Security/Ops
- Skill declared: `python-pro`

## Story Goal
Структурированные логи с `trace_id` (и secret-safe политика: не логировать тела с PII по умолчанию).

## AC / DoD
- [ ] Единая точка настройки логирования для API/handlers.
- [ ] `trace_id` в контексте запроса и в лог-записях.
- [ ] Тесты или контрактные проверки на наличие trace в успешном/ошибочном пути.

## Task Artifacts
- Task workspace: [`../../../task-m2-09-03-structured-logging-and-tracing/README.md`](../../../task-m2-09-03-structured-logging-and-tracing/README.md)
- Task specification: [`../../../task-m2-09-03-structured-logging-and-tracing/task-m2-09-03-structured-logging-and-tracing.md`](../../../task-m2-09-03-structured-logging-and-tracing/task-m2-09-03-structured-logging-and-tracing.md)
- Phase log: [`../../../task-m2-09-03-structured-logging-and-tracing/BULLRUN-PHASE-LOG.md`](../../../task-m2-09-03-structured-logging-and-tracing/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-09-03-structured-logging-and-tracing/acceptance-verification-STORY-M2-09-03.md`](../../../task-m2-09-03-structured-logging-and-tracing/acceptance-verification-STORY-M2-09-03.md)
