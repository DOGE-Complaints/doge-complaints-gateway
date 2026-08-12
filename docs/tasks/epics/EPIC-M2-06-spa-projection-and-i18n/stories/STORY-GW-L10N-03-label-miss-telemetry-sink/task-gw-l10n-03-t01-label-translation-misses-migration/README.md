# task-gw-l10n-03-t01

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** data
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
DDL таблицы `label_translation_misses`: агрегат `(label_key, locale)` + `count` + `last_seen_at`; PK/unique и индекс для operator queries.

## Code Facts
- `supabase/migrations/20260523_1200_req42_story_signals.sql` — migration + RLS pattern
- `src/core/infrastructure/db_sqlite.py:165+` — `ensure_schema()` CREATE TABLE parity
- `grep telemetry` по `openapi.yaml` / `API_REFERENCE.md` → 0 (таблицы нет)

## Acceptance / DoD
- Traces: AC2 (отдельная таблица для фиксации)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `supabase/migrations/YYYYMMDD_HHMM_gw_l10n_03_label_translation_misses.sql`
- `src/core/infrastructure/db_sqlite.py` — `ensure_schema()` block for `label_translation_misses`

## Verification commands
```bash
# Apply migration (supabase) or sqlite ensure_schema in test bootstrap
pytest tests/ -q -k label_miss --ignore=tests/smoke --ignore=tests/integration  # after T02/T05
```
