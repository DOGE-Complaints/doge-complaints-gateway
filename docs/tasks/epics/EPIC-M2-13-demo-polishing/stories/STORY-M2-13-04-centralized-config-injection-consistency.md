# STORY-M2-13-04: Centralized config injection consistency

## Meta
- Key: `STORY-M2-13-04`
- Parent Epic: [`../../EPIC-M2-13-demo-polishing.md`](../../EPIC-M2-13-demo-polishing.md)
- Type: Technical Story
- Status: Implemented (Waiting Acceptance/Commits)
- Stream: M2 Polishing
- Gap reference: `GAP-004`
- Skill declared: `python-pro`

## Story Goal
Выравнять использование централизованного `AppConfig`/feature flags по активным сервисам и DI-точкам, чтобы устранить архитектурный дрейф конфигурации.

## AC / DoD
- [x] Инъекция конфигурации через DI согласована между API dependencies, providers и service factory.
- [x] Добавлены тесты на консистентность config-driven поведения сервисов.
- [x] `GAP-004` закрыт через code+test evidence.

## Task Artifacts
- Task workspace: [`../../../task-m2-13-04-centralized-config-injection-consistency/README.md`](../../../task-m2-13-04-centralized-config-injection-consistency/README.md)
- Task specification: [`../../../task-m2-13-04-centralized-config-injection-consistency/task-m2-13-04-centralized-config-injection-consistency.md`](../../../task-m2-13-04-centralized-config-injection-consistency/task-m2-13-04-centralized-config-injection-consistency.md)
- Phase log: [`../../../task-m2-13-04-centralized-config-injection-consistency/BULLRUN-PHASE-LOG.md`](../../../task-m2-13-04-centralized-config-injection-consistency/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-13-04-centralized-config-injection-consistency/acceptance-verification-STORY-M2-13-04.md`](../../../task-m2-13-04-centralized-config-injection-consistency/acceptance-verification-STORY-M2-13-04.md)
