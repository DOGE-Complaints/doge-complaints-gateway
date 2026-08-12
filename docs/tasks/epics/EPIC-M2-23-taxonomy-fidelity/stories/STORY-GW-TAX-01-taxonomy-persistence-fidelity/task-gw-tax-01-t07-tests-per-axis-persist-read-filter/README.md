# task-gw-tax-01-t07-tests-per-axis-persist-read-filter

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** test
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T04, T05, T06

## Purpose
Тесты (backlog firm T07): per-axis приём (ось из контракта, не угадана), persist всех dispositions, read-filter исключает internal, legacy fallback, миграция таблицы.

## Code Facts
- Test namespace — `tests/test_gw_tax_01_*` (backlog firm T07)
- Patterns: intake fixtures — [`tests/intake_v2_fixtures.py`](../../../../../../../../tests/intake_v2_fixtures.py), story intake helpers
- No existing `test_gw_tax_01_*` files (grep → 0)

## Acceptance / DoD
- [ ] Traces parent AC-1..AC-4 via contract tests
- [ ] Traces parent AC-5: tests green under `-m "not live_integration"`
- [ ] Scope trace: backlog firm T07
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t07.md`](./acceptance-verification-gw-tax-01-t07.md) signed (Date post live-run only)

## Where to change
- `tests/test_gw_tax_01_*.py` (new)

## Out of scope
- Story gate signing (T08)
- Live integration tests

## Verification commands (post live-run only)
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_01_* -m "not live_integration"
```
