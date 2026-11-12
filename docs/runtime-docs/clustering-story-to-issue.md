# Clustering: Story → Issue — Runtime Architecture

**Дата:** 2026-04-30 (обновлён 2026-08-29T09:20:52Z — указатель pack-ветки SSR-04/05)  
**Методология:** analysis.mdc — только факты из кода, без предположений  
**Scope:** `doge-complaints-gateway` — cluster subsystem (civic lenses, post REQ-34 migration 2026-05-15). Pack-ветка — §1.3, не дублирует civic-схему ниже.

---

## 1. Общая схема пайплайна

### 1.1 Intake — приём истории (синхронно, без кластеризации)

```
POST /intake/stories
        │
        ▼
geo_scope check (если CLUSTER_GEO_SCOPE задан и location_query не пуст)
→ GeoScopeMismatchError если story вне зоны ответственности ноды
        │
        ▼
StoryIntakeService.create_story()
→ StoryRecord сохранён, lifecycle_status = READY_FOR_PROFILE
        │
        ▼
logs: story_cluster_issue_pending reason=cron_deferred
```

**Важно:** `POST /intake/stories` **не запускает кластеризацию синхронно**. После сохранения story intake возвращает ответ и логирует `reason=cron_deferred`. Кластеризация полностью отдана фоновому крону.

**Источник:** `src/core/api/handlers.py` (строки 195–203: явный комментарий "Intake path no longer clusters synchronously")

---

### 1.2 Cron — фоновая кластеризация (каждые CLUSTER_CRON_INTERVAL_S секунд)

```
ClusterCronJob._run_loop()  [daemon thread]
        │  каждые CLUSTER_CRON_INTERVAL_S секунд
        ▼
if ready_count < min_size_guard → skip (logs: cluster.batch_skipped_min_size)
        │
        ▼
StoryClusterOrchestrator.process_all_pending()
        │
        ▼
list_stories_ready_for_clustering()  ← DB-side filter (только READY_FOR_PROFILE)
        │
        ▼
для каждой story: get_signals_for_story(story)
→ infer_signals_from_canonical(canonical_type, canonical_labels, geo)
→ StoryProfileSignals(story_id, signals, geo)
        │
        ▼
ClusteringEngine.memberships(profiles)
→ {story_id → {lens_name → cluster_id}} для всех active_lenses
geo_filter_bucket() включается в cluster_key: "...base...|geo:{level}:{token}"
        │
        ▼
per-cluster: _create_issue_for_cluster(...)
│
├─ readiness_for_story() → readiness_score per Cluster (не max в view)
│
├─ PromotionGates check (min_stories, readiness_threshold, canonical_type gate)
│
├─ IssueCreateService.create_issue(IssueCreateCommand(
│       cluster_id, story_ids, readiness_score, title
│   ))
│
└─ lifecycle: все members → CLUSTERED
        │
        ▼
logs: cluster.cron_run_end run_id=... created_issue_count=... duration_ms=...
```

**Источники:**
- `src/core/scheduler/cluster_cron.py`
- `src/core/application/cluster_orchestrator.py` (civic path ниже; файл не `story_cluster_orchestrator.py`)
- `src/core/infrastructure/service_factory.py`

---

### 1.3 Schema-pack ветка (SSR-04/05) — тот же cron, другой engine

Диаграмма §1.2 описывает **civic** stories **без** persist-binding. Если у `StoryRecord` truthy `schema_id` и `bound_schema_version` (`is_schema_bound`, [`pack_engine.py:16–18`](../../src/core/schema/pack_engine.py)), `process_story` идёт в `_process_pack_bound_story` ([`cluster_orchestrator.py:236–237`](../../src/core/application/cluster_orchestrator.py)): exact-lens по `structured_payload`, promote по `readiness_policy` пака. Civic pool `_civic_ready` эти строки не берёт. Второй cron нет — по-прежнему `process_all_pending` ([`cluster_cron.py:64`](../../src/core/scheduler/cluster_cron.py)).

Операторский мануал (два мира, ALTER, как добавить ноду): [`manuals/schema-packs-node-data-model-ru.md`](./manuals/schema-packs-node-data-model-ru.md).

