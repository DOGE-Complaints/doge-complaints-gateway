# DOGEstonia — High-Level Architecture & Functional Description

> Документ описывает общую архитектуру и функциональную суть проекта DOGEstonia на базе анализа документации `doge-complaints-gateway` (Module 2). Не погружается в детали реализации.

---

## Что такое DOGEstonia

DOGEstonia — Smart City civic tech прототип для Эстонии (грантовый проект). Платформа позволяет гражданам сообщать о городских проблемах через диалог с ИИ, а затем автоматически агрегирует эти свидетельства в управляемые публичные кейсы (Distinct Issues) для городских операторов и государственных структур.

**Ключевая идея:** жалобы граждан не превращаются сразу в "тикеты" — они сначала сохраняются как первичные человеческие свидетельства (Stories), затем кластеризуются и только после достижения порога готовности становятся управляемым Issue.

---

## Компоненты системы

```
Гражданин
    ↓  диалог
GPT UI (OpenAI Custom GPT)
    ↓  POST StoryIntakeEnvelope
doge-complaints-gateway  ←——  Module 2 (Web2 Core / Story Intelligence Layer)
    ↓  issue projection
SPA Dashboard (spa-app)  ←——  Публичная витрина Issues
    ↓  (post-demo)
Web3 / Blockchain        ←——  Токенизация, on-chain доказательства
```

### GPT UI
OpenAI Custom GPT, выступающий интерфейсом сбора. GPT ведёт диалог с гражданином, извлекает структурированные сигналы из свободного текста (тема, геолокация, тип сбоя, deep need, desired state), готовит `StoryIntakeEnvelope` и отправляет его в API бэкенда. GPT — источник narrative, но **не** финальная управленческая истина: статусы публикации и issue-промоции определяет только сервер.

### doge-complaints-gateway (Module 2)
Python/FastAPI бэкенд — основной процессинговый слой. Принимает истории, хранит их неизменно, обогащает профилями сигналов, кластеризует, формирует Distinct Issues и проецирует их в SPA-совместимый формат.

### SPA Dashboard (spa-app)
Публичный дашборд (React SPA), отображающий Distinct Issues. Потребляет стабильный issue-контракт из бэкенда. MVP-ограничение: **zero-change SPA** — бэкенд обязан производить Issues, совместимые с текущим контрактом UI без breaking changes.

### Web3 слой (post-demo)
Blockchain-интеграция (Arweave для постоянного хранения артефактов, Dogeparty для токенизации) заложена архитектурно, но не входит в demo MVP.

---

## Функциональная суть Module 2 (doge-complaints-gateway)

### Формула модуля

```
Preserve Stories
  + Extract Signals
  + Build Dynamic Clusters
  + Promote Distinct Issues
  + Maintain Evidence Lineage
  + Keep SPA Contract Stable
```

### Бизнес-задача

Прямой поток жалоб в операционные системы создаёт шум, дубли и потерю человеческого контекста. Модуль решает это через разделение слоёв:

| Слой | Назначение |
|------|-----------|
| Story Store | Неизменяемые первичные свидетельства |
| Intelligence Layer | Профили сигналов и кластеризация |
| Issue Projection | SPA-совместимая витринная проекция |
| Evidence Pack | Цепочка трассируемости issue → cluster → stories |

---

## Основные сущности (Business Entities)

| Сущность | Описание |
|----------|----------|
| **Story** | Первичное свидетельство гражданина. Хранится неизменно. |
| **Story Profile / Signal Profile** | Аналитическая надстройка: тема, геоконтекст, тип сбоя, deep need, desired state, повторяемость. |
| **Cluster View** | Динамическое представление над корпусом историй. История может входить в несколько кластеров одновременно. |
| **Distinct Issue Candidate** | Кластер, достигший порога зрелости — промежуточный статус перед публикацией. |
| **Distinct Issue** | Dashboard-ready агрегат с обязательным смысловым ядром и ссылкой на evidence. |
| **Evidence Pack** | Связка `story ↔ cluster ↔ issue`, достаточная для аудита и токенизации. |

