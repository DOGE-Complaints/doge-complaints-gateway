# task-gw-rc-03-t03

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** data
- **Status:** 🟢 N/A (T02 defer)
- **Package:** pkg-000032 (gated)
- **Skill declared:** python-pro
- **Depends on:** T02 decision = `backfill_now` (otherwise **Skip / N/A**)

## Purpose
(Опционально, по решению T02) бэкфилл legacy через ре-проджектинг — legacy-issue получают недостающие поля (`institution`/`geo`/`original_locale`/provenance txids).

## Code Facts
- Reproject script — [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py)
- Autotests precedent — [`test_reproject_issue_i18n.py`](../../../../../../../tests/test_reproject_issue_i18n.py)
- T02 decision artifact — [`../task-gw-rc-03-t02-legacy-sql-audit-five-live-records/legacy-audit-five-records.md`](../task-gw-rc-03-t02-legacy-sql-audit-five-live-records/legacy-audit-five-records.md) (create at T02)

## Acceptance / DoD
- Traces parent AC: (Если решено) legacy-issue получили недостающие поля
- **Gate:** N/A if T02 decision = `defer` (default per D-RC-3)
- Runbook: reproject invocation for audited issue_ids
- Optional test assertion post-backfill
- BULLRUN phases complete
- Acceptance file signed (or N/A with T02 defer evidence)

## Where to change
- Runbook in task folder + optional test in `tests/test_reproject_issue_i18n.py` or `tests/test_gw_rc_03_contract_guarantee.py`

## Out of scope
- Read-path code changes (data-only gap)
- FE changes

## Verification commands
```bash
cd doge-complaints-gateway && python3 scripts/reproject_issue_i18n.py --help
cd doge-complaints-gateway && python3 -m pytest tests/test_reproject_issue_i18n.py -q
```
