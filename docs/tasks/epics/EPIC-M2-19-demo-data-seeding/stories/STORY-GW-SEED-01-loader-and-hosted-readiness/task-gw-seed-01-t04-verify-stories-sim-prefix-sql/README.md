# task-gw-seed-01-t04

## Meta
- **Story:** [STORY-GW-SEED-01](../STORY-GW-SEED-01-loader-and-hosted-readiness.md)
- **Type:** verify
- **Status:** ⚪ Todo
- **Package:** pkg-000036
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Зафиксировать факт записи (SQL по `stories` где `submitter_external_user_id LIKE 'sim:%'`).

## Code Facts
- Loader submitter prefix — [`simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — `sim:` external user ids on intake
- Table — `public.stories` on hosted Supabase
- Backlog scope — SQL verify `sim:*` in `stories` (submitter_external_user_id)

## Acceptance / DoD
- Traces parent AC: В `stories` появились строки `sim:*` (AC4)
- SQL query executed on hosted Supabase: `SELECT count(*) FROM public.stories WHERE submitter_external_user_id LIKE 'sim:%';`
- Count ≥ 130 after full run (or documented delta with cause)
- Query result saved in this task folder
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Hosted Supabase SQL — operator ops
- Task artifacts: SQL result export in this task folder

## Out of scope
- `doge_issues` / board card count (SEED-03)
- Application code

## Verification commands
```bash
# Hosted Supabase SQL editor or psql
# SELECT count(*) FROM public.stories WHERE submitter_external_user_id LIKE 'sim:%';
# Expected: >= 130 after T03 full run
```
