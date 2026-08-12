## Task workspace — `task-m2-02-05-t02-gap-bootstrap-embeddings-not-null`

- Story: [`../STORY-M2-02-05-supabase-bootstrap-schema-parity.md`](../STORY-M2-02-05-supabase-bootstrap-schema-parity.md)
- Decision Ref: [`../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) (§3, §5, GAP-08; варианты A/B в §3)

## Task: data — story/issue embedding column vs gateway writes

### Цель
Устранить GAP-08: в bootstrap объявлено `embedding vector(8) NOT NULL` без default, а `SupabaseStoryEmbeddingStore.save_story_embedding()` и `SupabaseIssueProjectionEmbeddingStore` не передают колонку `embedding` в JSON тела запросов (см. [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) около строк 435–457 и 496–535).

### Факты из кода
1) `save_story_embedding` POST в `/rest/v1/story_embeddings` с полями `story_id`, `model_name`, `embedding_vector_json`, `source_checksum`, `embedding_policy_version`, `created_at` — без `embedding`.
2) Bootstrap `create table ... story_embeddings` и `doge_issue_embeddings` задают `embedding vector(8) not null` ([`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) строки 35–41 и 59–64 в текущей версии файла).
3) Анализ рекомендует вариант A (`ALTER ... DROP NOT NULL`) или B (`DROP COLUMN`) — выбор фиксируется здесь в коммите (одна строка Decision в PR).

### Gap / Проблема
INSERT в PostgREST возвращает 400 при NOT NULL violation на свежем bootstrap.

### AC/DoD
- [x] (P0) Зафиксирован и реализован **один** вариант: **A (nullable)** — колонка `embedding` сохранена для возможного pgvector-use, NOT NULL снят; см. анализ §3.
- [x] (P0) Bootstrap и/или миграция отражают выбранный вариант; новый INSERT из кода проходит smoke-level проверку.
- [x] (P1) Документация в [`supabase/bootstrap/README.md`](../../../../../../supabase/bootstrap/README.md) при необходимости уточняет роль `embedding_vector_json` vs `embedding`.

### Где менять код
- [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql)
- [`supabase/migrations/`](../../../../../../supabase/migrations/) при необходимости отдельного forward-only шага.

### План выполнения
1. Принять решение A vs B (ссылка на обсуждение или на строку анализа).
2. Правка DDL + проверка совместимости с существующими миграциями `20260427_*`.
3. Минимальный тест или ручной verify через integration test bucket при наличии credentials.

### Команды проверки
```bash
rg "story_embeddings|doge_issue_embeddings" doge-complaints-gateway/supabase/bootstrap/000_full_init.sql
cd doge-complaints-gateway && pytest -q tests/integration/supabase/test_supabase_live_story_embedding_roundtrip.py 2>/dev/null || true
```
