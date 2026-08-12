# Acceptance — TASK-GW-DRAFT-01-T04

- **Result:** PASS
- **Date:** 2026-07-03

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| GET payload (AC #3) | PASS | `test_get_story_drafts_returns_saved_payload` |
| 404 unknown/expired (AC #3, #5) | PASS | `test_get_story_drafts_unknown_id_returns_404`, `test_get_story_drafts_expired_draft_returns_404` |

**Live run:** `pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py` (GET cases) → pass (2026-07-03)
