# Story Persistence Model — Supabase

**Дата:** 2026-05-20  
**Источники:** `supabase/bootstrap/000_full_init.sql`, `src/core/infrastructure/db_supabase.py`, `src/core/domain/contracts.py`, `src/core/application/services.py`

Документ описывает все таблицы и поля, в которые история сохраняется или с которыми она связана. Структура — по слоям: от основной записи к производным.

---

## Обзор: таблицы, связанные с историей

```
stories                     ← основная запись, все поля из intake
  ├── idempotency_keys      ← dedup: intake_key → story_id
  ├── story_drafts          ← ephemeral intake JSON stash (GW-DRAFT-01; TTL via expires_at)
  ├── story_embeddings      ← векторный индекс (8-dim, deterministic-baseline-v1)
  ├── story_signals         ← кэш extraction_policy → signals_json
  └── cluster_memberships   ← lens → cluster_id для аналитики

issue_candidates            ← кандидат на промоцию (state machine)
  ├── story_ids_json        ← (внутри записи) список историй кластера
  └── review_audit_log      ← история решений по кандидату

issue_story_links           ← финальная связь story ↔ issue
doge_issues                 ← финальный read-model (payload_json = DOGEIssue)
  └── doge_issue_embeddings ← векторный индекс issue
```

RLS: все таблицы — `service_role` only (полные права). `doge_issues` также читаем через view `issues_dashboard` (anon/authenticated).

---

## Слой 1: `public.stories` — основная запись истории

### Идентификация

| Колонка | Тип | Обязательно | Описание |
|---------|-----|-------------|---------|
| `story_id` | `text PK` | да | UUID4, генерируется сервером при intake |
| `schema_version` | `text NOT NULL` | да | Версия схемы входящего запроса (`m2.story_intake_envelope.v2`) |
| `lifecycle_status` | `text NOT NULL` | да | Текущее состояние в pipeline (см. ниже) |
| `created_at` | `timestamptz NOT NULL` | да | UTC, момент создания записи |
| `updated_at` | `timestamptz NOT NULL` | да | UTC, обновляется при каждом `save_story()` и `update_lifecycle_status()` |

**`lifecycle_status` — допустимые значения:**

| Значение | Условие перехода |
|----------|-----------------|
| `accepted` | Создана, но `narrative_v2_complete()` = False |
| `partial_ready` | `narrative_v2_complete()` = False (все обязательные поля заполнены?) |
| `ready_for_profile` | `narrative_v2_complete()` = True — история попадает в очередь кластеризации |
| `clustered` | Кластер промотирован в issue — история помечена как обработанная (идемпотентность cron) |

Переход выполняется в `services.py:advance_story_readiness()` сразу после `save_story()`.

Source: `domain/contracts.py:20-25`, `services.py:281-338`

---

### Нарратив

| Колонка | Тип | Обязательно | Описание |
|---------|-----|-------------|---------|
| `narrative_original_text` | `text NOT NULL` | да | Оригинальный текст истории от пользователя (stripped) |
| `narrative_language` | `text` | нет | Язык `original_text`: `et`, `ru`, `en` |
| `narrative_session_language` | `text` | нет | Язык интерфейса сессии (может отличаться от `language`) |
| `narrative_title_json` | `jsonb` | нет | Многоязычный заголовок: `{"et": "...", "ru": "...", "en": "..."}` |
| `narrative_description_json` | `jsonb` | нет | Многоязычное описание: `{"et": "...", "ru": "...", "en": "..."}` |
| `narrative_summary_json` | `text` (JSON) | нет | Многоязычное резюме (опционально, тот же формат dict) |
| `institution_json` | `jsonb` | нет | Многоязычное ведомство из `narrative.institution` (REQ-43): `{"et": "...", "ru": "...", "en": "..."}` |
| `narrative_consistency_notes` | `text` | нет | Заметки о согласованности нарратива из `live_story_context.consistency_notes` |
| `narrative_canonical_type` | `text` | нет | Тип из GPT: `complaint`, `observation`, `system_bug`, `absurdity` (без enum-валидации при intake) |
| `narrative_canonical_labels_json` | `text NOT NULL default '[]'` | да | JSON-массив строк: canonical labels из GPT, нормализованные (`.strip().lower()`, deduped) |