---

## 2. Сигнальные измерения (SignalDimension)

Каждый StoryProfileSignals содержит значения по 6 обязательным осям (civic lenses, REQ-34):

| Dimension | Смысл оси | Пример значений |
|-----------|-----------|----------------|
| `CIVIC_DOMAIN` | Тематика жалобы | `roads`, `transport`, `housing`, `waste`, ... (12 вариантов) |
| `FAILURE_PATTERN` | Тип сбоя | `broken_infrastructure`, `delay`, `unsafe_condition`, ... (9 вариантов) |
| `CIVIC_WEIGHT` | Системность сигнала | `systemic_pattern`, `not_only_me`, `recurring_issue`, `isolated` |
| `DESIRED_OUTCOME` | Желаемый результат | `better_maintenance`, `faster_response`, `safer_space`, ... |
| `AFFECTED_GROUP` | Затронутая группа | `residents`, `pedestrians`, `elderly_context`, `general_public` |
| `GEOGRAPHIC_DISTRICT` | Административный район | `lasnamäe`, `kesklinn`, `unknown` |

**Источник:** `src/core/domain/contracts.py` (SignalDimension enum)  
**Словари:** `src/core/cluster/vocabulary.py`

---

## 3. Извлечение сигналов: `infer_signals_from_canonical()`

Единственная функция извлечения сигналов (REQ-34, 2026-05-15). `infer_signals_from_narrative()` удалена.

```python
# src/core/profile/enrichment.py
def get_signals_for_story(story: StoryRecord) -> dict[str, str]:
    return infer_signals_from_canonical(
        story.narrative_canonical_type,
        story.narrative_canonical_labels,
        story.geo.admin_settlement if story.geo else None,
    )
```

**Принцип:** GPT нормализует нарратив на любом языке (ET/RU/EN) в `canonical_labels` — vocabulary-lookup в `vocabulary.py` даёт сигнал. Языковая нейтральность обеспечивается GPT, а не кодом gateway.

**Инвариант:** функция возвращает все 6 SignalDimension ключей; отсутствие данных → `"unknown"` или dimension-specific дефолт (`"isolated"` для civic_weight, `"general_public"` для affected_group).

**Источник:** `src/core/profile/enrichment.py` — `infer_signals_from_canonical()`, `get_signals_for_story()`

---

## 4. Кластерные линзы (ClusterLens)

6 civic линз определяют, по какому сигнальному измерению объединяются истории (REQ-34):

| Lens | Измерение | Суффикс ключа | Бонус readiness |
|------|-----------|--------------|-----------------|
| `civic_domain_micro` | CIVIC_DOMAIN | `:micro` | — |
| `failure_pattern_micro` | FAILURE_PATTERN | `:micro` | — |
| `civic_weight_systemic` | CIVIC_WEIGHT | `:systemic` | **+10** |
| `desired_outcome_local` | DESIRED_OUTCOME | `:local` | — |
| `affected_group_local` | AFFECTED_GROUP | `:local` | — |
| `geographic_district_micro` | GEOGRAPHIC_DISTRICT | `:micro` | **+5** |

**Формирование cluster_id (SHA-256):**
```python
# src/core/cluster/engine.py
key = f"{lens.value}:{dimension.value}:{raw_value}:{suffix}"
digest_hex = hashlib.sha256(f"{lens.value}:{key}".encode()).hexdigest()
numeric = int(digest_hex, 16) % 10_000_000_000
cluster_id = f"cluster:{lens.value}:{numeric:010d}"
```

ID детерминирован и стабилен между процессами (ADR-CE-001 — SHA-256, не Python `hash()`).

**Источник:** `src/core/cluster/types.py` (ClusterLens enum), `src/core/cluster/engine.py` (stable_cluster_id)

---

## 5. Оценка готовности кластера (readiness_score)

```python
# src/core/cluster/engine.py:readiness_score_for_cluster()
size       = len(members)
base       = min(100, 20 + size * 15)
lens_bonus = lens_readiness_bonus(lens)  # CIVIC_WEIGHT_SYSTEMIC → +10, GEOGRAPHIC_DISTRICT_MICRO → +5
mode_bonus = 10 if mode == ISSUE_READY else 0
score      = min(100, base + lens_bonus + mode_bonus)
```

