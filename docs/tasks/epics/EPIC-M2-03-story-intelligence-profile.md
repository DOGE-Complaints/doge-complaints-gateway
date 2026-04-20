# EPIC-M2-03: Story Intelligence Profile

## Epic Meta
- Status: Draft
- Priority: High
- Owner: TBD
- Target: Sprint 2

## Business Goal
Превратить stories в аналитически пригодные сигналы без потери исходного narrative.

## Problem Statement
Без структурированного signal profile невозможно устойчиво строить кластерные линзы и reviewability.

## Scope
### In Scope
- профиль сигналов (topic, system-failure, need, desired state, repeatability, relevance);
- separation user-asserted vs system-inferred fields;
- versioning profile updates;
- enrichment pipeline.

### Out of Scope
- кластерный UI;
- distinct issue promotion.

## Stakeholders
- Product Analytics
- Backend/Data team
- QA

## Dependencies
- EPIC-M2-02 completed

## Success Metrics
- >90% story records имеют заполненный минимальный signal profile;
- profile updates не модифицируют original narrative.

## Epic Acceptance Criteria
- профиль создается и обновляется независимо от story core;
- есть история версий signal profile;
- explainable fields доступны для cluster engine;
- тесты на profile consistency проходят.

## Risks and Mitigation
- Риск: агрессивная интерпретация искажет смысл.  
  Mitigation: хранить и показывать distinction “user said” vs “system inferred”.

## Definition of Done
- intelligence pipeline стабилен;
- данные пригодны для multi-lens clustering.

## Initial Story Decomposition (Draft)
- STORY-M2-03-01: design signal profile schema
- STORY-M2-03-02: implement enrichment service
- STORY-M2-03-03: profile versioning and audit trail
- STORY-M2-03-04: profile quality validation tests
