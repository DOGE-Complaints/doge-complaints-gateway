# Acceptance verification — GW-TAX-03 T02

- **Task:** task-gw-tax-03-t02-align-migration-text-fk
- **Result:** PASS
- **Date:** 2026-08-07T09:59:37Z

## Evidence

- File: [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql) edited **in-place**
- `story_id text NOT NULL REFERENCES stories(story_id)` (no UUID column type)
- Indexes: `idx_story_labels_story`, `idx_story_labels_axis`
- Guard header: UUID incompatible with text `stories.story_id`
- Verify: `rg UUID` on column DDL → no match for `story_id UUID`
