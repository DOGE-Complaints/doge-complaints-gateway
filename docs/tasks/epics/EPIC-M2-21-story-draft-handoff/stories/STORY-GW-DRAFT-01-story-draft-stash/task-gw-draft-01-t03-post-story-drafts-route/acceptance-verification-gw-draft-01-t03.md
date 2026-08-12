# Acceptance — TASK-GW-DRAFT-01-T03

- **Result:** PASS
- **Date:** 2026-07-03

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| POST → `{draft_id}`, no issue (AC #1) | PASS | `test_post_story_drafts_returns_draft_id_without_creating_story` |
| 401 без токена (AC #2) | PASS | `test_post_story_drafts_requires_service_token` |
| 400 invalid contract (AC #4) | PASS | `test_post_story_drafts_returns_400_for_invalid_contract` |

**Live run:** `pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py` (POST cases) → pass (2026-07-03)
