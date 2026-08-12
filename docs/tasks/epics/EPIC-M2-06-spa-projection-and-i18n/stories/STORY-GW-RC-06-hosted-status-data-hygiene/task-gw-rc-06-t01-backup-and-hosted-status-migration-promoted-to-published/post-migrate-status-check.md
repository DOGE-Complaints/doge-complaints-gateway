# Post-migrate status check — GW-RC-06 T01

**Date:** 2026-06-20

## SQL equivalent

```sql
SELECT count(*) FROM public.doge_issues WHERE status = 'promoted';
-- Expected: 0
```

## Hosted REST post-check

| Check | Result |
|-------|--------|
| Rows with `status='promoted'` before UPDATE | 5 |
| Rows PATCHed `promoted` → `PUBLISHED` | 5 |
| Rows with `status='promoted'` after UPDATE | **0** |
| All 5 pre-migrate rows now `PUBLISHED` | **yes** |

## Backup

Pre-migrate full row export: [`hosted-doge-issues-backup-pre-status-migration.json`](./hosted-doge-issues-backup-pre-status-migration.json)
