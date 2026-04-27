# 23. M2 Demo: кластеризация stories и выпуск issue — решения интервью (SSOT v1)

## 1. Назначение и статус

Документ фиксирует **требования уровня product/CTO** по итогам второго интервью (hardcoded clustering criteria + переход cluster → issue для demo), с **верификацией по коду** `doge-complaints-gateway`.

| Атрибут | Значение |
|--------|----------|
| Источник (сырой артефакт) | `docs/tasks/task-cluster-criteria-interview-01/interview-report-cluster-criteria-01.md` |
| Дата интервью | 2026-04-26 |
| Область | **Demo**; полная реализация кластеризатора, SQL и смена API — вне этого файла (см. задачи в §8) |
| Связь с intake | Решения по полям story (`canonical_type`, `title_hint`, persist) — в **`22-m2-demo-story-intake-interview-ssot-v1.md`**; без них часть решений этого документа **не реализуема в данных** |

**Правило:** раздел 3 — целевые решения интервью; раздел 2 — фактическое состояние кода на момент фиксации; при конфликте отчёта интервью и кода в разделе 2 указано расхождение.

---

## 2. Верификация по коду gateway (as-is)

### 2.1 `ClusteringEngine` и линзы

- Ровно **6** линз в константе `CANONICAL_LENSES` — см. `src/core/cluster/engine.py` (кортеж из шести значений `ClusterLens`).
- Формула readiness: `base = min(100, 20 + size * 15)`, `lens_bonus = 5` для `FAILURE_SYSTEMIC` и `RELEVANCE_SYSTEMIC`, `mode_bonus = 10` при `ClusteringMode.ISSUE_READY` — см. `readiness_score_for_cluster` в том же файле.
- `stable_cluster_id`, `dominant_value`, `build_cluster_narrative` — см. `src/core/cluster/engine.py`.
- Итерация по корзинам кластеров идёт по **`sorted(buckets.keys())`** — детерминированный порядок по строковому ключу корзины; выбор «primary» view — **`max(clusters, key=lambda cluster: len(cluster.members))`** (кластер с наибольшим числом members).

### 2.2 Связь cluster → issue сегодня

- HTTP-слой принимает у создания issue **внешние** `cluster_id`, `story_ids`, `readiness_score`, `title` — см. разбор payload в `src/core/api/handlers.py` (поля `cluster_id` и связанные).
- `IssueCreateCommand` содержит `cluster_id`, `story_ids`, `readiness_score`, `title` — см. `src/core/application/issue_create.py`.
- `StoryPromotionProjectionBridge.build_projection_input` строит `ProjectionInput`, вызывая **`_derive_issue_type`** и **`_derive_labels`** от **`promoted_title`** и агрегированного текста narratives — см. `src/core/application/issue_create.py` (метод `build_projection_input` и функции `_derive_*` ниже по файлу).
- `_derive_issue_type` / `_derive_labels` используют **латинские ключевые токены** в `.lower()`-корпусе (`"broken"`, `"waste"`, …) — см. `src/core/application/issue_create.py`.

### 2.3 Promotion gates (важное расхождение с формулировкой отчёта)

В отчёте интервью для строки mapping указано «нет (always promote)» относительно порога readiness на уровне pipeline. **В текущем коде** при переходе кандидата из `DRAFT` вызывается `evaluate_promotion_gates`: политика по умолчанию **`PromotionGatePolicy(min_readiness_score=70, min_stories=2)`** — см. `src/core/promotion/gates.py` и использование в `IssuePromotionService.submit_for_review` в `src/core/promotion/service.py`.

То есть **gate на readiness и число stories уже есть**, но значения **зашиты в коде**, а не читаются из `.env` (в `src/core/config` переменных `CLUSTER_*` **нет** — поиск по репозиторию `CLUSTER_` вне `docs/` не даёт совпадений в Python-конфиге).

### 2.4 `StoryRecord` и geo

- У записи story есть поле **`geo: StoryGeoSnapshot | None`** (в т.ч. `cluster_tags`) — см. `src/core/domain/contracts.py`.
- Полей **`canonical_type`**, **`canonical_labels`**, **`narrative_title_hint`** / **`language`** в `StoryRecord` **нет** — см. тот же `StoryRecord` в `src/core/domain/contracts.py`.

---

## 3. Принятые решения интервью (целевое состояние demo)

Сводка решений **D-01 … D-11** из отчёта (идентификаторы сохранены).

