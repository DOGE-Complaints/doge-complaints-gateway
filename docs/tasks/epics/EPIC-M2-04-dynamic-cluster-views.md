# EPIC-M2-04: Dynamic Cluster Views

## Epic Meta
- Status: Draft
- Priority: High
- Owner: TBD
- Target: Sprint 2-3

## Business Goal
Обеспечить многолинзовую кластеризацию stories и управляемую пересборку кластерных представлений.

## Problem Statement
Фиксированные кластеры преждевременно “цементируют” смысл и ломают продуктовую гибкость.

## Scope
### In Scope
- dynamic cluster views;
- multi-membership story <-> cluster;
- micro/local/systemic scales;
- cluster narrative and dominant pattern summary;
- issue-readiness scoring.

### Out of Scope
- финальная issue projection;
- external publication.

## Stakeholders
- Product Lead
- Operations/Review team
- Data/Backend team

## Dependencies
- EPIC-M2-03 completed

## Success Metrics
- одна story может участвовать минимум в 2+ cluster views;
- поддерживается пересборка кластера по новой линзе без потери lineage.

## Epic Acceptance Criteria
- минимум 6 обязательных линз реализованы;
- cluster narrative формируется для каждого кластера;
- аналитический и issue-ready кластеры различаются явно;
- split/merge hooks предусмотрены.

## Risks and Mitigation
- Риск: ложные merge разных проблем.  
  Mitigation: readiness gate + review workflow + explainability.

## Definition of Done
- cluster engine выдает стабильные и объяснимые представления;
- есть API/read-model для дальнейшей промоции в issue.

## Initial Story Decomposition (Draft)
- STORY-M2-04-01: implement cluster lens framework
- STORY-M2-04-02: implement multi-membership mapping
- STORY-M2-04-03: implement cluster narrative generator
- STORY-M2-04-04: implement readiness scoring
