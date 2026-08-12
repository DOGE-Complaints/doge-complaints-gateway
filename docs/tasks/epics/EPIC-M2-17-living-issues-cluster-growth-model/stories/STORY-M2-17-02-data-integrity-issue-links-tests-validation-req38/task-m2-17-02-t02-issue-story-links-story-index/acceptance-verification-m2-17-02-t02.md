# Acceptance verification — TASK-M2-17-02-T02

- **Task:** `idx_issue_story_links_story` DDL
- **Result:** PASS
- **Evidence:** `supabase/bootstrap/000_full_init.sql` L143; `supabase/migrations/20260517_1200_issue_story_links_story_idx.sql`
- **Commands:** grep `idx_issue_story_links_story` in bootstrap + migration
