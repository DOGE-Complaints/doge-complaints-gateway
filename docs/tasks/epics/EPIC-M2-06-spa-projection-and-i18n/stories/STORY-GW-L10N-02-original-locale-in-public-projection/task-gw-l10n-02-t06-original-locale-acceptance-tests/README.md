# task-gw-l10n-02-t06

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
Новый `tests/test_gw_l10n_02_original_locale.py`: mono `['et']`, mixed `['et','ru']`, list+get handlers; suite green.

## Code Facts
- Новый `tests/test_gw_l10n_02_original_locale.py`
- REQ-24 handlers — list/get Tallinn issues

## Acceptance / DoD
- Traces: AC1–AC3, AC5
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_l10n_02_original_locale.py`

## Verification commands
```bash
`cd doge-complaints-gateway && python3 -m pytest tests/test_gw_l10n_02_original_locale.py -q`
```
