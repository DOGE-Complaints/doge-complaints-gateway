# 25. Целевое состояние Clustering Engine: техническая спецификация

## 1. Назначение и контекст

Документ описывает **эталонные технические требования** к подсистеме кластеризации stories в issues для `doge-complaints-gateway`. Базируется на:

- аудите реализации (`docs/analysis/clustering-audit-story-to-issue.md` 2026-04-30);
- продуктовой модели `07-dynamic-clusters-product-model.md`;
- решениях интервью `23-m2-demo-story-clustering-interview-ssot-v1.md`.

Тематическая фиксация (canonical_type → issue_type, canonical_labels → SpaLabel) — **вне scope этого документа**; описана в `23` и требует отдельной реализации.

| Атрибут | Значение |
|---------|----------|
| Scope | Механика кластеризации: ID, сигналы, линзы, persistence, idempotency, конфигурация |
| Статус | Целевое требование (to-be) |
| Зависимости | `22` (canonical поля в StoryRecord), `23` (пороги и env-принцип), `24` (read API) |

---

## 2. Инварианты системы (неизменяемые требования)

Следующие свойства обязательны при любом варианте реализации:

**INV-01 — Детерминизм cluster_id:** одинаковая пара `(lens, dimension_value)` всегда даёт одинаковый `cluster_id` — независимо от:
- перезапуска Python-процесса;
- версии Python;
- платформы / ОС.

**INV-02 — Персистентная стабильность:** `cluster_id`, сохранённый в БД в одном запуске, остаётся действительным идентификатором после рестарта сервиса.

**INV-03 — Идемпотентность создания issue:** повторный вызов `process_story()` для уже кластеризованных stories **не создаёт** дублирующих issue-кандидатов для того же кластера.

**INV-04 — Языковая нейтральность кластеризации:** две семантически идентичные истории на разных языках (ET/RU/EN) попадают в один кластер.

**INV-05 — Конфигурируемость порогов:** все численные пороги (`min_stories`, `readiness_threshold`) и выборы осей задаются исключительно через переменные окружения; не зашиты в бизнес-логику в виде литералов.

**INV-06 — Трассируемость:** каждый созданный issue содержит явную ссылку на `cluster_id` и список `story_ids`, по которым он построен.

---

## 3. Стабильный алгоритм формирования cluster_id

### 3.1 Требование

`cluster_id` формируется через криптографический хэш с фиксированным алгоритмом. Python's встроенный `hash()` **запрещён** (зависит от PYTHONHASHSEED — разные значения при каждом запуске процесса).

### 3.2 Спецификация алгоритма

```
input_string  = "{lens_value}:{cluster_key}"
digest_hex    = SHA-256(input_string, encoding=UTF-8).hexdigest()
numeric_part  = int(digest_hex, 16) % 10_000_000_000   # 10 знаков
cluster_id    = f"cluster:{lens_value}:{numeric_part:010d}"
```

Примеры:
```
lens_value   = "topic_micro"
cluster_key  = "topic_micro:topic:infrastructure:micro"
cluster_id   = "cluster:topic_micro:0837412956"   ← стабильно при любом перезапуске
```

### 3.3 Ключ кластера (cluster_key)

Ключ строится по формуле: `{lens_value}:{dimension_value}:{signal_value}:{scope_suffix}`.

Scope suffix по линзам:

| Lens | Suffix |
|------|--------|
| `topic_micro` | `micro` |
| `failure_micro` | `micro` |
| `repeatability_local` | `micro` |
| `need_local` | `local` |
| `failure_systemic` | `systemic` |
| `relevance_systemic` | `systemic` |

Ключ должен быть полностью строковым (без None, без пустых сегментов). Если значение сигнала отсутствует — используется строка `"unknown"`.

### 3.4 Эталонная реализация

```python
import hashlib

def stable_cluster_id(lens_value: str, cluster_key: str) -> str:
    raw = f"{lens_value}:{cluster_key}".encode("utf-8")
    digest = int(hashlib.sha256(raw).hexdigest(), 16) % 10_000_000_000
    return f"cluster:{lens_value}:{digest:010d}"
```

### 3.5 Тест на детерминизм (обязательный)

