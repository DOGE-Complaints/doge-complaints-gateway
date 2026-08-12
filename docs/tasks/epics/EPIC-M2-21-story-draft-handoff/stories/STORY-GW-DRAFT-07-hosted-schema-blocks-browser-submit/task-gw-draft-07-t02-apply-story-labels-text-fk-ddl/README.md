# task-gw-draft-07-t02-apply-story-labels-text-fk-ddl

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** ops
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog T02: apply proposed SQL (text FK + indexes + RLS + GRANT) on Public Node — [`proposed-migration-DRAFT-07-story-labels-text-fk.sql`](../../../../../../backlog-stories/story-draft-handoff/proposed-migration-DRAFT-07-story-labels-text-fk.sql). Do **not** apply UUID migration as-is.

## Code Facts
- Proposed DDL — [`proposed-migration-DRAFT-07-story-labels-text-fk.sql`](../../../../../../backlog-stories/story-draft-handoff/proposed-migration-DRAFT-07-story-labels-text-fk.sql) (exists)
- Bootstrap canon — [`bootstrap/000_full_init.sql`](../../../../../../../../supabase/bootstrap/000_full_init.sql) `story_labels` text FK + RLS
- UUID migration (incompatible on this host) — [`20260714_1200_gw_tax_01_story_labels.sql`](../../../../../../../../supabase/migrations/20260714_1200_gw_tax_01_story_labels.sql)
- Hosted `stories.story_id` = **text** (story / pin claim)

## Acceptance / DoD
- [x] Traces story target #1–#2: `public.story_labels` created with **text** FK; RLS + `service_role` policy + GRANT applied
- [x] UUID repo migration **not** applied as-is on Public Node
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t02.md`](./acceptance-verification-gw-draft-07-t02.md) signed (Date post P3 verify only)

## Where to change
- Hosted Supabase Public Node (`lvfrdtglpksmaywqlohj`) — SQL apply only
- No gateway `src/` changes

## Out of scope
- Redeploy (T03); rewriting UUID migration for other hosts; SPA/identity/GPT

## Verification commands
```bash
# After apply (operator): PostgREST probe
# GET /rest/v1/story_labels?select=*&limit=1 → 200 (empty ok)
# information_schema: story_labels.story_id data_type = text
```
