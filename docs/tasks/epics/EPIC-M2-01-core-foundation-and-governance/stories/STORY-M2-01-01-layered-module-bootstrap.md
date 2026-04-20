# STORY-M2-01-01: Layered Module Bootstrap

## Meta
- Key: `STORY-M2-01-01`
- Parent Epic: [`EPIC-M2-01-core-foundation-and-governance.md`](../../EPIC-M2-01-core-foundation-and-governance.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Foundation

## Story Goal
Собрать минимальный каркас слоёв `API -> Application -> Domain -> Infrastructure` без бизнес-логики Core.

## Scope
- структура модулей/пакетов по слоям;
- правила зависимостей между слоями;
- стартовый bootstrap приложения;
- базовые smoke-тесты загрузки модулей.

## AC / DoD
- [ ] Создан и задокументирован слой `API`.
- [ ] Создан и задокументирован слой `Application`.
- [ ] Создан и задокументирован слой `Domain`.
- [ ] Создан и задокументирован слой `Infrastructure`.
- [ ] Определены guardrails зависимостей (нет обхода Domain/Application).
- [ ] Добавлены smoke-тесты bootstrapping для каркаса.

## Task Artifacts
- Task workspace: [`../../../task-m2-01-01-layered-module-bootstrap/README.md`](../../../task-m2-01-01-layered-module-bootstrap/README.md)
- Phase log: [`../../../task-m2-01-01-layered-module-bootstrap/BULLRUN-PHASE-LOG.md`](../../../task-m2-01-01-layered-module-bootstrap/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-01-01-layered-module-bootstrap/acceptance-verification-STORY-M2-01-01.md`](../../../task-m2-01-01-layered-module-bootstrap/acceptance-verification-STORY-M2-01-01.md)