```python
def test_stable_cluster_id_is_cross_process_deterministic() -> None:
    """cluster_id должен быть одинаковым независимо от PYTHONHASHSEED."""
    lens = "topic_micro"
    key = "topic_micro:topic:infrastructure:micro"
    expected = "cluster:topic_micro:0837412956"  # pre-computed reference value
    assert stable_cluster_id(lens, key) == expected
    # Запустить с PYTHONHASHSEED=0 и PYTHONHASHSEED=random — результат одинаков
```

Конкретное эталонное число вычислить один раз при миграции и зафиксировать в тесте.

---

## 4. Словари и перечисления

### 4.1 SignalDimension — оси сигналов

| Ключ (enum value) | Смысл | Источник значений |
|-------------------|-------|------------------|
| `topic` | Тематическая область жалобы | GPT `canonical_labels` → маппинг; keyword fallback |
| `system_failure` | Тип системного сбоя | GPT `canonical_type` → маппинг; keyword fallback |
| `need` | Потребность гражданина | keyword matching (языко-нейтральный через canonical) |
| `desired_state` | Желаемый итог | константа `"stable_public_service"` до появления вариативности |
| `repeatability` | Повторяемость проблемы | keyword matching |
| `relevance` | Релевантность сигнала | константа `"high"` до появления scoring |

**Замечание:** `desired_state` и `relevance` на текущей стадии не несут вариативности. Линза `relevance_systemic` объединяет **все** stories в один кластер — её включение в `CLUSTER_ACTIVE_LENSES` по умолчанию не рекомендуется.

### 4.2 Допустимые значения по каждой оси

#### `topic`
| Значение | Смысловой критерий |
|----------|--------------------|
| `infrastructure` | Дороги, вода, мосты, освещение, инфраструктура ЖКХ |
| `public_service` | Государственные/муниципальные услуги не физической природы |
| `unknown` | Не удалось классифицировать |

#### `system_failure`
| Значение | Смысловой критерий |
|----------|--------------------|
| `service_disruption` | Полный сбой / прерывание услуги |
| `quality_gap` | Деградация качества без полного прерывания |
| `unknown` | Не удалось классифицировать |

#### `need`
| Значение | Смысловой критерий |
|----------|--------------------|
| `restore_access` | Доступ заблокирован, нужно восстановить |
| `resolve_issue` | Проблема есть, нужно устранить |
| `unknown` | Не удалось классифицировать |

#### `desired_state`
| Значение | Смысловой критерий |
|----------|--------------------|
| `stable_public_service` | Единственное значение на текущей стадии |

#### `repeatability`
| Значение | Смысловой критерий |
|----------|--------------------|
| `recurrent` | Проблема повторяется, подтверждена несколькими гражданами |
| `single_or_unknown` | Единичный случай или неизвестная история |

#### `relevance`
| Значение | Смысловой критерий |
|----------|--------------------|
| `high` | Единственное значение на текущей стадии |

### 4.3 ClusterLens — оси кластеризации

| Enum value | Dimension | Scope suffix | readiness_bonus | Рекомендуется по умолчанию |
|------------|-----------|--------------|-----------------|---------------------------|
| `topic_micro` | `topic` | `micro` | 0 | ✅ да |
| `need_local` | `need` | `local` | 0 | ✅ да |
| `failure_systemic` | `system_failure` | `systemic` | +5 | ✅ да |
| `failure_micro` | `system_failure` | `micro` | 0 | ✅ да |
| `repeatability_local` | `repeatability` | `micro` | 0 | ✅ да |
| `relevance_systemic` | `relevance` | `systemic` | +5 | ❌ нет — вырожденная |

`CLUSTER_ACTIVE_LENSES` по умолчанию: `topic_micro,need_local,failure_systemic,failure_micro,repeatability_local`.

### 4.4 IssueCandidateStatus (promotion state machine)

```
DRAFT → READY_FOR_REVIEW → IN_REVIEW → PROMOTED
                                     → REJECTED
```

Переходы строго упорядочены. Откат запрещён. `PROMOTED` — терминальный успешный статус.

---

## 5. Извлечение сигналов: источники и стратегия

### 5.1 Иерархия источников

```
Приоритет 1: GPT canonical (narrative_canonical_type, narrative_canonical_labels)
Приоритет 2: keyword-matching по narrative_original_text (English fallback)
Приоритет 3: значение "unknown"
```

Выбор источника управляется через `CLUSTER_SIGNAL_SOURCE` (см. раздел 8).

