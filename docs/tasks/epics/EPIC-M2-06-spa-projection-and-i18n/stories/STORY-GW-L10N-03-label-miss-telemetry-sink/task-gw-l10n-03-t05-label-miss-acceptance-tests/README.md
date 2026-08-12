# task-gw-l10n-03-t05

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
Acceptance tests: valid event → row in table; invalid payload → soft 400; store unavailable → endpoint does not crash process.

## Code Facts
- `tests/test_gw_l10n_02_original_locale.py` — L10N acceptance test pattern (TestClient + in-memory stores)
- Backlog T05 scope verbatim in story source

## Acceptance / DoD
- Traces: AC1, AC2, AC3
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_l10n_03_label_miss_telemetry.py` (new)

## Verification commands
```bash
pytest tests/test_gw_l10n_03_label_miss_telemetry.py -q
pytest tests/ -q --ignore=tests/smoke --ignore=tests/integration
```
