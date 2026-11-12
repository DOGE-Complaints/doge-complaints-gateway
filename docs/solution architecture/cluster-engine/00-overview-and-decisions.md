# Cluster Engine — Solution Architecture Overview

**Дата:** 2026-04-30  
**Пакет:** `docs/solution architecture/cluster-engine/`  
**Требования:** `25-clustering-engine-target-state-spec.md`, `26-clustering-signal-axes-from-gpt-taxonomy.md`  
**Аудит:** `docs/analysis/clustering-audit-story-to-issue.md`

---

## 1. Структура пакета

```
cluster-engine/
├── 00-overview-and-decisions.md     ← этот файл
├── 01-data-model-and-contracts.md   ← типы, схема БД, протоколы
├── 02-signal-extraction.md          ← словари, enrichment, signal source hierarchy
└── 03-engine-and-orchestrator.md    ← ClusteringEngine, orchestrator, lifecycle
```

---

## 2. Компоненты и их текущее состояние

```
canonical_labels[] + canonical_type + geo.admin_settlement
        │
        ▼ (vocabulary lookup — language-agnostic)
infer_signals_from_canonical()
        │
        ▼
StoryProfileSignals
        │
        ▼
ClusteringEngine.memberships()
per-lens: build_view() + stable_cluster_id() [SHA-256]
        │
        ▼
StoryClusterOrchestrator.process_story()
└─ idempotency check (CLUSTERED lifecycle guard)
└─ primary_lens из CLUSTER_PRIMARY_LENS
└─ readiness_for_story() → score per-cluster
└─ PromotionGates (min_stories, readiness, canonical_type gate)
└─ IssueCreateService
└─ lifecycle: READY_FOR_PROFILE → CLUSTERED (все members)
```

**Примечание:** `infer_signals_from_narrative()` и режимы `keyword`/`hybrid` удалены в REQ-34 (2026-05-15). Единственный путь — canonical lookup.

---

## 3. Что сохраняем (хорошая архитектура)

| Компонент | Почему оставляем |
|-----------|-----------------|
| `ClusteringEngine` как frozen dataclass | Immutable, testable, DI-friendly |
| Protocol-based DI для всех stores | Позволяет InMemory/SQLite/Supabase без изменения domain |
| Promotion state machine (DRAFT → PROMOTED) | Правильная последовательность переходов, audit trail |
| `ClusterLens` как StrEnum | Extensible, string-safe для config и DB |
| `build_view()` / `memberships()` паттерн | Правильное разделение — view building vs. membership lookup |
| `dominant_value()` | Корректная функция агрегации, переиспользуем |
| `ServiceFactory` как composition root | Единое место сборки зависимостей |
| `AppConfig` как frozen dataclass | Immutable конфиг, loaded once at startup |
| `StoryProfileSignals` dataclass | Удобная единица передачи между enrichment и engine |

---

## 4. Что переделываем (критические проблемы)

