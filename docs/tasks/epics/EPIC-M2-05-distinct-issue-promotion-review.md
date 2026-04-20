# EPIC-M2-05: Distinct Issue Promotion and Reviewability

## Epic Meta
- Status: Draft
- Priority: High
- Owner: TBD
- Target: Sprint 3

## Business Goal
Построить управляемый переход от issue-ready cluster к distinct issue с human/process review.

## Problem Statement
Без явного promotion workflow возникают либо шумные issues, либо излишне задержанная публикация полезных кейсов.

## Scope
### In Scope
- issue-candidate state and lifecycle;
- promotion gates;
- split/merge/reframe workflows;
- reviewability traces (why this issue from which cluster/stories).

### Out of Scope
- SPA contract serialization;
- tokenization publish step.

## Stakeholders
- Product Lead
- Operations/Moderation
- Backend team

## Dependencies
- EPIC-M2-04 completed

## Success Metrics
- снижение false-promotions;
- 100% issue имеют объяснимую provenance цепочку.

## Epic Acceptance Criteria
- candidate lifecycle formalized and enforced;
- promotion gates configurable и тестируемы;
- review logs сохраняют decision rationale;
- merge/split outcomes traceable.

## Risks and Mitigation
- Риск: субъективность review решений.  
  Mitigation: стандартизированные критерии gate + audit trail.

## Definition of Done
- distinct issue pipeline стабилен и объясним;
- готов вход для SPA projection layer.

## Initial Story Decomposition (Draft)
- STORY-M2-05-01: define issue-candidate state machine
- STORY-M2-05-02: implement promotion gate evaluator
- STORY-M2-05-03: implement split/merge/reframe commands
- STORY-M2-05-04: implement review audit log