**Ключевой инвариант:** ни один Issue не существует без обратной связи к Evidence. Ни один кластер не "поглощает" Story как первичный объект.

---

## Жизненный цикл истории

```
draft_story → accepted_story → cluster_eligible → issue_candidate → projected_issue
```

Переходы к `clustered` / projected issue выполняет **in-process cron-loop** (`ClusterCronJob`, `CLUSTER_CRON_ENABLED`, default ON), а не синхронный intake: submit помечает историю как отложенную (`cron_deferred`), cron затем вызывает `process_all_pending()`.

1. **Story Intake** — приём `StoryIntakeEnvelope` от GPT; narrative сохраняется as-is.
2. **Normalization** — приведение смысла к операционной читаемости.
3. **Profile Enrichment** — заполнение сигналов для многомерной аналитики.
4. **Cluster Inclusion** — история входит в один или несколько кластеров.
5. **Cluster Maturation** — оценка cohesion score кластера до issue-candidate.
6. **Issue Projection** — формирование SPA-совместимого shape с i18n (et/ru/en).
7. **Evidence Pack Build** — выделенная доказательная сборка.

---

## Inbound API: формат данных от GPT

Endpoint: `POST /v1/stories/intake`

Тело запроса — `StoryIntakeEnvelope`:

```json
{
  "schema_version": "m2.story_intake_envelope.v1",
  "submitter":           { "external_user_id": "...", "identity_issuer": "..." },
  "narrative":           { "original_text": "...", "language": "ru" },
  "structured_signals":  { "deep_need": "...", "desired_state": "...", ... },
  "live_story_context":  { "dialogue_turns": [...], "key_facts": [...] },
  "location":            { "free_text": "Lasnamäe, Tallinn", "country_code": "EE" },
  "time":                { "kind": "date_range", "range": { ... } },
  "origin":              { "source": "openai_gpt_action", "conversation_id": "..." },
  "privacy":             { "contains_pii": false },
  "spa_issue_draft":     { "type": "complaint", "title": { "et": "...", "ru": "...", "en": "..." }, ... },
  "gov_interop_hints":   { "submission_channel": "gpt_web" }
}
```

**Принципы:**
- `narrative.original_text` — иммутабельный первичный актив, не перезаписывается.
- `spa_issue_draft` — черновик от GPT; сервер валидирует и может переопределить.
- `submitter.external_user_id` — opaque id от OAuth/IdP; не теряется на пути к evidence.
- Идемпотентность: повторная отправка с тем же `Idempotency-Key` не создаёт дубликат.

---

## Целевая архитектура (Solution Architecture)

```
GPT Intake Output
    ↓
API & Contract Layer          ← валидация, auth, DTO mapping
    ↓
Story Registry Orchestrator   ← lifecycle-команды
    ├── Story Store            ← immutable primary asset (PostgreSQL/Supabase)
    ├── Story Intelligence Engine → Cluster View Engine → Issue Promotion Engine
    │                                                          ↓
    │                                              SPA Projection Engine → SPA Issue Contract
    │                                                          ↓
    │                                              Evidence Pack Engine → Pilot Adapters (Blockchain)
    └── Geo Intelligence Module
```

### Слоёная модель
| Слой | Ответственность |
|------|----------------|
| **Presentation / API** | Request validation, auth, DTO mapping |
| **Application / Orchestration** | Lifecycle-команды, координаторы use-case |
| **Domain** | Story / Profile / Cluster / Issue / Evidence правила и инварианты |
| **Infrastructure** | DB repositories, external API adapters, queue adapters |

### Модули `src/core/`
| Модуль | Функция |
|--------|---------|
| `api` | FastAPI routes, middleware, DI |
| `application` | Use-case сервисы |
| `domain` | Доменные типы и правила |
| `intake` | Story Intake контракты и логика приёма |
| `profile` | Profile Enrichment |
| `cluster` | Cluster Engine (embedding-based) |
| `promotion` | Issue Candidate Gate и промоция |
| `projection` | SPA Projection Engine |
| `evidence` | Evidence Pack Builder |
| `geo` | Geo Intelligence (геокодинг) |
| `infrastructure` | Supabase adapters, внешние API |
| `scheduler` | `ClusterCronJob` — in-process cron-триггер promotion→доска (MVP, `CLUSTER_CRON_ENABLED` default ON); обобщённый automation plane — post-demo (EPIC-M2-11) |
| `adapters` | Integration adapters (demo/pilot) |