### 5.2 Маппинг GPT canonical → SignalDimension

#### `narrative_canonical_type` → `system_failure`

| GPT canonical_type | system_failure |
|--------------------|----------------|
| `INCIDENT` | `service_disruption` |
| `SERVICE_REQUEST` | `restore_access`* → `system_failure = service_disruption` |
| `IMPROVEMENT` | `quality_gap` |
| Иное / None | keyword fallback |

*Примечание: `SERVICE_REQUEST` → `need = restore_access`, `system_failure = quality_gap` семантически точнее, но итоговый маппинг требует согласования с doc 23 OP-01.

#### `narrative_canonical_labels[]` → `topic`

| GPT canonical_label | topic |
|---------------------|-------|
| `infrastructure` | `infrastructure` |
| `waste` | `public_service` |
| `safety` | `infrastructure` |
| `district` | `public_service` |
| Иное / пусто | keyword fallback |

Если несколько labels → берётся первый валидный маппинг.

### 5.3 Keyword-matching (fallback, English-only)

Применяется когда `CLUSTER_SIGNAL_SOURCE=keyword` или когда GPT-поля отсутствуют в `StoryRecord`.

Полный и верифицированный по коду набор ключевых слов (на момент аудита):

| Dimension | Ключевые слова (Python `in text`) | Значение при совпадении | Значение по умолчанию |
|-----------|----------------------------------|-------------------------|-----------------------|
| `topic` | `"road"`, `"water"` | `infrastructure` | `public_service` |
| `system_failure` | `"blocked"`, `"leak"` | `service_disruption` | `quality_gap` |
| `need` | `"blocked"` | `restore_access` | `resolve_issue` |
| `repeatability` | `"again"`, `"repeated"` | `recurrent` | `single_or_unknown` |

**Ограничение keyword-matching:** работает только с английским текстом. При эстонских и русских нарративах — дефолтные значения. Keyword-matching является устаревшим методом; замена на GPT canonical является целевым состоянием (см. INV-04).

### 5.4 Персистенция вычисленных сигналов

Сигналы **должны персистироваться** в БД при первом вычислении. При повторном обращении к story — читаются из хранилища.

Схема таблицы `story_signals`:

```sql
CREATE TABLE story_signals (
    story_id            TEXT        NOT NULL,
    extraction_policy   TEXT        NOT NULL,   -- e.g. "v1.keyword" | "v1.canonical"
    signals_json        JSONB       NOT NULL,   -- {"topic": "infrastructure", ...}
    extracted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (story_id, extraction_policy)
);
```

Ключ `(story_id, extraction_policy)` — позволяет хранить сигналы по разным версиям политики параллельно. При изменении политики старые записи остаются; новый проход записывает новую строку.

Protocol в domain layer:
```python
class StorySignalStore(Protocol):
    def save_signals(self, story_id: str, policy: str, signals: dict[str, str]) -> None: ...
    def get_signals(self, story_id: str, policy: str) -> dict[str, str] | None: ...
    def list_by_policy(self, policy: str) -> list[tuple[str, dict[str, str]]]: ...
```

---

## 6. Formulas для readiness score

### 6.1 Текущая формула (верифицирована по `engine.py:79-92`)

```python
size       = len(members)           # истории в кластере
base       = min(100, 20 + size * 15)
lens_bonus = 5  if lens in (FAILURE_SYSTEMIC, RELEVANCE_SYSTEMIC)  else 0
mode_bonus = 10 if mode == ClusteringMode.ISSUE_READY              else 0
score      = min(100, base + lens_bonus + mode_bonus)
```

### 6.2 Таблица base score по размеру кластера

| Кол-во stories | base | +FAILURE_SYSTEMIC | +ISSUE_READY |
|----------------|------|------------------|--------------|
| 1 | 35 | 40 | 45 |
| 2 | 50 | 55 | 60 |
| 3 | 65 | 70 | 75 |
| 4 | 80 | 85 | 90 |
| 5 | 95 | 100 | 100 |
| 6+ | 100 | 100 | 100 |

### 6.3 Целевой расчёт (исправление текущих проблем)

**Проблема 1:** `readiness_score` в `build_view()` вычисляется по наибольшему кластеру в линзе, не по кластеру target story.  
**Целевое поведение:** score вычисляется для каждого кластера отдельно и хранится в `Cluster`, а не в `ClusterView`.

