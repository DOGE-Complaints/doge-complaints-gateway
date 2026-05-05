# 27. DOGEIssue — переименование и доменная идентичность

Дата: 2026-05-05  
Статус: решение принято — готово к задачированию  
Supersedes: раздел 2.1 документа `24-tallinn-issues-read-api.md` (предлагал `tallinn_issues_projections`)  
Зависит от: `09-spa-issue-projection.md`, `24-tallinn-issues-read-api.md` (read API — в силе, только имя таблицы меняется)

---

## 1. Контекст и мотивация

`SpaIssueProjection` — объект, который сейчас называется по технической роли («проекция для SPA»). Это название отражало то, что объект строился как рендер-артефакт для фронтенда. Фактически же это **первоклассная публичная гражданская запись** — итог кластеризации историй, несущий i18n, тип, метки, блокчейн-поля и полный жизненный цикл.

Решение: переименовать в `DOGEIssue` — имя, несущее платформенную идентичность, а не технический слой.

Таблица `spa_issue_projections` → `doge_issues`.  
`spa_issue_projection_embeddings` → `doge_issue_embeddings`.

**Почему не `tallinn_issues_projections` (предложение из doc 24):** слово "projections" сохраняло техническую коннотацию. `doge_issues` — это финальное имя доменного объекта, не слой хранения.

---

## 2. Инвентарь изменений (верифицирован по коду)

### 2.1 Python — классы и enum

| Файл | Было | Станет |
|------|------|--------|
| `src/core/projection/dto.py` | `SpaIssueProjection` | `DOGEIssue` |
| `src/core/projection/enums.py` | `SpaIssueStatus` | `DOGEIssueStatus` |
| `src/core/projection/enums.py` | `SpaIssueType` | `DOGEIssueType` |
| `src/core/projection/enums.py` | `SpaLabel` | `DOGEIssueLabel` |
| `src/core/projection/mapper.py` | `project_distinct_issue` → возвращает `SpaIssueProjection` | возвращает `DOGEIssue` |
| `src/core/projection/__init__.py` | экспортирует `SpaIssueProjection`, `SpaIssueStatus`, `SpaIssueType`, `SpaLabel` | обновить экспорты |

Значения enum-констант (`NEW`, `PUBLISHED`, `IMPROVEMENT`, `waste`, `infrastructure` и т.д.) **не меняются** — это доменный словарь, не часть имени класса.

### 2.2 Python — policy version strings

| Файл | Константа | Было | Станет |
|------|-----------|------|--------|
| `src/core/projection/policy.py` | `PROJECTION_POLICY_VERSION` | `"m2.spa_issue_projection.v1"` | `"m3.doge_issue_projection.v1"` |
| `src/core/application/issue_create.py` | `DERIVATION_POLICY_VERSION` | `"m2.spa_issue_derivation.v1"` | `"m3.doge_issue_derivation.v1"` |
| `src/core/application/issue_create.py` | `ISSUE_EMBEDDING_POLICY_VERSION` | `"m2.issue_embedding_policy.v1"` | `"m3.doge_issue_embedding_policy.v1"` |
| `src/core/projection/extraction_policy.py` | `EXTRACTION_POLICY_VERSION` | `"m2.story_to_projection_policy.v1"` | `"m3.story_to_doge_issue_policy.v1"` |

Версия меняется с `m2.*` на `m3.*` — это сигнал для процессинга: записи с `m2.*` версиями созданы до rename-миграции и читаются в обратной совместимости, новые записи получают `m3.*`.

### 2.3 DB-таблицы

| Backend | Было | Станет |
|---------|------|--------|
| SQLite DDL (`db_sqlite.py`, `ensure_schema()`) | `spa_issue_projections` | `doge_issues` |
| SQLite DDL | `spa_issue_projection_embeddings` | `doge_issue_embeddings` |
| Supabase bootstrap (`000_full_init.sql`) | `spa_issue_projections`, `spa_issue_projection_embeddings` | `doge_issues`, `doge_issue_embeddings` |
| Supabase migration | новый файл rename | см. раздел 3 |

Схема таблиц **не меняется** — только имена.

### 2.4 Protocol names в `issue_create.py`

