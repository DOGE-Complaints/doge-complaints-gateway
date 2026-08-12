# task-gw-draft-07-t08-audit-r2-post-done-as-is-tense

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000057
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-DRAFT-07
- **Depends on:** T07 (or parallel docs)
- **Audit ref:** [`audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md`](../../../../../../analysis/audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md) **R2**

## Purpose
Убрать present-tense pre-fix «as-is» при Status Done: Depends «hosted DDL — нет»; §«Что наблюдаю сейчас» с live 503/`schema=false`. Пометить pre-fix UAT 2026-08-06; добавить post-Done текущее состояние (ready+schema true).

## Code Facts
- Backlog Depends — [`STORY-GW-DRAFT-07…md:11`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) «hosted DDL … **нет**»
- Pipeline Depends — pipeline Meta same
- Live post-fix — `/ready` schema true (T04/evidence); inventory `story_labels` present
- Status Done — Meta Status 🔵 Done pkg-000056

## Acceptance / DoD
- [x] Depends: hosted DDL **applied** (DRAFT-07 T02) — both backlog + pipeline
- [x] §«Что наблюдаю» labeled pre-fix / historical; post-Done current state section present
- [x] No claim that submit still 503 / schema false as current
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t08.md`](./acceptance-verification-gw-draft-07-t08.md) signed (Date post P6 verify only)

## Where to change
- backlog + pipeline `STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md`

## Out of scope
- AC retry wording (T07); dashboard (R3 Closed); UUID migration (TAX-03); SPA

## Verification commands
```bash
rg 'hosted DDL для `story_labels` — \*\*нет\*\*' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md || test $? -eq 1
rg 'hosted DDL.*applied|T02' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md
```