**Проблема 2:** `ClusteringMode.ISSUE_READY` никогда не передаётся из orchestrator.  
**Целевое поведение:** при попытке создания issue orchestrator передаёт `ClusteringMode.ISSUE_READY` в вызове `build_view()` для целевого кластера.

**Проблема 3:** `readiness_score=100` захардкожен в orchestrator.  
**Целевое поведение:** orchestrator передаёт реально вычисленный score кластера в `IssueCreateCommand`.

### 6.4 Целевая структура Cluster

```python
@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    lens: ClusterLens
    members: tuple[ClusterMember, ...]
    readiness_score: int          # добавить
    readiness_factors: dict[str, int]  # добавить
```

---

## 7. Idempotency: предотвращение дублирования issues

### 7.1 Механизм: lifecycle истории

**Целевое состояние:** после успешного создания и промоции issue все story в кластере переходят в статус `CLUSTERED`.

```python
class StoryLifecycleStatus(StrEnum):
    ACCEPTED = "accepted"
    PARTIAL_READY = "partial_ready"
    READY_FOR_PROFILE = "ready_for_profile"
    CLUSTERED = "clustered"        # новый статус
```

Переход `READY_FOR_PROFILE → CLUSTERED` производится в orchestrator после получения `issue_id`.

После перехода story исключается из `list_stories_ready_for_clustering()` → повторная обработка невозможна.

### 7.2 Правило: story может участвовать в нескольких issues (N:M, doc 23 D-10)

Story может попасть в разные кластеры по разным линзам → несколько issues. Переход в `CLUSTERED` происходит когда story включена хотя бы в один активный issue. Если продукт потребует полного N:M — решение фиксировать в doc 23.

### 7.3 Механизм: cluster_id deduplication в promotion layer (резервный)

Дополнительная защита: перед созданием нового candidate проверять, существует ли уже `PROMOTED` кандидат с тем же `cluster_id`.

```python
# IssueCandidateStore protocol — добавить метод:
def find_promoted_by_cluster_id(self, cluster_id: str) -> IssueCandidateRecord | None: ...
```

В orchestrator:
```python
existing = promotion_service.find_promoted_by_cluster_id(cluster_id)
if existing is not None:
    return existing.candidate_id  # идемпотентный возврат
```

### 7.4 Story lifecycle advancement — обязательный, не резервный

Cluster_id deduplication (7.3) является резервной мерой. **Основная** мера — lifecycle advancement (7.1). Обе должны быть реализованы.

---

## 8. Конфигурация через переменные окружения

### 8.1 Полный реестр переменных кластеризации

| Переменная | Тип | Default | Валидация | Статус |
|------------|-----|---------|-----------|--------|
| `CLUSTER_MIN_SIZE` | int > 0 | `8` | parse_positive_int | ✅ реализовано |
| `CLUSTER_READINESS_THRESHOLD` | int 1-100 | `70` | range check | ✅ реализовано (bypassed) |
| `CLUSTER_ACTIVE_LENSES` | comma-list | см. 4.3 | enum validation | ✅ реализовано |
| `CLUSTER_GEO_FILTER` | str | `"any"` | — | ⚠️ заглушка |
| `CLUSTER_TIE_BREAKER` | str | `"lexical"` | — | ⚠️ заглушка |
| `CLUSTER_TYPE_RESOLUTION` | str | `"canonical_priority"` | — | ⚠️ заглушка |
| `CLUSTER_SIGNAL_SOURCE` | enum | `"canonical"` | enum validation | 🆕 добавить |
| `CLUSTER_PRIMARY_LENS` | str | `"topic_micro"` | enum in ACTIVE_LENSES | 🆕 добавить |
| `CLUSTER_ID_ALGORITHM` | enum | `"sha256"` | enum validation | 🆕 добавить |

### 8.2 Новые переменные: спецификация

#### `CLUSTER_SIGNAL_SOURCE`

```
Тип: enum
Допустимые значения: "canonical" | "keyword" | "hybrid"
Default: "canonical"
Семантика:
  canonical — только GPT canonical_type / canonical_labels; отсутствие → "unknown"
  keyword   — только keyword-matching по narrative_original_text (legacy)
  hybrid    — сначала canonical, при отсутствии — keyword fallback
```

