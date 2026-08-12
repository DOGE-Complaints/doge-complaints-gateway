# task-gw-rc-07-t03

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000047
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
Per-row read probe: изолировать issue_id/поле, ломающее list read на hosted (7 новых INCIDENT + legacy test row).

## Code Facts
- Handler — [`handlers.py:368`](../../../../../../../src/core/api/handlers.py) `handle_tallinn_issues_list` → `list_projections` L390
- Read filters — [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py) `filter_projection_rows`
- Read store — [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) projection merge
- Contract tests — [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py)
- `INCIDENT` valid — [`enums.py:19`](../../../../../../../src/core/projection/enums.py)
- Hosted row count — audit CF-B: **8** PUBLISHED

## Acceptance / DoD
- Artifact [`per-row-read-probe.md`](./per-row-read-probe.md): each issue_id probed; failing row(s) identified or ruled out
- Traces parent AC #2 (isolation leg): Root cause изолирован (T03)
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t03.md`](./acceptance-verification-gw-rc-07-t03.md) signed

## Where to change
- Task artifact: `per-row-read-probe.md`
- Optional: diagnostic script under `tests/` (if added in P3)

## Out of scope
- Production fix (T04)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py
python3 -m pytest -q tests/ -k "tallinn or projection or read_filter"
# Per-issue probe against hosted DB snapshot — document in per-row-read-probe.md
```
