# Acceptance — TASK-GW-DRAFT-02-T04

- **Result:** PASS
- **Date:** 2026-07-03

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Idempotency key=`draft_id` + draft cleanup | PASS | `_story_intake_replay_from_idempotency`, `delete_draft` on 202 |

**Live run:** `test_repeat_submit_is_idempotent` (2026-07-03)
