# STORY-M2-02-01: Story Intake Request/Response Contract

## Meta
- Key: `STORY-M2-02-01`
- Parent Epic: [`EPIC-M2-02-story-intake-and-store.md`](../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Intake
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Определить и реализовать versioned контракт `StoryIntakeRequest/Response`, включая `submitter` для авторства и стабильный envelope-ответ.

## Scope
- request contract (`schema_version`, `submitter`, `narrative`, optional blocks);
- response contract (success/error envelopes);
- базовая contract validation;
- test coverage для shape и backward-safe эволюции.

## AC / DoD
- [ ] Контракт intake request описан и реализован.
- [ ] Контракт response описан и реализован.
- [ ] Поддержана версия контракта (`schema_version`).
- [ ] `submitter.external_user_id` принят как opaque строка без жесткого формата.
- [ ] Добавлены contract tests для request/response shape.

## Task Artifacts
- Task workspace: [`../../../task-m2-02-01-story-intake-request-response-contract/README.md`](../../../task-m2-02-01-story-intake-request-response-contract/README.md)
- Task specification: [`../../../task-m2-02-01-story-intake-request-response-contract/task-m2-02-01-story-intake-request-response-contract.md`](../../../task-m2-02-01-story-intake-request-response-contract/task-m2-02-01-story-intake-request-response-contract.md)
- Phase log: [`../../../task-m2-02-01-story-intake-request-response-contract/BULLRUN-PHASE-LOG.md`](../../../task-m2-02-01-story-intake-request-response-contract/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-02-01-story-intake-request-response-contract/acceptance-verification-STORY-M2-02-01.md`](../../../task-m2-02-01-story-intake-request-response-contract/acceptance-verification-STORY-M2-02-01.md)
