## Task workspace — `task-m2-02-05-bootstrap-schema-primary`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md)
- Skill declared: `python-pro`

## Task: orchestrate — bootstrap schema parity story gates

### Цель
Зафиксировать порядок закрытия GAP-07/08/09 по анализу data-model vs bootstrap и acceptance для STORY-M2-02-05 без расхождения с `gateway-active-packages` очередью.

### Факты из кода / артефактов
1) Анализ §14 перечисляет P0: geo-колонки в `stories`, `embedding NOT NULL` на embedding-таблицах; P1: JSONB read bug в `db_supabase.py`.
2) `SupabaseDatabase.required_columns_ready()` в [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) запрашивает geo-колонки для `stories` — при их отсутствии в БД проверка возвращает `False`.
3) Активный gateway-пакет после внедрения — `doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml` (см. `gateway-active-package.current.yaml`).

### Gap / Проблема
Без выровненного bootstrap и правок кода свежая Supabase-схема остаётся несовместимой с PostgREST-клиентом gateway (симптомы в анализе §1.4, §3, §6).

### AC/DoD
- [x] (P0) Выполнены вложенные таски T01–T03 в порядке очереди или зафиксировано явное блокирование с ссылкой на decision.
- [x] (P0) `gateway_resolve_queue.py --verify` для `pkg-000011-20260508-m2-02-bootstrap-schema-parity.yaml` завершается успешно.
- [x] (P1) Обновлён story-level acceptance (`acceptance-verification-STORY-M2-02-05.md`, `BULLRUN-PHASE-LOG.md`, story gate в родительской папке story).

### Где менять код
- По результатам дочерних тасков: [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql), [`supabase/migrations/`](../../../../../../supabase/migrations/), [`src/core/infrastructure/db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py).

### План выполнения
1. Выполнить T01 (geo DDL).
2. Выполнить T02 (embedding constraint vs код).
3. Выполнить T03 (JSONB read).
4. Прогнать verify и pytest согласно дочерним README.

### Команды проверки
```bash
cd /Users/eslinko/Development/DOGEstonia && python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && pytest -q tests/integration/supabase/test_supabase_dotenv_connectivity.py tests/test_supabase_bootstrap_schema.py 2>/dev/null || true
```