Валидация при старте:
```python
_ALLOWED_SIGNAL_SOURCES = frozenset({"canonical", "keyword", "hybrid"})
if cluster_signal_source not in _ALLOWED_SIGNAL_SOURCES:
    raise ConfigError(...)
```

#### `CLUSTER_PRIMARY_LENS`

```
Тип: str (один lens value)
Допустимые значения: любое значение из CLUSTER_ACTIVE_LENSES
Default: "topic_micro"
Семантика: определяет, по какому линзу создаётся issue-кандидат
Валидация: значение должно присутствовать в CLUSTER_ACTIVE_LENSES
```

Заменяет текущий `active_lenses[0]` — явная, именованная конфигурация вместо неявной позиционной.

#### `CLUSTER_ID_ALGORITHM`

```
Тип: enum
Допустимые значения: "sha256" | "legacy_hash"
Default: "sha256"
Семантика:
  sha256       — SHA-256 based, cross-process stable (требование INV-01)
  legacy_hash  — Python hash() для обратной совместимости с существующими данными в БД
                 НЕ рекомендуется для новых установок
```

Предусмотрен режим `legacy_hash` для migration path: существующие development/test данные в БД могут иметь hash-based IDs.

### 8.3 Переменные-заглушки: целевой смысл

#### `CLUSTER_GEO_FILTER`

```
Целевая семантика: "any" | "{normalized_label}"
"any"              — кластеризовать stories из любого гео-района
"{normalized_label}" — только stories с matching StoryGeoSnapshot.normalized_label
Зависимость: требует персистенции StoryGeoSnapshot (GAP-IMP-03)
```

#### `CLUSTER_TIE_BREAKER`

```
Целевая семантика: "lexical" | "oldest_first" | "systemic_priority"
"lexical"          — при равном count → кластер с наименьшим lexicographic cluster_id
"oldest_first"     — кластер с наиболее ранней story.created_at
"systemic_priority" — предпочитать linz с systemic scope (failure_systemic, relevance_systemic)
```

#### `CLUSTER_TYPE_RESOLUTION`

```
Целевая семантика: "canonical_priority" | "majority" | "first"
"canonical_priority" — использовать canonical_type если все stories в кластере согласны
"majority"          — canonical_type из большинства stories
"first"             — canonical_type первой (oldest) story в кластере
```

---

## 9. Персистентная модель данных кластеризации

### 9.1 Схема таблиц

#### `story_signals` (новая)
```sql
CREATE TABLE story_signals (
    story_id            TEXT        NOT NULL,
    extraction_policy   TEXT        NOT NULL,
    signals_json        JSONB       NOT NULL,
    extracted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (story_id, extraction_policy)
);
CREATE INDEX idx_story_signals_policy ON story_signals(extraction_policy);
```

#### `cluster_memberships` (новая, аналитическая)
```sql
CREATE TABLE cluster_memberships (
    story_id     TEXT        NOT NULL,
    lens         TEXT        NOT NULL,
    cluster_id   TEXT        NOT NULL,
    computed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (story_id, lens)
);
CREATE INDEX idx_cluster_memberships_cluster ON cluster_memberships(cluster_id);
```

Назначение: позволяет быстро найти все stories в кластере без пересчёта; поддерживает read API.

#### `issue_story_links` (уже существует в коде)
```sql
-- существующая таблица, верифицирована по infrastructure/repositories.py
CREATE TABLE issue_story_links (
    issue_id     TEXT        NOT NULL,
    cluster_id   TEXT        NOT NULL,
    story_id     TEXT        NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (issue_id, story_id)
);
CREATE INDEX idx_issue_story_links_cluster ON issue_story_links(cluster_id);
```

#### Расширение `stories` — статус `CLUSTERED`
```sql
ALTER TABLE stories
  ADD CONSTRAINT stories_lifecycle_check
  CHECK (lifecycle_status IN ('accepted','partial_ready','ready_for_profile','clustered'));
```

### 9.2 Протоколы доменного слоя (новые)

```python
class StorySignalStore(Protocol):
    def save_signals(self, story_id: str, policy: str, signals: dict[str, str]) -> None: ...
    def get_signals(self, story_id: str, policy: str) -> dict[str, str] | None: ...

class ClusterMembershipStore(Protocol):
    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None: ...
    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]: ...

# Дополнение к IssueCandidateStore:
class IssueCandidateStore(Protocol):
    ...
    def find_promoted_by_cluster_id(self, cluster_id: str) -> IssueCandidateRecord | None: ...
```

