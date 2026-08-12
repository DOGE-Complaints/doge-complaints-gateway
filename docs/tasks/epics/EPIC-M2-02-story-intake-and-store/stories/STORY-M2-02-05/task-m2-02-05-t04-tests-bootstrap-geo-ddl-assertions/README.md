## Task workspace — `task-m2-02-05-t04-tests-bootstrap-geo-ddl-assertions`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`](../../../../../../analysis/implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md) (§5.1)

## Task: tests — строгие assert-ы DDL geo и дельта-миграции

### Цель
Закрыть оговорку верификации §5.1: текущие тесты проверяют **имена** geo-колонок в тексте `000_full_init.sql`, но не типы и не содержимое миграции.

### Факты из кода
1) [`tests/test_supabase_bootstrap_schema.py`](../../../../../../tests/test_supabase_bootstrap_schema.py) — функции `test_supabase_bootstrap_contains_stories_geo_columns_gap07` и родственные assert-ы по подстрокам в SQL.
2) Канонический DDL geo в [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) (блок `alter table ... geo_*`, см. файл).
3) Дельта: [`supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql`](../../../../../../supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql).

### Gap / Проблема
Регресс типов (`double precision` vs `text`) или удаление миграции не будет пойман только проверкой имён.

### AC/DoD
- [ ] (P0) Тест(ы) assert-ят подстроки типов для `geo_latitude`, `geo_longitude`, `geo_confidence` и строку `geo_cluster_tags_json text not null default '[]'` в тексте `000_full_init.sql` (как в §5.1 отчёта).
- [ ] (P0) Тест assert-ит существование файла миграции `20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql` и наличие в нём `geo_normalized_label` и `alter column embedding drop not null`.
- [ ] (P1) `pytest -q tests/test_supabase_bootstrap_schema.py` проходит.

### Где менять код
- [`doge-complaints-gateway/tests/test_supabase_bootstrap_schema.py`](../../../../../../tests/test_supabase_bootstrap_schema.py)

### План выполнения
1. Добавить функции из §5.1 отчёта (или эквивалент) без дублирования лишних assert-ов.
2. Прогнать pytest.

### Команды проверки
```bash
cd doge-complaints-gateway && pytest -q tests/test_supabase_bootstrap_schema.py
```
