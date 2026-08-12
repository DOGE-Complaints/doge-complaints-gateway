# task-gw-cab-01-t01-decision-lock-status-mapping-and-metrics-spec

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** analyze / docs
- **Status:** 🟢 Done
- **Package:** pkg-000052
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Закрыть 4 «Открытые вопросы» pipeline story: зафиксировать D-CAB01-1..4 в [`STORY-GW-CAB-01-story-activity-api.md`](../STORY-GW-CAB-01-story-activity-api.md) без изменения backlog wording. Блокирует логику T02–T04.

## Code Facts
- Open questions — pipeline story §«Открытые вопросы»
- SPA status mapping SSOT — [`STORY-SPA-CAB-api-requirements.md:23`](../../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md) `PUBLISHED/DRAFT ↔ published/under_review`
- Issue status enum — [`enums.py:6`](../../../../../../../../src/core/projection/enums.py#L6) `DOGEIssueStatus`
- Story lifecycle enum — [`contracts.py:20`](../../../../../../../../src/core/domain/contracts.py#L20) `StoryLifecycleStatus`
- Story↔issue link — [`db_sqlite.py:277`](../../../../../../../../src/core/infrastructure/db_sqlite.py#L277) `issue_story_links`
- Author from `/me` on submit — [`authoritative_submitter.py:36`](../../../../../../../../src/core/identity/authoritative_submitter.py#L36)

## Acceptance / DoD
- [x] D-CAB01-1..4 записаны в pipeline story §«Решения» (не в backlog file)
- [x] Traces parent open Q1–Q4 closed with explicit decision text
- [x] decision_ref: SPA §0 + backlog source path
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t01.md`](./acceptance-verification-gw-cab-01-t01.md) signed (Date post P3 verify only)

## Where to change
- [`STORY-GW-CAB-01-story-activity-api.md`](../STORY-GW-CAB-01-story-activity-api.md) — §Решения D-CAB01-1..4

## Out of scope
- Code changes (T02+)
- Backlog file edits

## Verification commands
```bash
rg 'D-CAB01-[1-4]' doge-complaints-gateway/docs/tasks/epics/EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-01-story-activity-api/STORY-GW-CAB-01-story-activity-api.md
# expect 4 filled decisions after P3
```
