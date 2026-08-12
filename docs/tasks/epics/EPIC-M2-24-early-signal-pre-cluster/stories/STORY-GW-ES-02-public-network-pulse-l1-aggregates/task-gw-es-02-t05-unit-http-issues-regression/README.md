# task-gw-es-02-t05-unit-http-issues-regression

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** T01; T03 (HTTP smoke needs route)
- **decision_ref:** backlog ES-02 §E; PUBLIC-01 regression lineage

## Purpose
Unit-тесты `NetworkPulseService` (in-memory repos: counts, dims, 7d, no PII keys) + HTTP public GET без auth → 200 envelope; Issues L3 regression smoke green.

## Code Facts
- Pattern — `tests/test_gw_public_01_*` (PUBLIC-01)
- Issues handler — [`handlers.py:362`](../../../../../../../../src/core/api/handlers.py)
- Etalon activity tests may exist near story_activity consumers

## Acceptance / DoD
- [x] Traces parent AC: unit + HTTP public smoke; `GET /tallinn/issues` unchanged (regression)
- [x] Tests live under `tests/test_gw_es_02_*`
- [x] Assert no PII keys in pulse payload; Topic≠Issue key naming covered or deferred to T04 evidence
- [x] Offline suite relevant slice green
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t05.md` signed (Date post P3 verify only)

## Where to change
- New: `doge-complaints-gateway/tests/test_gw_es_02_*.py`

## Out of scope
- Live hosted integration; SQL count RPC perf tests

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_02_*.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py
```
