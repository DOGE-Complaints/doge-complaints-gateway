# task-gw-l10n-02-t03

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
В `create_manual_issue` вычислять `original_locale` из языков историй по запрошенным `story_ids`.

## Code Facts
- `src/core/application/issue_create.py:354+` — `create_manual_issue`

## Acceptance / DoD
- Traces: AC1 manual path
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `issue_create.py` — manual path: load stories by `story_ids`, collect `narrative_language`

## Verification commands
```bash
pytest manual create test (T06)
```
