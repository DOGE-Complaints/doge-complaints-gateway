# Acceptance verification — GW-DRAFT-07 T01

- **Task:** task-gw-draft-07-t01-hosted-readiness-table-inventory
- **Result:** PASS
- **Date:** 2026-08-06T21:09:44Z

## Evidence

### Code set (`REQUIRED_READINESS_TABLES`)
- [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py) — includes `story_labels` (verified via `rg`).

### Hosted Public Node `lvfrdtglpksmaywqlohj` (Supabase `execute_sql` 2026-08-06)

| table_name | present |
|------------|---------|
| cluster_memberships | true |
| doge_issue_embeddings | true |
| doge_issues | true |
| idempotency_keys | true |
| issue_candidates | true |
| issue_story_links | true |
| review_audit_log | true |
| stories | true |
| story_drafts | true |
| story_embeddings | true |
| story_labels | **false** |
| story_signals | true |

**Verdict:** missing **only** `story_labels` among `REQUIRED_READINESS_TABLES`.