| Компонент | Проблема | Решение |
|-----------|----------|---------|
| `stable_cluster_id()` | `hash()` зависит от PYTHONHASHSEED → разные IDs при рестарте | `hashlib.sha256` → cross-process stable |
| `infer_signals_from_narrative()` | keyword-matching только по EN тексту; 2 из 6 осей вырождены | **Реализовано (REQ-34)**: функция удалена; `infer_signals_from_canonical()` — единственный путь |
| `SignalDimension` enum | 6 осей: TOPIC, SYSTEM_FAILURE, NEED, DESIRED_STATE, REPEATABILITY, RELEVANCE — бинарные/константы | **Реализовано (REQ-34)**: 6 civic осей (CIVIC_DOMAIN, FAILURE_PATTERN, CIVIC_WEIGHT, DESIRED_OUTCOME, AFFECTED_GROUP, GEOGRAPHIC_DISTRICT) |
| `ClusterLens` enum | 6 legacy линз, 1 вырожденная (relevance_systemic) | **Реализовано (REQ-34)**: 6 civic линз; legacy полностью удалены |
| `orchestrator.active_lenses[0]` | Primary lens = позиционная зависимость от порядка в env | `primary_lens` как именованный параметр из `CLUSTER_PRIMARY_LENS` |
| `readiness_score=100` hardcode | Gate по readiness всегда проходит; смысл порога потерян | Вычисляемый score per-cluster, передаётся в IssueCreateCommand |
| `readiness_score_for_cluster()` | Score по largest cluster в view, не по cluster target story | Score встраивается в `Cluster`, не в `ClusterView` |
| Нет lifecycle advancement | Stories остаются `READY_FOR_PROFILE` после кластеризации → дубликаты issues при каждом новом intake | Новый статус `CLUSTERED`, lifecycle advance после создания issue |
| `list_stories()` full table scan | O(N) на каждый intake | `list_stories_ready_for_clustering()` с DB-side filter |
| Нет персистенции сигналов | Пересчёт сигналов на каждый `process_story()` | **Реализовано**: таблица `story_signals`, compute once + cache |
| `handlers.py` молча отбрасывает `process_story()` result | Нет observability — создался issue или нет | Логировать `issue_id` / причину отказа |
| `ClusteringMode.ISSUE_READY` не используется | Режим объявлен, но orchestrator всегда передаёт ANALYTIC | В orchestrator использовать ISSUE_READY при создании issue |
| `build_cluster_narrative()` static string | Narrative не несёт информации | Динамический narrative из dominant signals (§03) |
| Три config stub не подключены | `GEO_FILTER`, `TIE_BREAKER`, `TYPE_RESOLUTION` в AppConfig есть, в engine не переданы | Передать при инициализации ClusteringEngine |

---

## 5. Архитектурные решения (ADR)

### ADR-CE-001: SHA-256 вместо hash()

- **Статус:** Accepted
- **Решение:** `stable_cluster_id()` использует `hashlib.sha256`, не `hash()`.
- **Причина:** Python `hash()` пересеивается при каждом запуске интерпретатора (PYTHONHASHSEED). Одни и те же данные → разные cluster_id в разных процессах → сломанные ссылки в БД.
- **Trade-off:** SHA-256 немного медленнее; для кластеризации (не crypto) это несущественно.

### ADR-CE-002: Vocabulary lookup как основной источник сигналов

- **Статус:** Accepted
- **Решение:** `infer_signals_from_canonical(canonical_type, canonical_labels, geo)` — единственный путь. Режимы `keyword` и `hybrid` (`CLUSTER_SIGNAL_SOURCE=keyword/hybrid`) удалены в REQ-34 (2026-05-15).
- **Причина:** GPT уже разговаривает с гражданином на его языке и возвращает language-agnostic canonical labels. Дублировать NLP keyword-matching в Python — потеря уже сделанной работы GPT.
- **Trade-off:** Зависимость от заполненности `canonical_labels` в StoryRecord; требует canonical fields в intake (реализовано).

### ADR-CE-003: Readiness score per Cluster, не per ClusterView

- **Статус:** Accepted
- **Решение:** `Cluster` dataclass хранит собственный `readiness_score`; `ClusterView.readiness_score` убирается или остаётся как агрегат (max по clusters).
- **Причина:** `build_view()` сейчас считает readiness для `max(clusters, key=members)` — primary cluster. Если target story в малом кластере, её score неверен. Orchestrator должен получать score именно для своего кластера.
- **Trade-off:** Небольшое увеличение памяти (score в каждом кластере).

### ADR-CE-004: CLUSTERED как lifecycle-идемпотентность

- **Статус:** Accepted
- **Решение:** После создания issue все stories в кластере переходят в `CLUSTERED`. `list_stories_ready_for_clustering()` возвращает только `READY_FOR_PROFILE`.
- **Причина:** Самый чистый механизм идемпотентности — domain lifecycle, а не deduplication по cluster_id. Также убирает O(N) full table scan.
- **Trade-off:** Если issue rejected — story застревает в `CLUSTERED` (нужен `CLUSTERED → READY_FOR_PROFILE` transition при отказе промоции). Решить: orchestrator rollback при `PromotionStateError`.

### ADR-CE-005: CLUSTER_PRIMARY_LENS как именованный config

