## Task workspace — `task-m2-02-09-t03-story-store-institution-json-persistence`

- Story: [`../STORY-M2-02-09-institution-json-story-column-req43.md`](../STORY-M2-02-09-institution-json-story-column-req43.md)
- Decision Ref: [`../../../../../../requirements/43-institution-json-story-column.md`](../../../../../../requirements/43-institution-json-story-column.md) §2.2, §3.4–3.5

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000023`  
---

## Task: implement — `institution_json` persistence (all backends)

### Цель
Читать/писать `institution_json` в SQLite, Supabase и in-memory story repository; добавить колонку в bootstrap.

### Факты из кода
1. [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py) L83–94 — `_STORY_SELECT_COLUMNS` без `institution_json`; save ~L387+.
2. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) L44 — `_STORY_SELECT_FIELDS` без `institution_json`.
3. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) L30+ — `InMemoryStoryRepository` (нет отдельного `db_inmemory.py`).
4. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — нет `institution_json` (есть `narrative_summary_json` ~L50).
5. Паттерн JSON i18n: `narrative_summary_json` + `i18n_dict_to_json` / `i18n_dict_from_json` в [`narrative_i18n.py`](../../../../../../../src/core/domain/narrative_i18n.py).

### Gap / Проблема
`StoryRecord` с institution не переживает restart / Supabase roundtrip — колонка и маппинг отсутствуют.

### AC/DoD
- [ ] (P0) SQLite: `ALTER`/migration path + `institution_json` в SELECT/INSERT/UPSERT + `_story_record_from_sqlite_row`.
- [ ] (P0) Supabase: `_STORY_SELECT_FIELDS`, save/read mapping `institution_json` ↔ `narrative_institution`.
- [ ] (P0) `InMemoryStoryRepository`: roundtrip `narrative_institution` на `StoryRecord`.
- [ ] (P0) `000_full_init.sql`: `add column if not exists institution_json jsonb`.
- [ ] (P1) При необходимости — probe в `required_stories_*_columns_ready` (supabase health).

### Где менять код
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql)

### Out of scope
- Issue projection (T04).
- GPT UI.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_institution_intake.py -k sqlite
```
