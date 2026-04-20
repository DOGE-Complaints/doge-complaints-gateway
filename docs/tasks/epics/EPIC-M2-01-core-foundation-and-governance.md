# EPIC-M2-01: Core Foundation and Governance

## Epic Meta
- Status: In Progress
- Priority: Critical
- Owner: TBD
- Target: Sprint 1

## Business Goal
Создать архитектурный фундамент Module 2, который исключает legacy coupling и поддерживает масштабирование до pilot.

## Problem Statement
Без единых правил слоистой архитектуры, DI и governance команда быстро придет к фрагментации решений и росту техдолга.

## Scope
### In Scope
- базовый модульный каркас (API/Application/Domain/Infrastructure);
- DI providers + service factory;
- единый error envelope и request tracing;
- config governance и feature flags;
- ADR process и decision log.

### Out of Scope
- бизнес-функциональность story/cluster/issue;
- blockchain runtime.

## Stakeholders
- Product Lead
- CTO/Architecture
- Backend team
- QA lead

## Dependencies
- Solution architecture docs approved
- Epic index approved

## Success Metrics
- 100% новых модулей используют agreed layering + DI.
- 0 ad-hoc сервисов вне DI-графа.
- ADR log обновляется для всех ключевых решений.

## Epic Acceptance Criteria
- каркас приложения и DI-граф реализованы и документированы;
- единая схема конфигурации и feature flags действует во всех сервисах;
- определены и покрыты тестами базовые infra contracts;
- Definition of Ready/Done для stories согласованы.

## Risks and Mitigation
- Риск: over-engineering каркаса.  
  Mitigation: ограничить baseline только необходимыми интерфейсами demo.

## Definition of Done
- архитектурный bootstrap готов;
- quality gates подключены;
- docs и ADR синхронизированы;
- есть стартовый набор stories для next epics.

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-01-01 | [Layered module bootstrap](./EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-01-layered-module-bootstrap.md) | Done (Committed) |
| STORY-M2-01-02 | [DI providers and service factory baseline](./EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-02-di-providers-and-service-factory-baseline.md) | Done (Committed) |
| STORY-M2-01-03 | [Config schema and feature flags baseline](./EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-03-config-schema-and-feature-flags-baseline.md) | Done (Committed) |
| STORY-M2-01-04 | [Unified error envelope and trace propagation](./EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-04-unified-error-envelope-and-trace-propagation.md) | Done (Committed) |
