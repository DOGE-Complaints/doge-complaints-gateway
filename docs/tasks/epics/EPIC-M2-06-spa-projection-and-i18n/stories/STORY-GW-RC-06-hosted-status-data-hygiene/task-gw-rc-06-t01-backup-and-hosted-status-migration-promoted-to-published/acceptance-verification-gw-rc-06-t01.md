# Acceptance — TASK-GW-RC-06-T01

- **Result:** PASS
- **Date:** 2026-06-20

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| Backup export before UPDATE | PASS | `hosted-doge-issues-backup-pre-status-migration.json` (5 rows) |
| `UPDATE promoted→PUBLISHED` on hosted | PASS | PATCH via Supabase REST; 5 rows updated |
| Post-migrate: no `status='promoted'` | PASS | `post-migrate-status-check.md` — count 0 |
