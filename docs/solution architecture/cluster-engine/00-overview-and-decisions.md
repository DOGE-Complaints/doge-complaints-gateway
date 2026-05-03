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
narrative_original_text                    canonical_labels[] + canonical_type
        │                                              │
        ▼ (legacy, keyword-matching)                   ▼ (target, vocabulary lookup)
infer_signals_from_narrative()         infer_signals_from_canonical()
        │                                              │
        └──────────────────┬────────────────────────────┘
                           ▼  (CLUSTER_SIGNAL_SOURCE switch)
                  StoryProfileSignals
                           │
                           ▼
                  ClusteringEngine.memberships()
                  per-lens: build_view() + stable_cluster_id()
                           │
                           ▼
              StoryClusterOrchestrator.process_story()
              └─ idempotency check
              └─ PromotionGates (min_stories, readiness)
              └─ IssueCreateService
              └─ lifecycle: READY_FOR_PROFILE → CLUSTERED
```

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
| `infer_signals_from_narrative()` | keyword-matching только по EN тексту; 2 из 6 осей вырождены | `infer_signals_from_canonical()` → vocabulary lookup из GPT labels |
| `SignalDimension` enum | 6 осей: TOPIC, SYSTEM_FAILURE, NEED, DESIRED_STATE, REPEATABILITY, RELEVANCE — все бинарные или константы | 6 новых семантических осей из GPT taxonomy (civic_domain, failure_pattern, civic_weight, desired_outcome, affected_group, geographic_district) |
| `ClusterLens` enum | 6 legacy линз, 1 вырожденная (relevance_systemic) | 6 новых семантических линз; legacy сохраняются для backward compat |
| `orchestrator.active_lenses[0]` | Primary lens = позиционная зависимость от порядка в env | `primary_lens` как именованный параметр из `CLUSTER_PRIMARY_LENS` |
| `readiness_score=100` hardcode | Gate по readiness всегда проходит; смысл порога потерян | Вычисляемый score per-cluster, передаётся в IssueCreateCommand |
| `readiness_score_for_cluster()` | Score по largest cluster в view, не по cluster target story | Score встраивается в `Cluster`, не в `ClusterView` |
| Нет lifecycle advancement | Stories остаются `READY_FOR_PROFILE` после кластеризации → дубликаты issues при каждом новом intake | Новый статус `CLUSTERED`, lifecycle advance после создания issue |
| `list_stories()` full table scan | O(N) на каждый intake | `list_stories_ready_for_clustering()` с DB-side filter |
| Нет персистенции сигналов | Пересчёт `infer_signals_from_narrative()` на каждый `process_story()` | Таблица `story_signals`, compute once + cache |
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
- **Решение:** `infer_signals_from_canonical(canonical_type, canonical_labels, geo)` — первичный путь. Keyword-matching — legacy fallback через `CLUSTER_SIGNAL_SOURCE=keyword`.
- **Причина:** GPT уже разговаривает с гражданином на его языке и возвращает language-agnostic canonical labels. Дублировать NLP keyword-matching в Python — потеря уже сделанной работы GPT.
- **Trade-off:** Зависимость от заполненности `canonical_labels` в StoryRecord; требует §22 (canonical fields в intake).

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
- **Причина:** В текущей реализации `infer_signals_from_narrative()` вызывается для ВСЕХ `READY_FOR_PROFILE` stories при каждом intake. С ростом данных — quadratic overhead.
- **Trade-off:** Лишний round-trip в БД при первом вычислении; justified при N > ~20 stories.

### ADR-CE-007: Новые и legacy линзы сосуществуют

- **Статус:** Accepted
- **Решение:** `ClusterLens` и `SignalDimension` расширяются новыми значениями. Старые (TOPIC_MICRO, FAILURE_SYSTEMIC и т.д.) не удаляются — deprecated label, используются только при `CLUSTER_SIGNAL_SOURCE=keyword`.
- **Причина:** Нельзя поломать существующие тесты и данные в БД.
- **Trade-off:** Enum становится больше; документировать deprecated ясно.

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