**Легаси `narrative_title_hint*` (REQ-46 §2.4, STORY-M2-02-12 T11–T13):** колонки удалены из bootstrap и persistence; hosted purge — `supabase/migrations/20260603_1200_req46_title_hint_test_purge_and_column_drop.sql`. Чтение/запись title — только через `narrative_title_json`.

---

### Submitter / идентификация пользователя

| Колонка | Тип | Обязательно | Описание |
|---------|-----|-------------|---------|
| `submitter_external_user_id` | `text NOT NULL` | да | Внешний ID пользователя (напр. `telegram:123456789`) |
| `submitter_identity_issuer` | `text NOT NULL` | да | Источник идентификатора (напр. `telegram`) |

---

### Origin / источник запроса

| Колонка | Тип | Описание |
|---------|-----|---------|
| `origin_source` | `text` | Наименование источника (напр. `telegram_bot`) |
| `origin_conversation_id` | `text` | ID разговора в системе-источнике |
| `origin_tool_call_id` | `text` | ID tool call (при интеграции с GPT function calling) |

---

### Privacy

| Колонка | Тип | Default | Описание |
|---------|-----|---------|---------|
| `privacy_contains_pii` | `boolean NOT NULL` | `false` | Флаг наличия персональных данных. Если `true` — `original_text` редактируется в логах |
| `privacy_redaction_requested` | `boolean NOT NULL` | `false` | Запрос на удаление данных пользователем |

---

### Geo — нормализованная гео-позиция

Заполняется сервисом `geo_service.resolve_for_story(location_query)` при intake, если `location_query` не пустой и `GEO_SERVICE_ENABLED=true`. Если geo не разрешён — все поля `NULL`.

| Колонка | Тип | Описание |
|---------|-----|---------|
| `geo_normalized_label` | `text` | Нормализованный адресный label от geo-провайдера |
| `geo_latitude` | `double precision` | Широта |
| `geo_longitude` | `double precision` | Долгота |
| `geo_confidence` | `double precision` | Уверенность geo-провайдера (0.0–1.0) |
| `geo_provider` | `text` | Провайдер, разрешивший адрес |
| `geo_cluster_tags_json` | `text NOT NULL default '[]'` | JSON-массив тегов кластеризации от провайдера |
| `geo_admin_district` | `text` | Административный район (напр. `Kesklinn`) |
| `geo_admin_settlement` | `text` | Населённый пункт (напр. `tallinn`) |
| `geo_admin_region` | `text` | Регион (напр. `harju`) |
| `geo_admin_country` | `text` | Страна (напр. `ee`) |

Geo-поля используются в:
- `CLUSTER_GEO_FILTER` — суффикс cluster_key (`geo:{level}:{token}`)
- `CLUSTER_GEO_SCOPE` — gate при intake (reject если вне scope)
- `GET /tallinn/issues?geo_district=...` — фильтрация в read API через `payload_json`

Source: `domain/contracts.py:27-42`, `db_supabase.py:96-122`

---

## Слой 2: `public.idempotency_keys` — дедупликация intake

```sql
key       text PK            -- Idempotency-Key header или SHA-256(raw body)
story_id  text NOT NULL      -- FK → stories.story_id ON DELETE CASCADE
created_at timestamptz       -- UTC
```

**Поведение:** при повторном intake с тем же ключом — возвращается существующая история, новая не создаётся.

**Генерация ключа:**
- Заголовок `Idempotency-Key` присутствует и непустой → используется как есть
- Заголовок отсутствует → `sha256(raw_body_bytes).hexdigest()`

Source: `api/idempotency.py`, `domain/contracts.py:91-105`, `db_supabase.py:519-556`

---

## Слой 3: `public.story_embeddings` — векторный индекс истории

```sql
embedding_id           bigint GENERATED ALWAYS AS IDENTITY PK
story_id               text NOT NULL         -- FK → stories.story_id ON DELETE CASCADE
model_name             text NOT NULL         -- "deterministic-baseline-v1"
embedding              vector(8)             -- pgvector колонка; nullable (GAP-08 variant A)
embedding_vector_json  text                  -- JSON-массив 8 float; основной persist-путь
source_checksum        text NOT NULL         -- SHA-256 canonical source string
embedding_policy_version text NOT NULL       -- "m2.story_embedding_policy.v1"
created_at             timestamptz           -- UTC
```

**Политика сохранения (GAP-08 variant A):** Gateway пишет только в `embedding_vector_json` (не в pgvector-колонку). Колонка `embedding` nullable — pgvector-индексация через отдельный job не входит в текущий runtime.