| ID | Решение (кратко) |
|----|------------------|
| D-01 | `MIN_CLUSTER_SIZE` **по умолчанию 8**, задаётся через **`.env`** (`CLUSTER_MIN_SIZE` в таблице отчёта). |
| D-02 | Порог **`READINESS_SCORE_THRESHOLD`** — через **`.env`**; числовой default в интервью **не зафиксирован** (OP-01 в отчёте; предложение 65 — только как гипотеза в open points). |
| D-03 | **`ACTIVE_LENSES`** — список линз из **`.env`** (одна или несколько); в `example.env` — комментарий со всеми допустимыми линзами. |
| D-04 | **Язык не разделяет кластеры** — ET/RU/EN могут быть в одном кластере. |
| D-05 | **`CLUSTER_GEO_FILTER`** — bool через **`.env`**; default **не зафиксирован** (OP-02). |
| D-06 | **`CLUSTER_TIE_BREAKER`** через **`.env`** (`oldest_first` \| `systemic_priority` \| `alpha`); default **не зафиксирован** (OP-03). |
| D-07 | **`canonical_type` от GPT** — primary; backend `_derive_issue_type` — **устаревший** после появления полей в `StoryRecord`. |
| D-08 | **`canonical_labels[]` от GPT** — primary; `_derive_labels` — **устаревший** после появления полей в `StoryRecord`. |
| D-09 | **`CLUSTER_TYPE_RESOLUTION`** через **`.env`** (напр. `majority` \| `priority` \| `first`); default в отчёте — **majority** (с уточнением приоритетов в OP-04). |
| D-10 | Связь story–issue **N:M** (одна story в нескольких issues допустима); нужна таблица связей (**`issue_story_links`** и т.п.) — на уровне требования, не как факт кода. |
| D-11 | Заголовок issue — **`title_hint` доминантной story** в кластере; внешний **`IssueCreateCommand.title`** — убрать как обязательный ввод после реализации (целевое). |

### 3.1 Целевой контракт выхода кластерного шага (из отчёта)

Минимальный набор полей результата кластеризации (как в отчёте):  
`cluster_id`, `story_ids[]`, `readiness_score`, `dominant_lens`, `dominant_type`, `dominant_labels[]`, плюс расширения — **OP-05** в отчёте.

---

## 4. Open points (из интервью)

Перенесены из отчёта без изменения смысла: **OP-01 … OP-08** (default порогов readiness/geo/tie-breaker; приоритеты `CLUSTER_TYPE_RESOLUTION`; поля «Other» в output; определение доминантной story; стратегия при росте кластера; выравнивание таксономии GPT ↔ backend).

---

## 5. Согласованность с продуктовой моделью кластеров (документ 07)

`07-dynamic-clusters-product-model.md` задаёт общие оси, множественную принадлежность story и **readiness score к issue-candidate**. Решения интервью **конкретизируют** demo: пороги через `.env`, отсутствие language-partition, N:M story–issue, первичность сигналов GPT для type/labels. При планировании MVP сверять **07** (принципы) и **23** (demo-параметры и контракты).

---

## 6. Reconciliation: GPT-данные ↔ `StoryRecord` (факт кода)

| Нужно по интервью | В `StoryRecord` сейчас | Блокер реализации |
|-------------------|----------------------|-------------------|
| `canonical_type`, `canonical_labels[]`, персистируемый `title_hint` | нет | расширение intake + домен + БД (**`TASK-INTAKE-STORY-CONTRACT-EXPANSION-02`**, см. doc **22**) |
| `narrative_original_text` для similarity | да (`narrative_original_text`) | — |
| geo для фильтра по гео | да (`geo`) | включение логики `CLUSTER_GEO_FILTER` в pipeline |

---

## 7. Принцип конфигурации (интервью)

**Все пороги и выборы осей для demo** — через **переменные окружения** (и соответствующие поля `AppConfig`), а не «немые» константы в бизнес-логике. Исключение на момент фиксации документа: **`PromotionGatePolicy`** и **`CANONICAL_LENSES`** уже заданы в коде числами/кортежем — миграция к `.env` — часть реализации **`TASK-CLUSTER-STORY-FIRST-PIPELINE-01`** и связанных задач.

---

## 8. Трассировка на задачи и анализ

| Зона | Куда |
|------|------|
| Pipeline cluster → candidate issue + env-driven параметры | `TASK-CLUSTER-STORY-FIRST-PIPELINE-01` |
| Персистенция связей story–issue | `TASK-DB-SOURCE-PROCESS-LINKAGE-01` |
| E2E demo path | `TASK-TEST-E2E-STORY-TO-ISSUE-CLUSTER-01` |
| Связь GAP ↔ TASK | `docs/analysis/story-first-gap-task-linkage.md` |
| Intake + persist canonical полей | **`22-m2-demo-story-intake-interview-ssot-v1.md`** |

---

## 9. Связь с документом 19

`19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` описывает широкий inbound-envelope. Кластерные пороги и выходной контракт **demo story-first** после интервью фиксируются здесь (**23**) и должны быть согласованы с реализацией `ClusteringEngine` / HTTP / promotion при конвергенции.
