# task-gw-l10n-02-t02

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
Добавить `original_locale` в `DOGEIssue` и `to_public_dict()`; маппинг в `project_distinct_issue`; опускать поле при пустом списке.

## Code Facts
- `src/core/projection/dto.py:25-48` — `DOGEIssue.to_public_dict()` без `original_locale`
- `src/core/projection/mapper.py:20-58` — `project_distinct_issue`

## Acceptance / DoD
- Traces: AC1; AC3
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `dto.py` — поле + `to_public_dict`
- `mapper.py` — map from `ProjectionInput.original_locale`

## Verification commands
```bash
pytest T06; inspect `to_public_dict()` output
```