- **Статус:** Accepted
- **Решение:** `AppConfig.cluster_primary_lens: str` из `CLUSTER_PRIMARY_LENS` env var; дефолт `"civic_domain_micro"`. Заменяет `active_lenses[0]`.
- **Причина:** Позиционная зависимость от порядка в comma-separated env var хрупка и неочевидна.
- **Trade-off:** Дополнительная env var; validation усложняется (primary_lens должен быть в active_lenses).

### ADR-CE-006: Сигналы персистируются в story_signals

- **Статус:** Accepted
- **Решение:** При первом вычислении сигналы записываются в `story_signals (story_id, policy, signals_json)`. При повторном `process_story()` — читаются из кэша.
- **Причина:** До REQ-34 `infer_signals_from_narrative()` (а после — `infer_signals_from_canonical()`) вызывается для ВСЕХ `READY_FOR_PROFILE` stories при каждом intake. С ростом данных — quadratic overhead.
- **Trade-off:** Лишний round-trip в БД при первом вычислении; justified при N > ~20 stories.

### ADR-CE-007: Новые и legacy линзы сосуществуют

- **Статус:** ~~Accepted~~ **Superseded REQ-34 (2026-05-15)**
- **Решение (устаревшее):** Старые лензы не удаляются — deprecated label, при `CLUSTER_SIGNAL_SOURCE=keyword`.
- **Фактическое состояние:** Legacy лензы (TOPIC_MICRO, NEED_LOCAL, FAILURE_SYSTEMIC, FAILURE_MICRO, REPEATABILITY_LOCAL, RELEVANCE_SYSTEMIC) **полностью удалены** из `ClusterLens` enum. `CLUSTER_SIGNAL_SOURCE=keyword/hybrid` не поддерживается. `ClusterLens` содержит только 6 civic значений.
- **Причина отмены:** Поломки тестов не было — тесты к тому моменту уже тестировали civic-систему. Коэкзистенция вызывала документационный дрейф.

### ADR-CE-008: cluster_memberships — аналитическая таблица, не core

- **Статус:** Accepted  
- **Решение:** `cluster_memberships` — опциональная таблица для analytics/read API. Не блокирует основной pipeline. Заполняется в orchestrator после успешного issue creation.
- **Причина:** Core pipeline работает через in-memory memberships. Persistence нужна для read-side (аналитика, drill-down).
- **Trade-off:** При отказе записи в cluster_memberships — не падать, логировать.

---

## 6. Зависимости между компонентами (целевое)

```
vocabulary.py          → enrichment.py (signal extraction)
enrichment.py          → cluster_orchestrator.py (via StoryProfileSignals)
types.py               → engine.py, orchestrator
engine.py              → orchestrator
orchestrator           → story_repository (list_ready, update_lifecycle)
orchestrator           → signal_store (get/save signals)
orchestrator           → clustering_engine (memberships)
orchestrator           → issue_create_service (create_issue)
orchestrator           → cluster_membership_store (save_membership)
service_factory.py     → wires all of the above from AppConfig
```

---

## 7. Файлы, затронутые реализацией

| Файл | Тип изменения |
|------|---------------|
| `src/core/cluster/vocabulary.py` | **Создать** — frozenset registries |
| `src/core/cluster/types.py` | **Изменить** — новые ClusterLens, ClusteringMode, Cluster.readiness_score |
| `src/core/cluster/engine.py` | **Изменить** — SHA-256, per-cluster score, dynamic narrative |
| `src/core/domain/contracts.py` | **Изменить** — новые SignalDimension, CLUSTERED status, new Repository methods |
| `src/core/profile/enrichment.py` | **Изменить** — новая функция `infer_signals_from_canonical()`, сохранить legacy |
| `src/core/application/cluster_orchestrator.py` | **Переписать** — убрать все hardcodes, добавить idempotency, lifecycle |
| `src/core/infrastructure/service_factory.py` | **Изменить** — wire новые config params, новые stores |
| `src/core/config/schema.py` | **Изменить** — новые env vars, validation |
| `src/core/api/handlers.py` | **Изменить** — логировать issue_id результат |
| `src/core/infrastructure/repositories.py` | **Изменить** — InMemory реализации новых stores |
| `src/core/infrastructure/db_sqlite.py` | **Изменить** — SQLite реализации |
| `src/core/infrastructure/db_supabase.py` | **Изменить** — Supabase реализации |
