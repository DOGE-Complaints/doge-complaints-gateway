# EPIC-M2-06: SPA Projection and i18n Contract

## Epic Meta
- Status: In Progress (REQ-24 STORY-M2-06-06 Done Awaiting Commits; REQ-40 STORY-M2-06-05 Done Awaiting Commits)
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
| STORY-M2-06-01 | [SPA projection DTO and mapper](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-01-spa-projection-dto-and-mapper.md) | Done (Committed) |
| STORY-M2-06-02 | [i18n projection policy](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-02-i18n-projection-policy.md) | Done (Committed) |
| STORY-M2-06-03 | [SPA projection contract test suite](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-03-spa-projection-contract-tests.md) | Done (Committed) |
| STORY-M2-06-04 | [SPA enum governance checks](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-04-spa-enum-governance.md) | Done (Committed) |
| STORY-M2-06-05 | [Geo propagation to issue projection (REQ-40)](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-05-geo-propagation-to-issue-projection-req40/STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md) | Done (Awaiting Commits) |
| STORY-M2-06-06 | [Tallinn issues read API (REQ-24)](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-06-tallinn-issues-read-api-req24/STORY-M2-06-06-tallinn-issues-read-api-req24.md) | Done (Awaiting Commits) |
| STORY-GW-L10N-01 | [Projection content i18n preservation](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-L10N-01-projection-content-i18n-preservation/STORY-GW-L10N-01-projection-content-i18n-preservation.md) | Done (Awaiting Commits) |
| STORY-GW-L10N-02 | [original_locale in public projection](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-L10N-02-original-locale-in-public-projection/STORY-GW-L10N-02-original-locale-in-public-projection.md) | Done (Awaiting Commits) |
| STORY-GW-L10N-03 | [Label miss telemetry sink](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-L10N-03-label-miss-telemetry-sink/STORY-GW-L10N-03-label-miss-telemetry-sink.md) | Done (Awaiting Commits) |
| STORY-GW-RC-01 | [Read-path column merge (id/status/created_at)](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-01-read-path-column-merge/STORY-GW-RC-01-read-path-column-merge.md) | Done (Awaiting Commits) |
| STORY-GW-RC-07 | [Hosted `/tallinn/issues` INTERNAL_ERROR regression](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-RC-07-hosted-tallinn-issues-internal-error/STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md) | Done (Awaiting Commits) |
| STORY-GW-PUBLIC-01 | [Public issues regression gate (M-5)](./EPIC-M2-06-spa-projection-and-i18n/stories/STORY-GW-PUBLIC-01-public-issues-regression/STORY-GW-PUBLIC-01-public-issues-regression.md) | Done (Awaiting Commits) |