Таблица base-score по размеру кластера:

| Stories | base | +civic_weight_systemic | +ISSUE_READY mode | итого (systemic) |
|---------|------|----------------------|-------------------|-----------------|
| 1 | 35 | +10 | +10 | 55 |
| 2 | 50 | +10 | +10 | 70 |
| 3 | 65 | +10 | +10 | 85 |
| 4 | 80 | +10 | +10 | 100 |
| 5+ | 95+ | — | — | 100 |

Readiness score вычисляется для конкретного кластера story (не для max кластера в view) и передаётся в `IssueCreateCommand`.

---

## 6. Ворота продвижения (PromotionGatePolicy)

```python
# src/core/promotion/gates.py
@dataclass(frozen=True)
class PromotionGatePolicy:
    min_readiness_score: int  # из CLUSTER_READINESS_THRESHOLD
    min_stories: int          # из CLUSTER_MIN_SIZE

# Реальные значения из AppConfig (service_factory.py):
PromotionGatePolicy(
    min_readiness_score=config.cluster_readiness_threshold,  # default: 60
    min_stories=config.cluster_min_size,                     # default: 5
)
```

Кандидат блокируется если:
1. `candidate.readiness_score < min_readiness_score` → `"readiness_below_threshold"`
2. `len(candidate.story_ids) < min_stories` → `"insufficient_story_evidence"`
3. Кластер без хотя бы одной истории с `canonical_type in {"complaint", "system_bug"}` → `"canonical_type_gate_reject"` (REQ-34)

---

## 7. Конфигурация (env vars)

| Переменная | Default | Тип | Используется в runtime |
|------------|---------|-----|----------------------|
| `CLUSTER_MIN_SIZE` | `5` | int >0 | `PromotionGatePolicy.min_stories` |
| `CLUSTER_READINESS_THRESHOLD` | `60` | int 1-100 | `PromotionGatePolicy.min_readiness_score` |
| `CLUSTER_ACTIVE_LENSES` | `civic_domain_micro,failure_pattern_micro,civic_weight_systemic,desired_outcome_local,affected_group_local,geographic_district_micro` | comma-list | `ClusteringEngine.active_lenses` |
| `CLUSTER_PRIMARY_LENS` | `civic_domain_micro` | str | `ClusteringEngine.primary_lens` |
| `CLUSTER_ID_ALGORITHM` | `sha256` | str | `stable_cluster_id()` |
| `CLUSTER_CRON_ENABLED` | `true` | bool | запуск/остановка фонового cron |
| `CLUSTER_CRON_INTERVAL_S` | `60` | int | интервал между прогонами cron (секунды) |
| `CLUSTER_GEO_FILTER` | `country` | str | гранулярность гео-бакета в cluster_key: `district\|settlement\|region\|country` |
| `CLUSTER_GEO_SCOPE` | `null` | str\|null | зона ответственности ноды: `<level>:<value>`, напр. `settlement:tallinn` |
| `CLUSTER_TIE_BREAKER` | `alpha` | str | стратегия выбора dominant story (alpha_score в orchestrator) |
| `CLUSTER_TYPE_RESOLUTION` | `canonical_priority` | str | стратегия определения issue_type из canonical_type историй кластера |

---

## 8. Что конфигурируется

1. **Набор активных линз** — `CLUSTER_ACTIVE_LENSES` (comma-list civic линз). Дефолт: все 6.
2. **Primary lens** — `CLUSTER_PRIMARY_LENS` (по какой линзе создаётся issue). Дефолт: `civic_domain_micro`.
3. **CLUSTER_MIN_SIZE** — минимум историй для промоции. Дефолт: `5`.
4. **CLUSTER_READINESS_THRESHOLD** — порог score для создания issue. Дефолт: `60`.
5. **CLUSTER_CRON_ENABLED / CLUSTER_CRON_INTERVAL_S** — фоновый cron для `process_all_pending`.

---

## 9. Фоновый cron — структура, жизненный цикл, обработка ошибок

### 9.1 Структура