**Что является источником для embedding (`_canonical_story_embedding_source`):**

```
story_id={story_id}|lang={language}|title={primary_title}|type={canonical_type}|labels={labels_csv}|text={original_text}
```

- `primary_title` — выбирается по `session_language` → `language` → первый доступный из `et/ru/en`
- `text` — редактируется при `privacy_contains_pii=true`
- `labels` — CSV из `narrative_canonical_labels`

Вектор — детерминированный baseline: SHA-256 строки → 8 float в диапазоне `[0.0, 1.0]` из первых 16 байт дайджеста. Не семантический — используется как structural fingerprint.

**Индекс:** `idx_story_embeddings_story_id` на `story_id`

Source: `services.py:412-438`, `db_supabase.py:559-586`

---

## Слой 4: `public.story_signals` — кэш clustering signals

```sql
story_id           text NOT NULL  -- FK → stories.story_id ON DELETE CASCADE
extraction_policy  text NOT NULL  -- ключ политики (напр. "m3.doge_issue_derivation.v1")
signals_json       jsonb NOT NULL -- dict: SignalDimension.value → значение
extracted_at       timestamptz    -- UTC, момент вычисления
PRIMARY KEY (story_id, extraction_policy)
```

**Назначение:** signals вычисляются при первом `process_story()` и персистируются. При повторном вызове — читаются из кэша (ADR-CE-006). Предотвращает повторное вычисление для всех `READY_FOR_PROFILE` историй при каждом тике cron.

**Формат `signals_json`:**

```json
{
  "civic_domain":          "infrastructure",
  "failure_pattern":       "infrastructure_failure",
  "civic_weight":          "systemic",
  "desired_outcome":       "fix",
  "affected_group":        "residents",
  "geographic_district":   "kesklinn",
  "canonical_type":        "complaint"
}
```

Ключи — значения `SignalDimension` enum (6 civic осей + `canonical_type`).

**Индекс:** `idx_story_signals_policy` на `extraction_policy`

Source: `domain/contracts.py:108-128`, `db_supabase.py:927-963`

---

## Слой 5: `public.cluster_memberships` — аналитическая таблица lens→cluster

```sql
story_id    text NOT NULL  -- FK → stories.story_id ON DELETE CASCADE
lens        text NOT NULL  -- ClusterLens value (напр. "civic_domain_micro")
cluster_id  text NOT NULL  -- SHA-256 cluster key
computed_at timestamptz    -- UTC
PRIMARY KEY (story_id, lens)
```

**Назначение:** аналитический read-side — сохраняет результат кластеризации per lens. Используется для drill-down запросов. Не блокирует основной pipeline (ADR-CE-008): запись выполняется after issue creation; при ошибке записи — логируется, не падает.

**Активные линзы (REQ-34):**

| Линза | Cluster key суффикс |
|-------|-------------------|
| `civic_domain_micro` | `civic_domain:{value}` |
| `failure_pattern_micro` | `failure_pattern:{value}` |
| `civic_weight_systemic` | `civic_weight:{value}` |
| `desired_outcome_local` | `desired_outcome:{value}` |
| `affected_group_local` | `affected_group:{value}` |
| `geographic_district_micro` | `geographic_district:{value}` |

**Индекс:** `idx_cluster_memberships_cluster` на `cluster_id`

Source: `domain/contracts.py:140-148`, `db_supabase.py:966-997`

---

## Слой 6: `public.issue_candidates` — кандидат на промоцию

Создаётся при первом `process_story()` для кластера. Переходит через state machine перед созданием issue.

```sql
candidate_id    text PK            -- UUID4 (будущий issue_id)
status          text NOT NULL      -- IssueCandidateStatus (см. ниже)
cluster_id      text NOT NULL      -- SHA-256 cluster key
story_ids_json  jsonb NOT NULL     -- JSON-массив story_id всех членов кластера
readiness_score integer NOT NULL   -- 0–100, вычисленный score кластера
title           text NOT NULL      -- заголовок (строка, legacy)
updated_at      timestamptz        -- UTC
```

**`status` — состояния:**

| Значение | Описание |
|----------|---------|
| `draft` | Кандидат создан, ещё не готов |
| `ready_for_review` | Прошёл promotion gates |
| `in_review` | На ручной проверке |
| `promoted` | Промотирован в `doge_issues` |
| `rejected` | Отклонён (story lifecycle может быть откачен) |

