# Acceptance verification — GW-DRAFT-07 T07

- **Task:** task-gw-draft-07-t07-audit-r1-ac-retry-wording-align
- **Result:** PASS
- **Date:** 2026-08-07T09:19:57Z

## Evidence

- Backlog AC + T05 bullet: idempotent **202** + same `story_id`; GET draft **404** — [`STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md`](../../../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- Pipeline AC aligned — pipeline story same wording
- Gate checklist row wording aligned (PASS evidence unchanged) — [`story-acceptance-gate-STORY-GW-DRAFT-07.md`](../task-gw-draft-07-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-07.md)
- `rg '404/expired'` on backlog story → no match; idempotent / same story_id present
- Code unchanged: [`handlers.py:656-713`](../../../../../../../../src/core/api/handlers.py) `_story_intake_replay_from_idempotency`