`ClusterCronJob` (`src/core/scheduler/cluster_cron.py`) — daemon-поток с именем `cluster-cron-job`. Работает поверх `threading.Event` и `threading.Lock`.

```python
@dataclass
class ClusterCronJob:
    orchestrator: StoryClusterOrchestrator
    interval_s: int          # из CLUSTER_CRON_INTERVAL_S (дефолт: 60)
    min_size_guard: int      # из CLUSTER_MIN_SIZE (дефолт: 5)
    _stop_event: Event       # сигнал остановки
    _run_lock: Lock          # исключает параллельные прогоны
    _thread: Thread | None   # daemon=True → не блокирует завершение процесса
```

### 9.2 Жизненный цикл

**Запуск** (ASGI lifespan startup):
```python
# src/core/api/asgi_app.py
if deps.config.cluster_cron_enabled:
    if deps.config.db_backend == "supabase" and not deps.db_ready:
        # DB не готова → cron не стартует, только warning в лог
        logger.warning("startup.cluster_cron_skipped ...")
    else:
        cron_job = ClusterCronJob(orchestrator, interval_s, min_size_guard)
        cron_job.start()
```

**Сторожевое условие при старте:** если бэкенд Supabase и `db_ready=False` (нет связи, не применены миграции) — cron **не запускается**. Подсказка в логе: `"fix SUPABASE_URL/secrets or apply migrations; or CLUSTER_CRON_ENABLED=false"`.

**Цикл ожидания:**
```python
def _run_loop(self) -> None:
    while not self._stop_event.wait(max(self.interval_s, 1)):
        ...
```
`Event.wait(interval_s)` ждёт `interval_s` секунд **перед** каждым прогоном. Первый прогон — через `interval_s` секунд после старта, не мгновенно.

**Остановка** (ASGI lifespan shutdown):
```python
cron_job.stop()  # → _stop_event.set() + thread.join(timeout=max(interval_s, 1))
```
Graceful: ждёт завершения текущего прогона не дольше `interval_s` секунд, затем завершается.

### 9.3 Pre-run guard: min_size_guard

Перед вызовом `process_all_pending()` cron считает количество готовых историй:
```python
ready_count = len(repo.list_stories_ready_for_clustering())
# если ready_count < min_size_guard → пропустить прогон:
#   logs: cluster.batch_skipped_min_size
```
Смысл: не запускать кластеризацию, если историй меньше минимального порога — всё равно ни один кластер не пройдёт PromotionGates.

### 9.4 Обработка ошибок

Cron **никогда не падает** из-за ошибок в задаче. Вся кластеризация обёрнута в `try/except Exception`:

```python
try:
    issue_ids = self.orchestrator.process_all_pending()
    # → logs: cluster.cron_run_end created_issue_count=N failed_count=0
except Exception as exc:
    log_runtime_exception(logger, exc,
        stage="cluster.cron", run_id=run_id, duration_ms=elapsed_ms)
    # → logs: cluster.cron_run_end created_issue_count=0 failed_count=1
    # loop продолжается — следующий прогон через interval_s секунд
```

`log_runtime_exception()` (`src/core/logging_setup.py`) — структурированный лог с `stage`, `run_id`, `duration_ms` и traceback. После любого исключения (инфраструктурного, доменного, сетевого) loop **продолжается** со следующей итерацией.

**Параллельные прогоны** исключены через `_run_lock`:
```python
with self._run_lock:   # следующий прогон ждёт завершения текущего
    ...
```
Если прогон занимает больше `interval_s` (медленный DB) — следующий не запустится параллельно, а дождётся.

### 9.5 Наблюдаемость (log events)

| Событие | Когда |
|---------|-------|
| `cluster.cron_started` | Cron запущен, в extra: `interval_s`, `min_size_guard` |
| `cluster.cron_run_start` | Начало прогона, в extra: `run_id`, `ready_count`, `min_size_guard` |
| `cluster.batch_skipped_min_size` | Прогон пропущен: `ready_count < min_size_guard` |
| `cluster.cron_run_end` | Конец прогона: `created_issue_count`, `failed_count`, `duration_ms` |
| `cluster.cron_stopped` | Cron остановлен (ASGI shutdown) |
| `startup.cluster_cron_skipped` | DB не готова при старте; cron не запущен |