### 9.3 Обновление lifecycle после issue creation

```python
class StoryRepository(Protocol):
    ...
    def list_stories_ready_for_clustering(self) -> list[StoryRecord]: ...
    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None: ...
```

`list_stories_ready_for_clustering()` — фильтрует по `lifecycle_status = READY_FOR_PROFILE` **на уровне DB query**, не в Python. Устраняет полный скан таблицы.

---

## 10. Orchestrator: целевая последовательность

```python
def process_story(self, story_id: str) -> str | None:
    # 1. guard: story существует и в правильном статусе
    target = self.story_repository.get_story(story_id)
    if target is None or target.lifecycle_status is not StoryLifecycleStatus.READY_FOR_PROFILE:
        return None

    # 2. загрузить только READY_FOR_PROFILE stories (DB-side filter)
    ready_stories = self.story_repository.list_stories_ready_for_clustering()
    if not ready_stories:
        return None

    # 3. получить сигналы (из кэша или вычислить)
    profiles = tuple(
        StoryProfileSignals(
            story_id=item.story_id,
            signals=self._get_or_compute_signals(item),
        )
        for item in ready_stories
    )

    # 4. кластеризовать
    memberships = self.clustering_engine.memberships(profiles)
    if story_id not in memberships:
        return None

    # 5. выбрать primary lens (из конфига, не active_lenses[0])
    primary_lens = self.config.cluster_primary_lens
    cluster_id = memberships[story_id].get(primary_lens)
    if cluster_id is None:
        return None

    # 6. idempotency check: уже существует promoted issue?
    existing = self.promotion_service.find_promoted_by_cluster_id(cluster_id)
    if existing is not None:
        return existing.candidate_id

    # 7. собрать членов кластера
    member_story_ids = tuple(
        p.story_id for p in profiles
        if memberships.get(p.story_id, {}).get(primary_lens) == cluster_id
    )

    # 8. вычислить readiness score для кластера (не hardcode 100)
    readiness = self.clustering_engine.compute_readiness(
        lens=primary_lens,
        story_count=len(member_story_ids),
        mode=ClusteringMode.ISSUE_READY,
    )

    # 9. создать issue
    issue_title = target.narrative_title_hint or f"cluster:{primary_lens}"
    try:
        result = self.issue_create_service.create_issue(
            IssueCreateCommand(
                cluster_id=cluster_id,
                story_ids=member_story_ids,
                readiness_score=readiness,
                title=issue_title,
            )
        )
    except (ValueError, PromotionStateError):
        return None

    # 10. advance lifecycle для всех stories в кластере
    for sid in member_story_ids:
        self.story_repository.update_lifecycle_status(
            sid, StoryLifecycleStatus.CLUSTERED
        )

    # 11. persist cluster memberships
    for sid in member_story_ids:
        self.cluster_membership_store.save_membership(sid, primary_lens, cluster_id)

    return result.issue_id
```

---

## 11. Observability и логирование

### 11.1 Обязательные события

| Событие | Уровень | Поля |
|---------|---------|------|
| issue создан при intake | INFO | `story_id`, `issue_id`, `cluster_id`, `lens`, `story_count`, `readiness_score` |
| gate не прошёл | INFO | `story_id`, `cluster_id`, `gate_reason`, `story_count`, `readiness_score`, `threshold` |
| idempotency hit | DEBUG | `story_id`, `cluster_id`, `existing_issue_id` |
| signal source используется | DEBUG | `story_id`, `signal_source` (`canonical`\|`keyword`\|`hybrid`) |
| кластеризация пропущена | DEBUG | `story_id`, `reason` (`not_ready`\|`no_cluster`\|`empty_stories`) |

### 11.2 Исправление silent discard в handlers.py

```python
# handlers.py — целевой код:
issue_id = dependencies.story_cluster_orchestrator.process_story(story.story_id)
if issue_id:
    log_api_event(
        logging.INFO, "story_cluster_issue_created",
        trace_id=resolved_trace_id,
        story_id=story.story_id,
        issue_id=issue_id,
        outcome="clustered",
    )
else:
    log_api_event(
        logging.DEBUG, "story_cluster_issue_pending",
        trace_id=resolved_trace_id,
        story_id=story.story_id,
        outcome="not_clustered",
    )
```

