## Task workspace — `task-m2-02-05-t01-gap-bootstrap-stories-geo-columns`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md#14-приоритетный-список-действий`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) (§1.4 GAP-07)

## Task: data — bootstrap `public.stories` geo columns parity

### Цель
Добавить в канонический bootstrap (и при необходимости в новую миграцию `supabase/migrations/` по соглашению имён `*_*.sql`) шесть geo-колонок, которые `_STORY_SELECT_FIELDS` и `_story_geo_supabase_fields()` уже ожидают в [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py).

### Факты из кода
1) Константа `_STORY_SELECT_FIELDS` (тот же файл, строки 28–34) включает `geo_normalized_label`, `geo_latitude`, `geo_longitude`, `geo_confidence`, `geo_provider`, `geo_cluster_tags_json`.
2) Функция `_story_geo_supabase_fields()` (строки 37–55) всегда возвращает эти ключи для merge в `save_story`.
3) В [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) до блока ALTER narrative (строки 7–27) geo-колонок нет — зафиксировано в анализе §1.3.

### Gap / Проблема
GAP-07: INSERT/SELECT через PostgREST падают, если колонок нет; `required_columns_ready()` возвращает `False`.

### AC/DoD
- [x] (P0) `000_full_init.sql` содержит `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` для всех шести geo-полей (типы как в анализе §1.4 «Нужный ALTER») либо эквивалент в отдельной миграции + ссылка в bootstrap README при split.
- [x] (P0) После применения схемы на тестовом проекте `required_columns_ready()` для `stories` не падает на отсутствии колонок (проверка live по [`tests/integration/supabase/`](../../../../../../tests/integration/supabase/) при наличии env).
- [x] (P1) Нет регрессии для существующих миграций: порядок применения документирован в комментарии к SQL.

### Где менять код
- [`doge-complaints-gateway/supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql)
- При необходимости: [`doge-complaints-gateway/supabase/migrations/`](../../../../../../supabase/migrations/) (новый файл, не редактировать уже закоммиченные снимки задним числом без явного решения).

### План выполнения
1. Сверить целевой DDL с анализом §1.4.
2. Внести правки в bootstrap и/или добавить миграцию.
3. Прогнать локальную проверку схемы (grep / live supabase по политике команды).

### Команды проверки
```bash
rg "geo_normalized_label" doge-complaints-gateway/supabase/bootstrap/000_full_init.sql doge-complaints-gateway/supabase/migrations/
cd doge-complaints-gateway && pytest -q tests/test_supabase_bootstrap_schema.py 2>/dev/null || true
```
