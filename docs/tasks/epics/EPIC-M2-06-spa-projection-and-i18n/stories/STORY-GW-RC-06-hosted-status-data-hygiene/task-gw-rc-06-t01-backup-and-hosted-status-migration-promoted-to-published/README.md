# task-gw-rc-06-t01

## Meta
- **Story:** [STORY-GW-RC-06](../STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Type:** data
- **Status:** ⚪ Todo
- **Package:** pkg-000035
- **Skill declared:** python-pro

## Purpose
Резервная выгрузка текущих 5 hosted записей `doge_issues` → SQL `UPDATE promoted→PUBLISHED` на hosted Supabase (D-RC05-2).

## Code Facts
- Hosted rows — [`investigation-empty-board-status-vocabulary-2026-06-20.md`](../../../../../../backlog-stories/issues-read-contract/investigation-empty-board-status-vocabulary-2026-06-20.md) §E3: 5× `test-*`, all `status='promoted'`
- Recommended SQL — same investigation §Recommended fixes 3: `UPDATE public.doge_issues SET status = 'PUBLISHED' WHERE status = 'promoted';`
- Board enum — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11) `DOGEIssueStatus` = NEW/IN_REVIEW/PUBLISHED
- Decision — [`interview-rc05-rc06-status-vocabulary-2026-06-20.md`](../../../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) D-RC05-2

## Acceptance / DoD
- Traces parent AC: на hosted нет `doge_issues.status='promoted'` (все board-vocab)
- Backup export of current 5 rows saved in task folder (before UPDATE)
- `UPDATE public.doge_issues SET status='PUBLISHED' WHERE status='promoted'` executed on hosted
- Post-migrate check: `SELECT count(*) FROM doge_issues WHERE status = 'promoted'` → 0
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Hosted Supabase (operator ops) — **not** `src/core/` code
- Task artifacts: backup SQL/export file in this task folder

## Out of scope
- Application code changes (RC-05)
- S1 empty content (T02–T03)

## Verification commands
```bash
# Post-migrate (hosted Supabase SQL editor or psql)
# SELECT issue_id, status FROM public.doge_issues WHERE status = 'promoted';
# Expected: 0 rows
```