---

## 12. Конфигурация ClusteringEngine: расширение

### 12.1 Целевые параметры

```python
@dataclass(frozen=True)
class ClusteringEngine:
    active_lenses: tuple[ClusterLens, ...]
    primary_lens: ClusterLens           # из CLUSTER_PRIMARY_LENS
    id_algorithm: str                   # "sha256" | "legacy_hash"
    signal_source: str                  # "canonical" | "keyword" | "hybrid"
    geo_filter: str                     # "any" | normalized_label
    tie_breaker: str                    # "lexical" | "oldest_first" | "systemic_priority"
    type_resolution: str                # "canonical_priority" | "majority" | "first"
```

### 12.2 Фабрика (service_factory.py)

```python
def get_clustering_engine(self) -> ClusteringEngine:
    return ClusteringEngine(
        active_lenses=tuple(ClusterLens(l) for l in self.config.cluster_active_lenses),
        primary_lens=ClusterLens(self.config.cluster_primary_lens),
        id_algorithm=self.config.cluster_id_algorithm,
        signal_source=self.config.cluster_signal_source,
        geo_filter=self.config.cluster_geo_filter,
        tie_breaker=self.config.cluster_tie_breaker,
        type_resolution=self.config.cluster_type_resolution,
    )
```

Все параметры должны быть переданы из `AppConfig` в `ClusteringEngine` при конструировании — не подхватываться из env напрямую внутри engine.

---

## 13. Acceptance criteria

### AC-01 — Детерминизм cluster_id
- [ ] cluster_id для одинакового `(lens, dimension_value)` одинаков при 100 последовательных запусках с разными PYTHONHASHSEED
- [ ] тест `test_stable_cluster_id_is_cross_process_deterministic()` проходит

### AC-02 — Idempotency
- [ ] 10 последовательных intake одинакового нарратива создают ровно 1 issue (не 10)
- [ ] тест `test_process_story_idempotent_no_duplicate_issues()` проходит

### AC-03 — Lifecycle advancement
- [ ] после создания issue stories в кластере имеют статус `CLUSTERED`
- [ ] `list_stories_ready_for_clustering()` не возвращает `CLUSTERED` stories

### AC-04 — Readiness score
- [ ] `IssueCreateCommand.readiness_score` не равен 100 для кластеров с <5 stories
- [ ] `CLUSTER_READINESS_THRESHOLD=80` реально блокирует кластер из 2 stories (base=50 < 80)

### AC-05 — CLUSTER_PRIMARY_LENS
- [ ] при `CLUSTER_PRIMARY_LENS=failure_systemic` issue создаётся по линзу `failure_systemic`
- [ ] cluster_id в `issue_story_links` начинается с `cluster:failure_systemic:`

### AC-06 — Языковая нейтральность (при CLUSTER_SIGNAL_SOURCE=canonical)
- [ ] ET-нарратив и EN-нарратив с одинаковым `canonical_type=INCIDENT` попадают в один кластер `failure_systemic`

### AC-07 — Observability
- [ ] `grep "story_cluster_issue_created"` в логах находит запись с `issue_id` при успешном intake
- [ ] `grep "story_cluster_issue_pending"` находит запись при intake с недостаточным кластером

### AC-08 — Персистенция сигналов
- [ ] повторный intake той же story читает сигналы из `story_signals`, не пересчитывает
- [ ] `story_signals` содержит ровно 1 строку per (story_id, policy) после первого compute

---

## 14. Трассировка

| Зона | Файл / задача |
|------|---------------|
| hash → sha256 migration | `TASK-CLUSTER-STABLE-ID-01` |
| Idempotency + lifecycle CLUSTERED | `TASK-CLUSTER-IDEMPOTENCY-01` |
| CLUSTER_PRIMARY_LENS + CLUSTER_SIGNAL_SOURCE env | `TASK-CLUSTER-CONFIG-EXPAND-01` |
| story_signals persistence | `TASK-CLUSTER-SIGNAL-PERSIST-01` |
| Observability (handlers.py logging) | `TASK-CLUSTER-OBSERVABILITY-01` |
| cluster_memberships table | `TASK-CLUSTER-MEMBERSHIP-PERSIST-01` |
| list_stories_ready_for_clustering (DB-side filter) | `TASK-CLUSTER-REPO-FILTER-01` |
| Продуктовая рамка кластеров | `07-dynamic-clusters-product-model.md` |
| Demo-параметры и env-принцип | `23-m2-demo-story-clustering-interview-ssot-v1.md` |
| Аудит текущей реализации | `docs/analysis/clustering-audit-story-to-issue.md` |

