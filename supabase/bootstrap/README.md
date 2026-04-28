# Supabase Full Bootstrap (fresh install)

Этот каталог содержит единый bootstrap-скрипт для инициализации БД с нуля.

## Файл

- `000_full_init.sql` — полный idempotent setup:
  - extension `vector`
  - core таблицы (`stories`, `idempotency_keys`, `story_embeddings`, `spa_issue_projections`, `spa_issue_projection_embeddings`)
  - story-first расширения (`narrative_*`, `embedding_vector_json`, `embedding_policy_version`)
  - process/linkage таблицы (`issue_candidates`, `review_audit_log`, `issue_story_links`)
  - view `issues_dashboard`
  - RLS + `service_role` policies (включая hardened_plus для новых таблиц)
  - grant на `issues_dashboard` для `anon`, `authenticated`

## Как запускать

### Вариант 1: Supabase SQL Editor
1. Открыть SQL Editor в проекте Supabase.
2. Вставить содержимое `supabase/bootstrap/000_full_init.sql`.
3. Выполнить скрипт целиком.

### Вариант 2: Supabase CLI (psql)
```bash
psql "$DATABASE_URL" -f supabase/bootstrap/000_full_init.sql
```

## Важное правило использования

- Для **fresh install** использовать этот bootstrap-файл.
- Для уже развернутой БД с историей миграций продолжать использовать `supabase/migrations/*.sql` как дельты.
