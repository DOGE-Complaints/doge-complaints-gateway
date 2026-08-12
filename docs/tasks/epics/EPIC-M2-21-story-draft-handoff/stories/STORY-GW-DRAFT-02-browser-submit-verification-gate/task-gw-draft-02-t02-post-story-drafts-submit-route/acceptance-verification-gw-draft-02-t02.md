# Acceptance — TASK-GW-DRAFT-02-T02

- **Result:** PASS
- **Date:** 2026-07-03

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| `POST /story-drafts/{draft_id}/submit` route | PASS | `asgi_app.py` — `story_draft_submit`, `require_story_draft_submit_user`, `extract_authorization_bearer` |

**Live run:** `tests/test_gw_draft_02_story_draft_submit_contract.py` → 7 passed (2026-07-03)