---

## 10. Гео-кластеризация — конфигурирование

### 10.1 Два параметра, два разных смысла

| Параметр | Роль | Момент применения |
|----------|------|-------------------|
| `CLUSTER_GEO_SCOPE` | Зона ответственности ноды — что **принимается** | Intake: `POST /intake/stories` |
| `CLUSTER_GEO_FILTER` | Гранулярность кластеров — как **делятся** принятые истории | Кластеризация: `cluster_key_for_lens()` |

### 10.2 Уровни гео-иерархии

Оба параметра используют одни и те же уровни (`src/core/geo/scope.py`):

| Уровень | `StoryGeoSnapshot` поле | Пример для Таллинна |
|---------|------------------------|---------------------|
| `district` | `admin_district` | `"lasnamäe"`, `"kesklinn"`, `"mustamäe"` |
| `settlement` | `admin_settlement` | `"tallinn"` |
| `region` | `admin_region` | `"harjumaa"` |
| `country` | `admin_country` | `"estonia"` |

Историческое значение `"any"` — алиас для `"country"`.

### 10.3 CLUSTER_GEO_SCOPE — intake gate

**Формат:** `<level>:<value>`, например `settlement:tallinn`.

**Что делает:**
```python
# src/core/api/handlers.py
if geo_scope is not None and location_query:
    resolved_geo = geo_service.resolve_for_story(location_query)
    assert_geo_in_scope(resolved_geo, level=scope_level, expected_value=scope_value)
    # → если geo не совпадает → GeoScopeMismatchError → 400 GEO_SCOPE_MISMATCH
```

Проверка срабатывает **только если**: CLUSTER_GEO_SCOPE задан **и** в intake-запросе передан непустой `narrative.location_query`. Story без `location_query` принимается всегда.

**Возможные значения:**

| Значение | Смысл |
|----------|-------|
| не задан (null) | Нода принимает истории из любого места — нет ограничения |
| `settlement:tallinn` | Нода принимает только истории из города Таллинн |
| `district:lasnamäe` | Нода принимает только истории из района Ласнамяэ |
| `region:harjumaa` | Нода принимает только истории из уезда Харьюмаа |
| `country:estonia` | Нода принимает только истории из Эстонии |

### 10.4 CLUSTER_GEO_FILTER — гранулярность кластеров

**Что делает:** добавляет гео-суффикс к каждому cluster_key:
```python
# src/core/cluster/engine.py
geo_part = geo_filter_bucket(profile.geo, geo_filter)
return f"{base}|{geo_part}"
```

Результирующий cluster_key: `"{lens}:{dimension}:{value}:{suffix}|geo:{level}:{token}"`

**Поведение по уровням:**

| Значение | Гео-часть ключа | Эффект на кластеры |
|----------|-----------------|-------------------|
| `country` (дефолт) | `geo:country:estonia` | Все истории из одной страны — в один кластер |
| `region` | `geo:region:harjumaa` | Истории Харьюмаа и Тартумаа — в разные кластеры |
| `settlement` | `geo:settlement:tallinn` | Таллинн и Нарва — в разные кластеры |
| `district` | `geo:district:lasnamäe` | Каждый район Таллинна — отдельный кластер |

**Истории без geo:**
- `geo is None` → `"geo:agnostic"` — все geo-less истории попадают в общий бакет, независимо от filter-уровня
- Гео есть, но нужный уровень пустой → `"geo:unknown"`

### 10.5 Пример: CLUSTER_GEO_SCOPE=settlement:tallinn + CLUSTER_GEO_FILTER=district

Конфигурация для Таллиннской публичной ноды:
```bash
CLUSTER_GEO_SCOPE=settlement:tallinn    # нода принимает только таллиннские истории
CLUSTER_GEO_FILTER=district            # внутри Таллинна кластеры делятся по районам
```

**Что происходит:**

1. **Intake:** история с `location_query="Narva mnt 5"` → geo resolve → `admin_settlement=narva` → `GeoScopeMismatchError` → 400. История из Нарвы не принята.

