# Acceptance — TASK-GW-DRAFT-01-T02

- **Result:** PASS
- **Date:** 2026-07-03

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| TTL → None/404 (AC #5) | PASS | `get_draft` expiry check in all 3 adapters |
| Отдельный store (AC #6) | PASS | Wired in `providers.py` + `DefaultServiceFactory` |

**Live run:** `rg 'StoryDraft' src/core/infrastructure/` → in_memory/sqlite/supabase adapters (2026-07-03)
