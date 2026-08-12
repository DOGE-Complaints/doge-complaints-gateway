# SQL verify — sim:* stories — T04

**Date:** 2026-06-21

```sql
SELECT count(*) FROM public.stories
WHERE submitter_external_user_id LIKE 'sim:%';
```

| Result | Value |
|--------|-------|
| Count | **141** |
| Content-Range | `0-0/141` |
| Method | Supabase REST `Prefer: count=exact` |

**Note:** Count ≥ 130 (AC4). Delta 141 vs 130 = prior smoke (10) + full (130) with idempotent overlap on re-POST (same `story_id` for duplicate `simulation_id`).
