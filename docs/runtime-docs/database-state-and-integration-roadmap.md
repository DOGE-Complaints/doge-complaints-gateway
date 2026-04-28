# База данных: текущее состояние и roadmap интеграции

## Контекст и управленческий вопрос

Ключевой вопрос:  
**какова фактическая зрелость persistence-контура сегодня, и что требуется для безопасного production-hardening без потери story-first контрактов?**

## Current state (implemented now)

### 1) Три режима persistence

Runtime поддерживает три взаимоисключающих backend-режима через `DB_BACKEND`.

| Режим | `DB_BACKEND` | Класс | Статус |
|---|---|---|---|
| In-memory | `in_memory` | `InMemory*` | Stable для unit/integration тестов и демо |
| SQLite | `sqlite` | `Sqlite*` в `db_sqlite.py` | Stable, авто-DDL (`ensure_schema`) |
| Supabase/PostgreSQL | `supabase` | `Supabase*` в `db_supabase.py` | Stable для runtime path + readiness probes (HTTP/PostgREST client) |

Источник выбора и wiring: `src/core/infrastructure/providers.py`.

### 2) Конфигурация per backend

Источник: `src/core/config/schema.py`.

- `in_memory`: запрещает `DATABASE_URL`/`SUPABASE_*`
- `sqlite`: требует `DATABASE_URL` c префиксом `sqlite:///`
- `supabase`: требует `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE` (`DATABASE_URL` не обязателен)

### 3) Реально персистируемые сущности

#### SQLite (`src/core/infrastructure/db_sqlite.py`)

`ensure_schema()` создает и использует:

- `stories`
- `idempotency_keys`
- `story_embeddings`
- `spa_issue_projections`
- `spa_issue_projection_embeddings`
- `issue_candidates`
- `review_audit_log`
- `issue_story_links`

#### Supabase (`src/core/infrastructure/db_supabase.py` + `supabase/migrations`)

Runtime stores реализованы для тех же групп данных:

- stories/idempotency
- story embeddings
- issue projections
- issue embeddings
- issue candidates
- review audit
- issue->stories linkage

Критичные миграции текущей волны:

- `20260427_1600_story_first_schema_parity.sql`
- `20260427_1615_spa_issues_dashboard_view.sql`
- `20260427_1645_process_linkage.sql`
- `20260427_1655_embedding_policy_version.sql`

### 4) Embeddings и policy versioning

В обоих SQL backend-ах embeddings сохраняются как JSON-vector + checksum + policy version:

- story embeddings: `embedding_policy_version = m2.story_embedding_policy.v1`
- issue embeddings: `embedding_policy_version = m2.issue_embedding_policy.v1`

Runtime-источники:

- `src/core/application/services.py`
- `src/core/application/issue_create.py`

### 5) Healthcheck и readiness

`SupabaseDatabase` предоставляет:

- `healthcheck()`
- `required_tables_ready()`
- `required_columns_ready()`
- `service_role_policy_probe()`

Их агрегированный результат публикуется в `GET /ready` через `db.checks`.

## Gaps / risks

- Для Supabase используется «новое соединение на операцию», connection pool отсутствует.
- Нет централизованного retry/backoff слоя для DB adapter операций.
- Применение Supabase миграций по-прежнему внешнее (CLI/операционный процесс), нет встроенного migration runner в Python runtime.
- Часть operational checks возвращает `bool` без детального structured error reason.

## Roadmap

### Ближайшие шаги

1. Добавить connection pooling для Supabase backend.
2. Добавить retry/backoff policy для transient DB ошибок.
3. Расширить readiness output диагностикой причин деградации (не только bool flags).

### Средний горизонт

4. Формализовать миграционный процесс (preflight + audit trail запуска миграций).
5. Добавить race-condition integration tests для idempotency/linkage под конкурентной нагрузкой.

### Долгосрочно

6. Ввести performance budget/observability для story-first pipeline на Supabase.
7. Подготовить migration governance для смены embedding-модели/размерности.

## Контрольные проверки

```bash
# Core regression
python3 -m pytest tests/ -q

# Story-first DB pipeline
python3 -m pytest tests/test_db_backed_pipeline_e2e.py tests/test_process_linkage_sqlite.py tests/test_embedding_policy_versioning.py -q

# Supabase integration (skip-safe без live env)
# requires SUPABASE_TEST_URL + SUPABASE_TEST_SERVICE_ROLE
python3 -m pytest tests/integration/supabase/test_supabase_live_smoke.py tests/integration/supabase/test_spa_projection_supabase_roundtrip.py -q
```
