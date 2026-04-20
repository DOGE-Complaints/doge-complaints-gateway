# EPIC-M2-02: Story Intake and Story Store

## Epic Meta
- Status: Done (Committed)
- Priority: Critical
- Owner: TBD
- Target: Sprint 1-2

## Business Goal
Зафиксировать story как первичный актив продукта и обеспечить intake без forced collapse в issue.

## Problem Statement
Legacy intake ориентирован на complaint-flow и не обеспечивает корректный story-first lifecycle.

## Scope
### In Scope
- story intake contracts;
- story persistence (immutable narrative + mutable derived layers);
- readiness states;
- origin linkage (intake source tracking);
- **фиксация авторства:** сохранение `submitter.external_user_id` (opaque, формат не фиксируется) и при необходимости `identity_issuer`, полученных из OAuth-потока на стороне GPT/IdP — без потери на пути intake → store → evidence;
- idempotent intake command.

### Out of Scope
- кластеризация;
- issue projection;
- evidence pack.

## Stakeholders
- Product Lead
- Data/Backend team
- QA team

## Dependencies
- EPIC-M2-01 completed

## Success Metrics
- 100% историй сохраняются как отдельные объекты;
- отсутствует forced merge на intake этапе;
- intake errors классифицируются и наблюдаемы.

## Epic Acceptance Criteria
- intake endpoint принимает narrative package по новому контракту (включая блок `submitter` при политике с логином);
- story layer хранит original narrative отдельно от интерпретаций;
- внешний идентификатор автора сохраняется в персистентной модели и доступен для lineage;
- readiness lifecycle покрыт unit/integration тестами;
- mapping legacy->story documented.

## Risks and Mitigation
- Риск: неполные истории блокируют intake.  
  Mitigation: partial-ready статусы и мягкая валидация на intake.

## Definition of Done
- intake и store стабильно работают;
- данные готовы для profile enrichment;
- документация по контракту опубликована.

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-02-01 | [Story intake request/response contract](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-01-story-intake-request-response-contract.md) | Done (Committed) |
| STORY-M2-02-02 | [Story repository lifecycle and authorship linkage](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-02-story-repository-lifecycle-and-authorship-linkage.md) | Done (Committed) |
| STORY-M2-02-03 | [Intake idempotency key handling](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md) | Done (Committed) |
| STORY-M2-02-04 | [Intake observability and error taxonomy](./EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-04-intake-observability-and-error-taxonomy.md) | Done (Committed) |
