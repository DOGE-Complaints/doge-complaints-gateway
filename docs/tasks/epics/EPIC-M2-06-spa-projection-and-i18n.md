# EPIC-M2-06: SPA Projection and i18n Contract

## Epic Meta
- Status: Implemented (Waiting Commits)
- Priority: Critical
- Owner: TBD
- Target: Sprint 3

## Business Goal
Гарантировать zero-change совместимость с текущим SPA Issue контрактом.

## Problem Statement
Без изолированного projection слоя любое изменение доменной модели начнет ломать BoardPage/IssuePage.

## Scope
### In Scope
- projection engine;
- strict Issue contract mapping;
- i18n `{et,ru,en}` для title/summary/description;
- fallback summary -> title;
- enum governance for status/type/labels.

### Out of Scope
- изменение SPA кода;
- tokenization tx fields real population.

## Stakeholders
- Frontend team
- Product Owner
- Backend team

## Dependencies
- EPIC-M2-05 completed

## Success Metrics
- 0 contract breaks against current SPA consumers;
- 100% projected issues проходят contract tests.

## Epic Acceptance Criteria
- projection output соответствует обязательным полям;
- optional fields заполняются только валидными значениями;
- фиктивные txid не генерируются;
- contract tests интегрированы в quality gate.

## Risks and Mitigation
- Риск: расхождение словарей labels/type между командами.  
  Mitigation: единый dictionary governance и schema checks.

## Definition of Done
- projection стабильна;
- UI потребляет новые данные без изменений кода.

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-06-01 | [SPA projection DTO and mapper](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-01-spa-projection-dto-and-mapper.md) | Implemented (Waiting Commits) |
| STORY-M2-06-02 | [i18n projection policy](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-02-i18n-projection-policy.md) | Implemented (Waiting Commits) |
| STORY-M2-06-03 | [SPA projection contract test suite](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-03-spa-projection-contract-tests.md) | Implemented (Waiting Commits) |
| STORY-M2-06-04 | [SPA enum governance checks](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-04-spa-enum-governance.md) | Implemented (Waiting Commits) |
