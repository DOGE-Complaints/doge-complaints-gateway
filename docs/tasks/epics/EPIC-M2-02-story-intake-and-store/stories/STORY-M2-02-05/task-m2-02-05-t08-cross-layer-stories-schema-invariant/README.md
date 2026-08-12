## Task workspace — `task-m2-02-05-t08-cross-layer-stories-schema-invariant`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.6); продуктовый контекст: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md)

## Task: tests — MVP offline-инвариант колонок `stories` (код vs bootstrap)

### Цель
Системный gap §5.6: несколько источников правды о колонках `public.stories` (`_STORY_SELECT_FIELDS`, `required_columns_ready`, `save_story` payload, `000_full_init.sql`). Ввести **минимальный** offline-тест, который поймает рассинхрон имени колонки (класс ошибки GAP-07).

### Факты из кода
1) Список select-полей: [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) — `_STORY_SELECT_FIELDS` (строки ~39–45) и `required_columns_ready()` (строки ~238+).
2) DDL: [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) — `create table` / `alter table` для `public.stories`.

### Gap / Проблема
Нет автоматической сверки множества имён колонок stories между SQL-текстом и константой Python.

### AC/DoD
- [ ] (P0) Один тест (новый файл рядом с `test_supabase_bootstrap_schema.py` или расширение него), который:
  - извлекает имена колонок stories из `_STORY_SELECT_FIELDS` (split по запятой, trim) **или** дублирует эталонный frozenset рядом с тестом с комментарием «sync with _STORY_SELECT_FIELDS»;
  - assert-ит каждое имя как подстроку в `000_full_init.sql` в блоке `public.stories` / последующих `alter table ... stories` (минимально: grep по файлу целиком допустим для MVP).
- [ ] (P1) Ссылка в комментарии на `req-cross-layer-contract-testing.md` как на roadmap полного C-xx набора.

### Где менять код
- [`doge-complaints-gateway/tests/`](../../../../../../tests/)
- Чтение только: [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py), [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql)

### План выполнения
1. Выбрать стратегию парсинга (простой split vs ast SQL — MVP = split + оговорки в тесте).
2. Реализовать тест и pytest.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_supabase_bootstrap_schema.py tests/test_stories_schema_cross_layer_invariant.py 2>/dev/null || pytest -q tests/test_supabase_bootstrap_schema.py
```
