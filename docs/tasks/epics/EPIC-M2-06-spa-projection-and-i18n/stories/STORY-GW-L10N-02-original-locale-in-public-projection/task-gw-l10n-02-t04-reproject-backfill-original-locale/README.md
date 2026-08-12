# task-gw-l10n-02-t04

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** data
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
Расширить `scripts/reproject_issue_i18n.py` для пересчёта `original_locale`; обновить runbook appendix.

## Code Facts
- `scripts/reproject_issue_i18n.py` — GW-L10N-01 backfill
- `docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md` — out of scope → in scope

## Acceptance / DoD
- Traces: AC1 existing rows after backfill
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `scripts/reproject_issue_i18n.py`
- `docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md`

## Verification commands
```bash
`python3 scripts/reproject_issue_i18n.py --dry-run`
```
