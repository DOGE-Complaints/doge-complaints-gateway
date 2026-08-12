# task-gw-rc-03-t02

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000032
- **Skill declared:** python-pro
- **Depends on:** T01 (optional parallel)

## Purpose
SQL-аудит 5 live-записей (наличие id/status/type/institution/geo/original_locale/txids в payload). Зафиксировать решение по бэкфиллу (defer vs backfill now) для T03 gate.

## Code Facts
- Projection table — [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py), [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- Payload shape — [`dto.py:26-50`](../../../../../../../src/core/projection/dto.py#L26-L50) (`institution`, `geo`, `original_locale`, `arweave_txid`, `image_txid`, `image_hash`)
- Interview §4 open question — [`interview-issues-read-contract-2026-06-19.md`](../../../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md)

## Acceptance / DoD
- Traces parent AC: проведён аудит legacy-записей; принято и зафиксировано решение по бэкфиллу
- Audit artifact: `legacy-audit-five-records.md` in task folder (SQL + findings table)
- Decision recorded: `defer` (default) or `backfill_now` → unblocks/skips T03
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `legacy-audit-five-records.md` (task folder artifact)
- README runbook SQL steps (no prod mutation without T03)

## Out of scope
- Runtime code changes
- FE changes
- Mandatory backfill (T03 if decision = backfill_now)

## Verification commands
```bash
# Manual: run audit SQL against target DB (see legacy-audit-five-records.md)
```
