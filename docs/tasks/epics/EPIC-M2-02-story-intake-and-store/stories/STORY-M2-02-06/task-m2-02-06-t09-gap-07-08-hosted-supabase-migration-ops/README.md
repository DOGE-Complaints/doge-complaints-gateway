## Task workspace — `task-m2-02-06-t09-gap-07-08-hosted-supabase-migration-ops`

- Story: [`../STORY-M2-02-06-data-model-registry-section-16-followup.md`](../STORY-M2-02-06-data-model-registry-section-16-followup.md)
- Decision Ref: [`../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md`](../../../../../../analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md) — **«Незакрытые хвосты — финальный прогон»**; §16 **GAP-07**, **GAP-08**

## Task: data — применение bootstrap-гео и nullable embedding на hosted Supabase

### Цель
Свести **hosted** схему Supabase с репозиторием: geo-колонки на `public.stories` и `embedding drop not null` на `story_embeddings` / `doge_issue_embeddings`, как в [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) и дельте [`supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql`](../../../../../../../supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql).

### Факты из кода
1. `required_columns_ready()` и `save_story` ожидают geo-колонки — см. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py).
2. Bootstrap-тесты в [`tests/test_supabase_bootstrap_schema.py`](../../../../../../../tests/test_supabase_bootstrap_schema.py) валидируют репозиторий как SSOT для **файлов** SQL; hosted может отставать.

### Gap / Проблема
«Код закрыт» ≠ «remote БД мигрирована»; live pytest может skip/fail до прогона миграций.

### AC/DoD
- [ ] (P0) Зафиксирован чеклист ops в этой папке (`implementation-notes-hosted-migrations.md` или раздел в README): шаги `supabase db push` / ручной SQL для целевого проекта.
- [ ] (P0) Явная ссылка на файлы миграций в репозитории (имена без усечения).
- [ ] (P2) Follow-up (не блокер таска): CI `supabase db diff --linked` — вынести в отдельную story при необходимости.

### Где менять
- Операции вне git или короткий ops-док в папке таска; **без** обязательных правок Python в рамках этого таска.

### Команды проверки (после применения на hosted)
```bash
cd doge-complaints-gateway && pytest -q tests/integration/supabase/ -m live
```
(только при настроенных live creds.)
