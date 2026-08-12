# task-gw-rc-06-t03

## Meta
- **Story:** [STORY-GW-RC-06](../STORY-GW-RC-06-hosted-status-data-hygiene.md)
- **Type:** data
- **Status:** ⚪ Todo
- **Package:** pkg-000035
- **Skill declared:** python-pro
- **Depends on:** T02 (audit complete)

## Purpose
Ре-проджектинг восстановимых записей через `reproject_issue_i18n.py`; для невосстановимых — решение (оставить/удалить как test-seed).

## Code Facts
- Reproject script — [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) `run_reproject()`, `--dry-run`, `--issue-id`
- Operator manual — [`docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md`](../../../../../../../docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md)
- Bridge — [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) `StoryPromotionProjectionBridge.build_projection_input`
- Decision D-RC05-3 — [`interview-rc05-rc06-status-vocabulary-2026-06-20.md`](../../../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md)

## Acceptance / DoD
- Traces parent AC: записи с пустым контентом либо ре-проджектнуты, либо явно помечены как test-seed/удалены
- Recoverable rows: `reproject_issue_i18n.py` run (dry-run then apply) per T02 audit
- Unrecoverable rows: documented decision (test-seed label or DELETE) in task artifact
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Hosted data via [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py) (ops)
- Task decision artifact in this folder
- **Not** `src/core/` unless script bug found (escalate)

## Verification commands
```bash
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --dry-run
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --issue-id <recoverable-id>
# Post-check hosted: title_json/summary_json populated for reprojected rows
```