---

## 15. Gap Analysis: текущее состояние vs. спецификация (аудит 2026-05-05)

Аудит проведён по фактическому коду. Статусы — **факты из кода**, не предположения.

### 15.1 Статус реализации

| Требование (раздел) | Статус | Файл / строка |
|--------------------|--------|---------------|
| `CLUSTERED` lifecycle статус (7.1) | ✅ | `src/core/domain/contracts.py:24` |
| readiness_score не захардкожен (6.3) | ✅ | `src/core/cluster/engine.py` — `readiness_for_story()` |
| `list_stories_ready_for_clustering()` на DB-уровне (9.3) | ✅ | `src/core/infrastructure/db_sqlite.py` — `WHERE lifecycle_status = ?` |
| `story_signals` таблица в SQLite DDL (9.1) | ✅ | `src/core/infrastructure/db_sqlite.py:209-226` |
| `cluster_memberships` таблица в SQLite DDL (9.1) | ✅ | `src/core/infrastructure/db_sqlite.py` |
| SHA-256 алгоритм — реализован (3.4) | ✅ | `src/core/cluster/engine.py` — `stable_cluster_id()` |
| Тест на детерминизм SHA-256 (3.5) | ✅ | `tests/test_clustering_engine.py:131` |
| `CLUSTER_SIGNAL_SOURCE` env var (8.1) | ✅ | `src/core/config/schema.py` |
| `CLUSTER_PRIMARY_LENS` env var (8.1) | ✅ | `src/core/config/schema.py` |
| `CLUSTER_ID_ALGORITHM` env var (8.1) | ✅ | `src/core/config/schema.py` |
| **`CLUSTER_ID_ALGORITHM` default = `"sha256"` (8.2)** | ❌ | `src/core/config/schema.py` — дефолт `"legacy_hash"` |
| **`story_signals` в Supabase bootstrap (9.1)** | ❌ | `supabase/bootstrap/000_full_init.sql` — отсутствует |
| **`cluster_memberships` в Supabase bootstrap (9.1)** | ❌ | `supabase/bootstrap/000_full_init.sql` — отсутствует |
| **Idempotency check через `find_promoted_by_cluster_id` (7.3)** | ❌ | Метод есть в 3 backends, orchestrator не вызывает |
| Logging event names (11.2) | ⚠️ | `src/core/api/handlers.py` — имена событий отличаются от spec |

### 15.2 Незакрытые пункты → задачи

| GAP-ID | Проблема | Файл | Задача |
|--------|---------|------|--------|
| GAP-25-01 | `CLUSTER_ID_ALGORITHM` default = `"legacy_hash"` вместо `"sha256"` | `src/core/config/schema.py` | `TASK-CLUSTER-CONFIG-DEFAULT-01` |
| GAP-25-02 | `story_signals` отсутствует в Supabase bootstrap | `supabase/bootstrap/000_full_init.sql` | `TASK-CLUSTER-SUPABASE-SCHEMA-01` |
| GAP-25-03 | `cluster_memberships` отсутствует в Supabase bootstrap | `supabase/bootstrap/000_full_init.sql` | `TASK-CLUSTER-SUPABASE-SCHEMA-01` (совмещается) |
| GAP-25-04 | Orchestrator не вызывает `find_promoted_by_cluster_id` (INV-03) | `src/core/application/cluster_orchestrator.py` | покрывается req29 |
| GAP-25-05 | Logging event names не соответствуют spec (11.2) | `src/core/api/handlers.py` | `TASK-CLUSTER-OBSERVABILITY-01` |

### 15.3 Рекомендуемый порядок закрытия

1. **GAP-25-01** — одна строка в `schema.py`, нулевой риск; нужно для корректного default behavior на новых установках
2. **GAP-25-02 + GAP-25-03** — один SQL блок в bootstrap; нужен для Supabase fresh install и полноты схемы
3. **GAP-25-04** — покрывается реализацией req29 (living issues); отдельная задача не нужна
4. **GAP-25-05** — низкий приоритет, не блокирует функциональность
