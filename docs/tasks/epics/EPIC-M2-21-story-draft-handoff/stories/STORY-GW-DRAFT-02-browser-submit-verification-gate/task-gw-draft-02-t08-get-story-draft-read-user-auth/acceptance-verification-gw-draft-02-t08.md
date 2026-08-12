# Acceptance — TASK-GW-DRAFT-02-T08

- **Result:** PASS
- **Date:** 2026-07-03

| AC (audit G1) | Status | Evidence |
|---------------|--------|----------|
| GET requires browser Bearer + `/me` active session | PASS | `require_story_draft_read_user` in `asgi_app.py`; no `phone_verified` gate |

**Live run:** `rg require_story_draft_read_user src/core/api/asgi_app.py` (2026-07-03)
