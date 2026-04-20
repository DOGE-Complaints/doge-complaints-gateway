# EPIC-M2-07: Evidence Pack and Lineage

## Epic Meta
- Status: Draft
- Priority: High
- Owner: TBD
- Target: Sprint 3-4

## Business Goal
Обеспечить доказательную связность `story <-> cluster <-> issue` и отделить evidence слой от публичной карточки.

## Problem Statement
Issue без provenance и evidence разрушает доверие и не годится для дальнейшей верификации/токенизации.

## Scope
### In Scope
- evidence pack model;
- lineage links and snapshots;
- public/internal visibility tiers;
- export-ready evidence bundle metadata.

### Out of Scope
- on-chain evidence anchoring;
- external gov submission.

## Stakeholders
- Product Lead
- Legal/Policy stakeholders
- Backend/Data team

## Dependencies
- EPIC-M2-05 and EPIC-M2-06 completed

## Success Metrics
- 100% distinct issues имеют полную lineage цепочку;
- evidence pack доступен для drill-down без утечки лишних данных.

## Epic Acceptance Criteria
- evidence pack создается отдельно от issue-card;
- lineage запросы обратимы до source stories;
- privacy tiers применяются корректно;
- evidence snapshots версионируются.

## Risks and Mitigation
- Риск: избыточная публичность данных.  
  Mitigation: explicit visibility policy + redaction layer.

## Definition of Done
- evidence и lineage работают как независимый модуль;
- готовность к pilot tokenization prep подтверждена.

## Initial Story Decomposition (Draft)
- STORY-M2-07-01: design evidence pack schema
- STORY-M2-07-02: implement lineage graph persistence
- STORY-M2-07-03: implement visibility tiers and redaction
- STORY-M2-07-04: implement evidence export metadata
