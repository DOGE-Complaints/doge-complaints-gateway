# task-gw-es-03-t05-unit-http-issues-regression

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** T01–T04; T03 for HTTP
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
`tests/test_gw_es_03_*`: unit (published exclude, top-N, no PII); contract Emerging ≠ Issues envelope/source; HTTP public smoke; Issues regression green.

## Code Facts
- Etalon suite — [`tests/test_gw_es_02_network_pulse.py`](../../../../../../../../tests/test_gw_es_02_network_pulse.py)
- PUBLIC-01 Issues regression — existing public issues tests
- Published mapping — [`story_activity.py`](../../../../../../../../src/core/application/story_activity.py)

## Acceptance / DoD
- [ ] Traces AC: Emerging ≠ Issues (test); Topic≠Issue / no threshold; no PII; Issues regression
- [ ] Unit: published-linked stories excluded; top-N ordering; no submitter/narrative keys
- [ ] Contract: Emerging payload shape/source ≠ Issues `list_projections` board envelope
- [ ] HTTP public smoke for Emerging path (from T00); Issues regression green
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t05.md` signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/tests/test_gw_es_03_*.py` (new)
- Optionally assert against PUBLIC-01 / Issues list tests still pass

## Out of scope
- OpenAPI prose (T06); inventing path

## Verification commands
```bash
cd doge-complaints-gateway && python -m pytest tests/test_gw_es_03_*.py tests/test_gw_public_01_public_issues_regression.py -q
```
