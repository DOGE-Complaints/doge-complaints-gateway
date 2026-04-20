# STORY-M2-01-02: DI Providers and Service Factory Baseline

## Meta
- Key: `STORY-M2-01-02`
- Parent Epic: [`EPIC-M2-01-core-foundation-and-governance.md`](../../EPIC-M2-01-core-foundation-and-governance.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Foundation

## Story Goal
Ввести единый DI-контур (providers + service factory), чтобы исключить ad-hoc инициализацию сервисов.

## Scope
- контракт `ServiceFactory`;
- providers для ключевых сервисов baseline;
- wiring в API dependencies;
- тесты резолва зависимостей.

## AC / DoD
- [ ] Описан контракт `ServiceFactory`.
- [ ] Реализованы DI providers для базовых сервисов.
- [ ] API-слой получает зависимости только через DI-bridge.
- [ ] Нет ad-hoc создания сервисов в route handlers.
- [ ] Добавлены unit/integration тесты на DI graph.

## Task Artifacts
- Task workspace: [`../../../task-m2-01-02-di-providers-and-service-factory-baseline/README.md`](../../../task-m2-01-02-di-providers-and-service-factory-baseline/README.md)
- Phase log: [`../../../task-m2-01-02-di-providers-and-service-factory-baseline/BULLRUN-PHASE-LOG.md`](../../../task-m2-01-02-di-providers-and-service-factory-baseline/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-01-02-di-providers-and-service-factory-baseline/acceptance-verification-STORY-M2-01-02.md`](../../../task-m2-01-02-di-providers-and-service-factory-baseline/acceptance-verification-STORY-M2-01-02.md)