`IssueProjectionStore`, `IssueProjectionEmbeddingStore`, `IssueProjectionReadStore` — имена остаются (они описывают роль, не домен). Только вхождения `SpaIssueProjection` в импортах и сигнатурах заменяются на `DOGEIssue`.

---

## 3. Миграция БД

### SQLite (dev / CI)

Таблицы создаются через `ensure_schema()` при каждом запуске — схема пересоздаётся. Достаточно заменить имена в DDL и SQL-запросах в `db_sqlite.py`.

### Supabase (production)

```sql
-- supabase/migrations/YYYYMMDD_rename_to_doge_issues.sql

ALTER TABLE public.spa_issue_projections RENAME TO doge_issues;
ALTER TABLE public.spa_issue_projection_embeddings RENAME TO doge_issue_embeddings;

-- Пересоздать RLS policies
DROP POLICY IF EXISTS projections_service_role_all ON public.doge_issues;
CREATE POLICY doge_issues_service_role_all
    ON public.doge_issues FOR ALL TO service_role
    USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS projection_embeddings_service_role_all ON public.doge_issue_embeddings;
CREATE POLICY doge_issue_embeddings_service_role_all
    ON public.doge_issue_embeddings FOR ALL TO service_role
    USING (true) WITH CHECK (true);
```

**Bootstrap (`000_full_init.sql`):** заменить все вхождения `spa_issue_projections` → `doge_issues`, `spa_issue_projection_embeddings` → `doge_issue_embeddings`.

---

## 4. Backward compatibility для существующих записей

Записи в `doge_issues` с `policy_version = "m2.spa_issue_derivation.v1"` — читаются без изменений. Поле `policy_version` — строка, не foreign key. Новые записи будут содержать `m3.doge_issue_derivation.v1`.

Read-store (`list_projections`, `get_projection`) не фильтрует по `policy_version` — возвращает все записи независимо от версии.

---

## 5. Влияние на doc 24 (read API)

`24-tallinn-issues-read-api.md` предлагал endpoint namespace `/tallinn/issues` и таблицу `tallinn_issues_projections`.

**Решение:**
- Таблица: `doge_issues` (этот документ)
- Endpoint namespace `/tallinn/issues` — **остаётся** (это публичный URL, не имя таблицы; менять нежелательно из-за связности с SPA)
- `IssueProjectionReadStore`, read handlers, CORS — из doc 24 в силе

---

## 6. Порядок реализации

| # | Действие | Файлы |
|---|----------|-------|
| 1 | Rename enum-классов в `enums.py` + обновить `__init__.py` | `projection/enums.py`, `projection/__init__.py` |
| 2 | Rename `SpaIssueProjection` → `DOGEIssue` в `dto.py`, обновить `mapper.py` | `projection/dto.py`, `projection/mapper.py` |
| 3 | Обновить policy version strings во всех 4 файлах | `policy.py`, `extraction_policy.py`, `issue_create.py` |
| 4 | Rename таблиц в SQLite DDL + SQL-запросах | `db_sqlite.py` |
| 5 | Rename таблиц в Supabase bootstrap | `000_full_init.sql` |
| 6 | Supabase migration файл | `supabase/migrations/YYYYMMDD_rename_to_doge_issues.sql` |
| 7 | Обновить все тест-файлы, импортирующие `SpaIssueProjection`, `SpaIssueStatus`, etc. | `tests/` |
| 8 | Запустить полный test suite, smoke write-path | все тесты |

**Шаги 4–5 — самые опасные:** затрагивают write-path. Делать вместе с шагом 6, проверить `POST /intake/stories` сразу после.

---

## 7. Acceptance criteria

**AC-27-1:** `SpaIssueProjection`, `SpaIssueStatus`, `SpaIssueType`, `SpaLabel` не встречаются в `src/` (кроме комментариев с историей).

**AC-27-2:** Таблицы `spa_issue_projections`, `spa_issue_projection_embeddings` не встречаются в `src/` и bootstrap SQL.

**AC-27-3:** `POST /intake/stories` с `CLUSTER_MIN_SIZE=1` создаёт запись в `doge_issues` без ошибок.

**AC-27-4:** Новые записи содержат `policy_version = "m3.doge_issue_derivation.v1"`.

**AC-27-5:** Все 177 тестов проходят.