2. **Intake:** история с `location_query="Mustamäe tee 12"` → geo resolve → `admin_settlement=tallinn` → scope OK → story сохранена.

3. **Кластеризация:**
   - История из Ласнамяэ с `civic_domain=roads`: ключ = `civic_domain_micro:civic_domain:roads:micro|geo:district:lasname`
   - История из Кескlinна с `civic_domain=roads`: ключ = `civic_domain_micro:civic_domain:roads:micro|geo:district:kesklinn`
   - → **Два разных кластера**, не один. "Roads в Ласнамяэ" ≠ "Roads в Кескlinне".

4. **Результат в `GET /node/issues`:**
   - Issue: "Дорожные проблемы в Ласнамяэ" (civic_domain=roads, district=lasnamäe, 7 историй)
   - Issue: "Дорожные проблемы в Кескlinне" (civic_domain=roads, district=kesklinn, 3 истории)

### 10.6 Другие реальные конфигурации

**Нода одного города без районирования** — все жалобы на roads из любого района Таллинна в один кластер:
```bash
CLUSTER_GEO_SCOPE=settlement:tallinn
CLUSTER_GEO_FILTER=settlement    # → geo:settlement:tallinn для всех
```

**Страновая нода без гео-разделения** — глобальная агрегация по тематике:
```bash
# CLUSTER_GEO_SCOPE не задан
CLUSTER_GEO_FILTER=country       # дефолт — все Estonia в одном бакете
```

**Региональная нода** — две ноды для разных уездов, каждая кластеризует свои истории по районам:
```bash
# Нода Харьюмаа:
CLUSTER_GEO_SCOPE=region:harjumaa
CLUSTER_GEO_FILTER=district

# Нода Тартумаа:
CLUSTER_GEO_SCOPE=region:tartumaa
CLUSTER_GEO_FILTER=district
```

**Тестовая нода — без гео-ограничений:**
```bash
# CLUSTER_GEO_SCOPE не задан (принимает всё)
CLUSTER_GEO_FILTER=country       # кластеры без гео-разделения
CLUSTER_MIN_SIZE=1               # issue при первой же истории
```

---

## 11. Архитектурные ограничения текущей реализации

1. **Нет DB-backed signal persistence** — `story_signals` in-memory; при рестарте сигналы пересчитываются (`infer_signals_from_canonical` вызывается заново).
2. **Нет DB-backed cluster_memberships** — после рестарта membership history не восстанавливается.
3. **Нет chaos/failure тестов** — rollback lifecycle при `PromotionStateError` не покрыт тестами.

---

## 12. Сводная таблица состояния

| Компонент | Состояние | Примечание |
|-----------|-----------|------------|
| SignalDimension (6 civic) | Реализовано | CIVIC_DOMAIN, FAILURE_PATTERN, CIVIC_WEIGHT, DESIRED_OUTCOME, AFFECTED_GROUP, GEOGRAPHIC_DISTRICT |
| ClusterLens (6 civic) | Реализовано | Legacy lenses удалены (REQ-34, 2026-05-15) |
| infer_signals_from_canonical() | Реализовано | Единственная функция; language-agnostic |
| infer_signals_from_narrative() | Удалено | Удалена в REQ-34, 2026-05-15 |
| stable_cluster_id() SHA-256 | Реализовано | Cross-process deterministic |
| readiness_score_for_cluster() | Реализовано | Вычисляется по engine, передаётся в IssueCreateCommand |
| lens_readiness_bonus() | Реализовано | CIVIC_WEIGHT_SYSTEMIC +10, GEOGRAPHIC_DISTRICT_MICRO +5 |
| PromotionGatePolicy | Реализовано | min_stories=5, readiness_threshold=60 |
| canonical_type readiness gate | Реализовано | Кластер без `complaint`/`system_bug` → не промотируется |
| CLUSTER_PRIMARY_LENS | Реализовано | Именованный config, не active_lenses[0] |
| lifecycle: CLUSTERED | Реализовано | Все members → CLUSTERED после создания issue |
| Signal persistence in DB | Не реализовано | Пересчёт при каждом вызове; story_signals in-memory |
| Multi-lens intersection | Не реализовано | Архитектурная возможность |
