# task-gw-tax-01-t05-public-read-filter-by-disposition

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Public read-filter (D-TAX-3): `/tallinn/issues` карточки + cabinet surfaces **никогда** не отдают `internal`; `metadata_only` — по правилу (§24).

## Code Facts
- Read filters module exists — [`read_filters.py`](../../../../../../../../src/core/projection/read_filters.py) — geo/type/status; **disposition filter отсутствует**
- Projection repos import read_filters — [`db_sqlite.py:934`](../../../../../../../../src/core/infrastructure/db_sqlite.py), [`repositories.py:11`](../../../../../../../../src/core/infrastructure/repositories.py)
- Cabinet read surfaces consume projection/issue data

## Acceptance / DoD
- [ ] Traces parent AC-3: public read never exposes `internal` labels (§24)
- [ ] Scope trace: backlog §4 Public read-filter D-TAX-3
- [ ] `metadata_only` handling per §24 rule
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t05.md`](./acceptance-verification-gw-tax-01-t05.md) signed (Date post live-run only)

## Where to change
- [`src/core/projection/read_filters.py`](../../../../../../../../src/core/projection/read_filters.py)
- (if needed) projection read paths using label/taxonomy fields

## Out of scope
- GW-TAX-02 clustering lens changes
- Intake contract (T01)

## Verification commands (post live-run only)
```bash
rg -n "internal|metadata_only|disposition" doge-complaints-gateway/src/core/projection/read_filters.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration" -k read_filter
```
