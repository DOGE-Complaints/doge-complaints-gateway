# task-gw-rc-05-t02

## Meta
- **Story:** [STORY-GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000034
- **Skill declared:** python-pro
- **Depends on:** T01 (write-fix; read canon is defense-in-depth, can proceed in parallel after T01 pattern clear)

## Purpose
`canonicalize_status_on_read` в `read_filters` (alias `promoted`→`PUBLISHED`, unknown→default+log); применить в merge-выводе и фильтре статуса.

## Code Facts
- Read passthrough — [`read_filters.py:234`](../../../../../../../src/core/projection/read_filters.py#L234) `out["status"] = row_status`
- Status filter raw — [`read_filters.py:271`](../../../../../../../src/core/projection/read_filters.py#L271) `row_status not in status_values`
- Pattern to mirror — [`read_filters.py:150-171,236,265-268`](../../../../../../../src/core/projection/read_filters.py#L150-L171) `canonicalize_issue_type_on_read`
- Board enum — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11) `{NEW, IN_REVIEW, PUBLISHED}`
- Anomaly log pattern — `record_unknown_issue_type` in same module (RC-02)

## Acceptance / DoD
- Traces parent AC: `GET /tallinn/issues` отдаёт `status ∈ {NEW,IN_REVIEW,PUBLISHED}` даже для legacy `promoted` (read-канонизация)
- Helper `canonicalize_status_on_read()` wired in `merge_projection_columns` output
- Status filter in `filter_projection_rows` compares canonical values (mirror type :265-268)
- Known alias `promoted` → `PUBLISHED`
- Unknown status behavior documented (mirror RC-02: default + log); open product question in parent story
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/projection/read_filters.py`](../../../../../../../src/core/projection/read_filters.py) — helper + wire in merge output and status filter
- New unit test file `tests/test_gw_rc_05_status_canonical_on_read.py` (P3)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_05_status_canonical_on_read.py -q
```
