# EPIC-M2-05: Distinct Issue Promotion and Reviewability

## Epic Meta
- Status: Implemented (Waiting Commits)
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

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-05-01 | [Issue candidate state machine and lifecycle](./EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-01-issue-candidate-state-machine-and-lifecycle.md) | Implemented (Waiting Commits) |
| STORY-M2-05-02 | [Promotion gate evaluator baseline](./EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-02-promotion-gate-evaluator-baseline.md) | Implemented (Waiting Commits) |
| STORY-M2-05-03 | [Split merge reframe command handlers](./EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-03-split-merge-reframe-command-handlers.md) | Implemented (Waiting Commits) |
| STORY-M2-05-04 | [Review audit log repository](./EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-04-review-audit-log-repository.md) | Implemented (Waiting Commits) |
