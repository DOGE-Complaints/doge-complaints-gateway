# task-gw-rc-06-t02

## Meta
- **Story:** [STORY-GW-RC-06](../STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Type:** analyze
- **Status:** ⚪ Todo
- **Package:** pkg-000035
- **Skill declared:** python-pro
- **Depends on:** T01 (status migration complete)

## Purpose
Аудит пустого контента: у каких hosted `test-*` записей с пустым `title_json`/`summary_json` есть `issue_story_links` для ре-проджектинга.

## Code Facts
- Empty content — [`investigation-empty-board-status-vocabulary-2026-06-20.md`](../../../../../../backlog-stories/issues-read-contract/investigation-empty-board-status-vocabulary-2026-06-20.md) §E3: 4/5 rows `title_json={}`
- Links API — [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) `/rest/v1/issue_story_links`
- SQLite schema — [`db_sqlite.py:264`](../../../../../../../src/core/infrastructure/db_sqlite.py#L264) `issue_story_links` table
- Columnar only — `payload_json` removed (RC-04); content in `title_json`/`summary_json` columns

## Acceptance / DoD
- Traces parent AC: input for AC#2 (empty content disposition)
- Per-row audit table: `issue_id`, empty `title_json`/`summary_json` flag, link count, recoverable (Y/N)
- Audit artifact saved in task folder
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Task artifacts only (audit report in this folder)
- Read-only queries against hosted Supabase

## Verification commands
```bash
# Hosted REST (example)
# GET /rest/v1/doge_issues?select=issue_id,status,title_json,summary_json
# GET /rest/v1/issue_story_links?issue_id=eq.<test-id>
```
