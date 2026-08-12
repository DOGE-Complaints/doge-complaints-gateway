# Acceptance — TASK-GW-CAB-01-T02

- **Result:** PASS
- **Date:** 2026-07-13T09:59:00Z

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Filter by author `sub` via `submitter_external_user_id` | PASS | `contracts.py` `list_stories_by_submitter`; used by `StoryActivityService` |
| All backends (in_memory, sqlite, supabase) | PASS | `repositories.py`, `db_sqlite.py`, `db_supabase.py` |
| DB-level filter per D-CAB01-4 | PASS | SQL `WHERE submitter_external_user_id = ?` / Supabase `.eq(...)` |
