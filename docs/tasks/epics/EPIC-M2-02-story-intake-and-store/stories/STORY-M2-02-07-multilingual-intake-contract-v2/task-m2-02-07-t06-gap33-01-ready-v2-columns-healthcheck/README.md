## Task workspace — `task-m2-02-07-t06-gap33-01-ready-v2-columns-healthcheck`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: [`../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md`](../../../../../../analysis/audit-req33-multilingual-intake-v2-2026-05-15.md) GAP-33-01

## Task: fix — wire REQ-33 v2 columns into `/ready` healthcheck

### Цель
Подключить `required_stories_intake_v2_columns_ready()` к Supabase `db_checks`, чтобы `/ready` не давал ложный `columns: true` при отсутствии миграции `20260513_*`.

### Факты из кода
1. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — метод `required_stories_intake_v2_columns_ready()` (L329–344) существует, но не вызывается.
2. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — `db_checks["columns"]` = `required_columns_ready()` (legacy `narrative_title_hint` only).

### Gap / Проблема
**GAP-33-01 (P0):** без v2-колонок на hosted DB healthcheck зелёный, первый `POST /intake/stories` падает на записи.

### AC/DoD
- [x] (P0) В `build_api_dependencies` для Supabase добавлен ключ `columns_v2` → `required_stories_intake_v2_columns_ready()`.
- [x] (P0) `db_ready = all(db_checks.values())` учитывает `columns_v2`.
- [x] (P1) `GET /ready` при `DB_BACKEND=supabase` отдаёт `checks.columns_v2` (live test или shape test).

### Где менять код
- [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py)
- [`tests/integration/supabase/test_supabase_ready_endpoint_shape.py`](../../../../../../../tests/integration/supabase/test_supabase_ready_endpoint_shape.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/integration/supabase/test_supabase_ready_endpoint_shape.py -q --tb=short
```
