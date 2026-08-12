# Acceptance — TASK-GW-CAB-01-T04

- **Result:** PASS
- **Date:** 2026-07-13T09:59:00Z

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| GET /story-activity → 200 + MVP data shape | PASS | `asgi_app.py` route; `handle_story_activity`; T05 tests |
| Author from `user_introspection.sub` | PASS | `story_activity` handler passes `sub` |
| Missing Bearer → 401 | PASS | `_STORY_DRAFT_READ_DEPS`; T05 `test_gw_cab_01_missing_bearer_returns_401` |
| OpenAPI + API_REFERENCE | PASS | `openapi.yaml` `/story-activity`; `API_REFERENCE.md` §6 GW-CAB-01 |