Source: `promotion/types.py:8-28`, `db_supabase.py:741-846`

---

## Слой 7: `public.review_audit_log` — история решений

```sql
audit_id              bigserial PK      -- auto-increment
candidate_id          text NOT NULL     -- ссылка на issue_candidates.candidate_id
actor                 text NOT NULL     -- кто принял решение
decision              text NOT NULL     -- "approve" | "reject"
rationale             text NOT NULL     -- обоснование
related_cluster_id    text NOT NULL     -- cluster_id на момент решения
related_story_ids_json jsonb NOT NULL   -- снимок story_ids на момент решения
created_at            timestamptz       -- UTC
```

**Индекс:** `idx_review_audit_candidate` на `candidate_id`

Source: `promotion/types.py:39-45`, `db_supabase.py:849-892`

---

## Слой 8: `public.issue_story_links` — финальная связь story↔issue

```sql
issue_id    text NOT NULL     -- FK не объявлен, фактически → doge_issues.issue_id
cluster_id  text NOT NULL     -- cluster_id, при котором создан issue
story_id    text NOT NULL     -- FK → stories.story_id (implicit)
created_at  timestamptz       -- UTC
PRIMARY KEY (issue_id, story_id)
```

Заполняется в `IssueCreateService` после успешного `save_projection()`. Идемпотентно: `on_conflict (issue_id, story_id)` → ignore.

**Индексы:** `idx_issue_story_links_issue` (issue_id), `idx_issue_story_links_story` (story_id)

Source: `db_supabase.py:895-924`

---

## Слой 9: `public.doge_issues` — read-model issue

```sql
issue_id      text PK            -- UUID4 = candidate_id из issue_candidates
status        text NOT NULL      -- "DRAFT" | "PUBLISHED" (не связан с IssueCandidateStatus)
payload_json  jsonb NOT NULL     -- DOGEIssue.to_public_dict() (см. ниже)
policy_version text NOT NULL     -- "m3.doge_issue_derivation.v1"
created_at    timestamptz        -- UTC
updated_at    timestamptz        -- UTC
```

### Структура `payload_json` — `DOGEIssue.to_public_dict()`

```json
{
  "id":          "<issue_id>",
  "status":      "PUBLISHED",
  "type":        "complaint",
  "labels":      ["pothole", "road_maintenance"],
  "title":       { "et": "...", "ru": "...", "en": "..." },
  "summary":     { "et": "...", "ru": "...", "en": "..." },
  "description": { "et": "...", "ru": "...", "en": "..." },
  "institution": {
    "et": "Tallinna Linnavalitsus",
    "ru": "Таллинская городская управа",
    "en": "Tallinn City Government"
  },
  "created_at":  "2026-05-01T10:00:00Z",
  "arweave_txid": null,
  "image_txid":   null,
  "image_hash":   null,
  "geo": {
    "admin_district":   "Kesklinn",
    "admin_settlement": "tallinn",
    "admin_region":     "harju",
    "admin_country":    "ee",
    "lat":  59.437,
    "lon":  24.753
  }
}
```

**Поля, добавляемые только если не null:** `institution`, `created_at`, `arweave_txid`, `image_txid`, `image_hash`, `geo`.

**Происхождение полей (REQ-34):**
- `type` = `canonical_type` доминантной истории (по `alpha_score`) или `"observation"`
- `labels` = union `canonical_labels` всех историй кластера, без дублей
- `title`, `summary`, `description` = агрегация из `narrative_title_json` / `narrative_summary_json` / `narrative_description_json` доминантной истории
- `institution` = `institution_json` доминантной истории (`narrative_institution`), если не `null`
- `geo` = `StoryGeoSnapshot` доминантной истории

**View `issues_dashboard`** (доступен anon/authenticated):

```sql
SELECT issue_id, status, policy_version, updated_at,
       payload_json->>'type'       AS type,
       payload_json->'title'->>'en' AS title_en,
       payload_json->'title'->>'et' AS title_et,
       payload_json->'title'->>'ru' AS title_ru,
       payload_json->'summary'->>'en' AS summary_en, ...
       payload_json->'labels'      AS labels_json,
       payload_json
FROM public.doge_issues;
```

Source: `projection/dto.py`, `bootstrap/000_full_init.sql:162-183`

---

## Слой 10: `public.doge_issue_embeddings` — векторный индекс issue

