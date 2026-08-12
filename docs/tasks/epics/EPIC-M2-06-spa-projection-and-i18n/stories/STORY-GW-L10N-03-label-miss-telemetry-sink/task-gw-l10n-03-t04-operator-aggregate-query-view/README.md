# task-gw-l10n-03-t04

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** data
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
Operator visibility: SQL view (e.g. `label_translation_misses_ranked`) or documented query — «топ / новые непереведённые ключи по locale».

## Code Facts
- `supabase/migrations/20260427_1615_spa_issues_dashboard_view.sql` — view precedent
- `docs/runtime-docs/appendix/reproject-issue-i18n-backfill-ru.md` — operator runbook pattern

## Acceptance / DoD
- Traces: AC4 (оператор-запрос)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- Supabase migration view (same or follow-up migration as T01)
- `docs/runtime-docs/appendix/label-translation-misses-operator-ru.md` (new) — SQL examples for operator

## Verification commands
```bash
# After T03 test insert: documented SQL returns expected rows
# sqlite: SELECT from view in test or manual query
```