---

## Динамическая кластеризация

Фиксированные кластеры цементируют смысл и мешают управленческому чтению с разных сторон. Поэтому используется **multi-lens dynamic clustering**.

**Оси кластеризации:** тема, география/район, тип пространства, тип системного сбоя, deep need, desired state, время/повторяемость, suggested institution.

**Масштабы:** микро-кейс → локальный кластер → системный (city-wide) паттерн.

**Ключевые свойства:**
- Story может входить в несколько кластеров одновременно.
- Кластер можно пересобрать по новым критериям без потери первичных данных.
- Разделение analytics cluster (для аналитики) и issue-ready cluster (готов к промоции).
- Авто-промоция и проекция на доску идут через cron (`process_all_pending`); intake только откладывает кластеризацию (`cluster_outcome="deferred"`, `reason="cron_deferred"`).

---

## SPA Projection: SPA-совместимый Issue

Issue на витрине имеет строгий контракт совместимости с текущим SPA:

| Поле | Обязательность |
|------|---------------|
| `id`, `status`, `type` | Обязательны |
| `labels`, `title`, `summary`, `description` | Обязательны |
| `title/summary/description` | i18n формат `{ et, ru, en }` |
| `institution`, `created_at`, `arweave_txid` | Опциональны |

**Правила:** статус по умолчанию `NEW`; type только из согласованного словаря; фиктивные blockchain-txid запрещены.

---

## Технологический стек

| Компонент | Технология |
|-----------|-----------|
| Backend runtime | Python 3.11 + FastAPI (ASGI) |
| Database | Supabase (PostgreSQL) |
| Embeddings / Vectorization | Supabase Edge Functions |
| AI summarization | Anthropic API (via Edge Function) |
| Permanent storage (pilot) | Arweave / IPFS via Pinata |
| Tokenization (pilot/legacy) | Dogeparty |
| Geocoding | OpenCage / Nominatim |

---

## Бизнес-метрики успеха

| Метрика | Описание |
|---------|----------|
| Duplicate Compression Ratio | Снижение дублей на витрине |
| Cluster Cohesion Score | Качество кластеров |
| Issue Readiness Conversion Rate | Доля историй, доходящих до Issue |
| False Merge Rate | Некорректные склейки несовместимых историй |
| Evidence Completeness Index | Полнота доказательной базы |
| Трассируемость issue→story | Должна быть 100% |

---

## Ключевые архитектурные принципы

1. **Story-first, issue-later** — сначала фиксация свидетельства, потом агрегация.
2. **No evidence loss** — агрегация не уничтожает первичный narrative.
3. **Multi-lens clustering** — нет единственного "правильного" кластера.
4. **Aggregation without dehumanization** — снижение дублей без потери человеческого слоя.
5. **Traceability by design** — любой Issue объясним назад до Story.
6. **Zero-change SPA** — расширения только опциональные и backward-compatible.
7. **Adapter-first tokenization** — Web3 интегрируется через адаптеры без ломки домена.
8. **Разделение "user said" / "system inferred"** — narrative и интерпретации хранятся отдельно.

---

## Scope MVP vs Post-Demo

**In Scope (MVP demo):**
- Story Intake от GPT с OAuth авторством
- Story Profile / Signal Profile
- Dynamic Cluster Views
- Distinct Issue formation и SPA Projection
- Evidence Pack и lineage
- Geo Intelligence

**Out of Scope (MVP):**
- Интервью с пользователем (это задача GPT)
- On-chain токенизация / голосование
- Финальная гос-интеграция (Smart City API)
- Обобщённый automation plane (job runner / queue / ручной replay) — post-demo (EPIC-M2-11). NB: минимальный in-process cron-loop промоции кластеров (`ClusterCronJob`, `CLUSTER_CRON_ENABLED`, default ON) входит в MVP как триггер доски.
- Story tokenization и contributor notifications (post-demo)
