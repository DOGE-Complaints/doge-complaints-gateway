## Task workspace — `task-m2-02-07-t04-persistence-stories-v2-columns`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: REQ-33 §3–§4

## Task: implement — persistence columns for v2 narrative fields

### Цель
Сохранять v2 dict-поля и session_language в SQLite/Supabase; миграция DDL согласована с `StoryRecord` после T02.

### Факты из кода
1. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — колонки `narrative_title_hint`, `narrative_title_hint_et/ru/en`.
2. [`supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql`](../../../../../../../supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql) — расширения transitional title_hint_*.
3. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py), [`db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) — read/write `StoryRecord`.

### Gap / Проблема
Без новых колонок/JSONB v2 поля не переживут persist roundtrip.

### AC/DoD
- [ ] (P0) Новая migration: колонки под `narrative_title`, `narrative_description`, `narrative_summary`, `narrative_session_language` (JSONB/text по принятому в репо паттерну).
- [ ] (P0) `save_story` / `get_story` читают и пишут v2 поля; `submitter_identity_issuer` NOT NULL на уровне приложения.
- [ ] (P1) Bootstrap/parity policy репозитория соблюдена (touch `000_full_init` только если принято для greenfield).

### Где менять код
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- `supabase/migrations/20260513_*_m2_02_07_intake_v2_narrative.sql` (новый файл)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_supabase_bootstrap_schema.py tests/integration/supabase/test_supabase_live_story_roundtrip.py -q --tb=short -m "not integration" 2>/dev/null || python3 -m pytest tests/test_supabase_bootstrap_schema.py -q --tb=short
```
