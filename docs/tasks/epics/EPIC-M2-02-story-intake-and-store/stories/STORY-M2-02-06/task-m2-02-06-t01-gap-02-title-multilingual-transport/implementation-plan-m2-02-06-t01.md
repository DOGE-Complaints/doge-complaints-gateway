# План реализации — TASK-M2-02-06-T01 (GAP-02)

## Фаза 0 — Conflict-scan
- Проверено отсутствие противоречивых задач по `narrative_title_hint` в Done.

## Фаза 1 — Контракт intake
- Файл: `src/core/intake/contracts.py` — поля `title_hint_et|ru|en` на `Narrative`; парсер в `parse_story_intake_request`.

## Фаза 2 — Домен и сервис
- Файл: `src/core/domain/contracts.py` — `narrative_title_hint_et|ru|en`.
- Файл: `src/core/application/services.py` — маппинг в `StoryRecord`.

## Фаза 3 — Персистенция
- `db_supabase.py`, `db_sqlite.py` — select/insert/row mapping.
- `supabase/bootstrap/000_full_init.sql`, `supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql`.

## Фаза 4 — GPT / тесты
- `GPT UI/instructions/api-orchestrator.md` — §5.2.1.
- `tests/test_story_intake_live_context_not_on_record.py`, `tests/test_supabase_bootstrap_schema.py`.

## Критерии готовности фазы 4
- `cd doge-complaints-gateway && python3 -m pytest -q` — успех.
