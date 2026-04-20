# EPIC-M2-07: Evidence Pack and Lineage

## Epic Meta
- Status: Done (Committed)
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

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-07-01 | [Evidence pack schema](./EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-01-evidence-pack-schema.md) | Done (Committed) |
| STORY-M2-07-02 | [Lineage graph persistence](./EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-02-lineage-graph-persistence.md) | Done (Committed) |
| STORY-M2-07-03 | [Visibility tiers and redaction](./EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-03-visibility-tiers-and-redaction.md) | Done (Committed) |
| STORY-M2-07-04 | [Evidence export metadata](./EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-04-evidence-export-metadata.md) | Done (Committed) |
