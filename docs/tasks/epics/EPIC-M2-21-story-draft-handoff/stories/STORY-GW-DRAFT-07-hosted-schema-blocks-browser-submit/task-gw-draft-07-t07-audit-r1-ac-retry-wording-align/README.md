# task-gw-draft-07-t07-audit-r1-ac-retry-wording-align

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000057
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-DRAFT-07
- **Depends on:** T01–T06 Done
- **Audit ref:** [`audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md`](../../../../../../analysis/audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md) **R1**

## Purpose
Выровнять AC wording «повторный Submit → 404/expired» на as-built контракт: idempotent **202** + same `story_id` (`_story_intake_replay_from_idempotency`); GET draft after → **404**. Без изменения `src/`.

## Code Facts
- Replay — [`handlers.py:656-713`](../../../../../../../../src/core/api/handlers.py) `_story_intake_replay_from_idempotency` → 202
- Backlog AC literal — [`STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md:77`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- Pipeline AC — pipeline story AC bullet same wording
- Gate — [`story-acceptance-gate-STORY-GW-DRAFT-07.md`](../task-gw-draft-07-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-07.md) already notes as-built 202
- Evidence — [`evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md`](../../../../../../analysis/evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md)

## Acceptance / DoD
- [x] Backlog AC + T05 bullet wording = idempotent 202 + same story_id; GET 404 (no false second publish)
- [x] Pipeline story AC / T05 bullet aligned
- [x] Gate checklist row wording aligned (PASS evidence unchanged)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t07.md`](./acceptance-verification-gw-draft-07-t07.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md`
- `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md`
- `…/task-gw-draft-07-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-07.md` (wording only)

## Out of scope
- Changing handlers / idempotency behavior
- R2 present-tense (T08); G4 tests (T09); SPA (T10)

## Verification commands
```bash
rg '404/expired' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md || test $? -eq 1
rg 'idempotent|same story_id|_story_intake_replay' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md
```