```sql
embedding_id           bigint GENERATED ALWAYS AS IDENTITY PK
issue_id               text NOT NULL     -- FK → doge_issues.issue_id ON DELETE CASCADE
model_name             text NOT NULL
embedding              vector(8)         -- nullable (GAP-08 variant A)
embedding_vector_json  text              -- основной persist-путь
source_checksum        text NOT NULL
embedding_policy_version text NOT NULL   -- "m3.doge_issue_embedding_policy.v1"
created_at             timestamptz
```

Структура аналогична `story_embeddings`. Upsert: сначала PATCH по `issue_id`, если 0 строк — INSERT.

**Индекс:** `idx_issue_embeddings_issue_id` на `issue_id`

Source: `db_supabase.py:693-738`

---

## Сводная диаграмма зависимостей

```
POST /intake/stories
        │
        ▼
stories [story_id, narrative_*, submitter_*, geo_*, lifecycle_status=ACCEPTED→ready_for_profile]
        │
        ├── idempotency_keys [key → story_id]
        │
        └── story_embeddings [story_id, model=deterministic-baseline-v1, embedding_vector_json, checksum]

ClusterCronJob (каждые cluster_cron_interval_s)
        │
        ▼
story_signals [story_id, extraction_policy → signals_json]          ← compute once, cache
        │
        ▼
issue_candidates [candidate_id, cluster_id, story_ids_json, readiness_score, status=draft→promoted]
        │
        ├── review_audit_log [candidate_id, actor, decision, rationale]
        │
        ▼
doge_issues [issue_id, status, payload_json=DOGEIssue, policy_version]
        │
        └── doge_issue_embeddings [issue_id, embedding_vector_json]

issue_story_links [issue_id, cluster_id, story_id]    ← связь story↔issue
cluster_memberships [story_id, lens, cluster_id]       ← аналитика lens-membership
```

Stories lifecycle: `accepted → partial_ready → ready_for_profile → clustered`

---

## Слой 0: `public.story_drafts` — ephemeral draft stash (GW-DRAFT-01)

Отдельный store для handoff GPT→браузер. **Не** создаёт запись в `stories` и **не** создаёт issue.

| Колонка | Тип | Обязательно | Описание |
|---------|-----|-------------|---------|
| `draft_id` | `text PK` | да | Opaque id (`secrets.token_urlsafe(16)`) |
| `payload_json` | `jsonb NOT NULL` | да | Полный `StoryDraftStashRequest` JSON (без `submitter`) как нормализован на `POST /story-drafts` |
| `created_at` | `timestamptz NOT NULL` | да | UTC момент стеша |
| `expires_at` | `timestamptz NOT NULL` | да | `created_at + STORY_DRAFT_TTL_SECONDS` (default 86400) |

**TTL:** `get_draft()` возвращает `None` (→ HTTP 404) когда `expires_at <= now()`; sqlite/supabase адаптеры удаляют протухшую строку при чтении.

**Порт:** `StoryDraftRepository` в `domain/contracts.py`; адаптеры: `InMemoryStoryDraftRepository`, `SqliteStoryDraftRepository`, `SupabaseStoryDraftRepository`.

**Миграция:** `supabase/migrations/20260703_1200_gw_draft_01_story_drafts.sql`

**Browser submit (GW-DRAFT-02):** после успешного `POST /story-drafts/{draft_id}/submit` строка удаляется из `story_drafts`; story создаётся в `stories` через `StoryIntakeService`. См. [`API_REFERENCE.md`](api-reference/API_REFERENCE.md) §6.8 submit + [`architecture-and-layers-as-is.md`](architecture-and-layers-as-is.md) §4.1.

---

## Условия проверки готовности БД при старте

При запуске в режиме `DB_BACKEND=supabase` сервис выполняет три probe-запроса:

| Проверка | Метод | Что проверяет |
|----------|-------|--------------|
| `required_tables_ready()` | GET 1 строку из каждой из 11 таблиц | Все таблицы существуют и доступны |
| `required_columns_ready()` | SELECT только нужных колонок | `stories`: geo-колонки; `story_embeddings`, `doge_issue_embeddings`: `embedding_vector_json` |
| `required_stories_intake_v2_columns_ready()` | SELECT intake v2 колонок | `narrative_title_json`, `narrative_description_json`, `narrative_session_language` применены (миграция 20260513) |

Если `db_ready=False` → cron не запускается; readiness endpoint возвращает `degraded`.

Source: `db_supabase.py:276-392`
