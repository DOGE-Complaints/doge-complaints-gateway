# 30. Кластеризация и модель линз: обрамляющий контекст

> **Назначение документа.** Самодостаточный вводный текст для нового собеседника или нового агента без контекста проекта. Цель — дать понятийную базу для работы с документами `25-clustering-engine-target-state-spec.md` и `26-clustering-signal-axes-from-gpt-taxonomy.md`. Все технические утверждения верифицированы по фактическому коду репозитория `doge-complaints-gateway`.

---

## 1. Контекст проекта: о чём этот сервис

**DOGEstonia** (`doge-complaints-gateway`) — это Python/FastAPI сервис, который:

1. Принимает гражданские жалобы от жителей Таллинна через API (`POST /intake/stories`). Жалоба называется **story** — свободный текст на эстонском, русском или английском: "Яма на Нарвском шоссе не ремонтируется уже год".

2. Обрабатывает накопленные stories через механизм **кластеризации** — находит группы похожих историй.

3. Создаёт из кластеров **DOGEIssue** — публичную карточку гражданской проблемы с i18n-заголовком, типом, метками и readiness score.

4. Отдаёт эти issues через read API (`GET /tallinn/issues`) — SPA фронтенд и государственные потребители читают issues, не сырые stories.

**Итог:** сервис превращает поток неструктурированных жалоб в классифицированные, приоритизированные проблемы.

---

## 2. Что такое Story в коде

`StoryRecord` (`src/core/domain/contracts.py`) — центральный объект домена:

```python
@dataclass(frozen=True)
class StoryRecord:
    story_id: str
    narrative_original_text: str          # свободный текст жалобы
    narrative_canonical_type: str | None  # GPT: INCIDENT | SERVICE_REQUEST | IMPROVEMENT
    narrative_canonical_labels: tuple[str, ...]  # GPT: ["roads", "broken_infrastructure", "systemic_pattern"]
    lifecycle_status: StoryLifecycleStatus       # ACCEPTED → READY_FOR_PROFILE → CLUSTERED
    geo: StoryGeoSnapshot | None                 # нормализованный район: "lasnamäe"
    ...
```

Ключевые поля для кластеризации:
- `narrative_canonical_labels` — нормализованные теги от GPT (языко-нейтральные)
- `narrative_canonical_type` — архетип жалобы (инцидент / запрос / улучшение)
- `geo.normalized_label` — административный район

Story участвует в кластеризации только в статусе `READY_FOR_PROFILE`. После создания issue переходит в `CLUSTERED` и выбывает из следующих прогонов.

---

## 3. Что такое Signal

**Сигнал** — это атомарная классификационная характеристика story, нормализованная к фиксированному словарю.

Пример: из текста "Яма на Нарвском шоссе — третий год не чинят, соседи тоже жалуются" извлекается набор сигналов:

```
civic_domain     = "roads"
failure_pattern  = "broken_infrastructure"
civic_weight     = "not_only_me"
desired_outcome  = "better_maintenance"
affected_group   = "residents"
geographic_district = "lasnamäe"
```

Сигналы — это **нормализованный язык**, в котором разные тексты на разных языках становятся одинаковыми векторами. История на эстонском "Tänav on katki, naabrid kurdavad ka" с теми же GPT-метками даст идентичный набор сигналов.

### Как сигналы извлекаются: два метода

**Метод 1 — keyword-matching** (legacy, `infer_signals_from_narrative`):

```python
# src/core/profile/enrichment.py:16-44
inferred["topic"] = "infrastructure" if "road" in text else "public_service"
inferred["system_failure"] = "service_disruption" if "blocked" in text else "quality_gap"
```

Проблема: работает только с английским текстом. Эстонская и русская жалоба всегда получают дефолтные значения.

**Метод 2 — canonical lookup** (целевой, `infer_signals_from_canonical`):

```python
# src/core/profile/enrichment.py:47-88
def infer_signals_from_canonical(canonical_type, canonical_labels, geo_normalized_label):
    civic_domain = next(
        (label for label in canonical_labels if label in CIVIC_DOMAIN_VOCABULARY),
        "unknown",
    )
    ...
```

GPT нормализует текст любого языка в canonical_labels → lookup по vocabulary → сигнал. Языковая нейтральность обеспечивается GPT, а не кодом gateway.

### Откуда берётся canonical_labels

GPT (отдельный сервис, GPT UI) во время разговора с гражданином присваивает story нормализованные метки из контролируемого словаря. Словарь зафиксирован в `src/core/cluster/vocabulary.py`:

```python
CIVIC_DOMAIN_VOCABULARY: frozenset[str] = frozenset({
    "transport", "roads", "parking", "public_space", "waste",
    "environment", "housing", "education", "healthcare",
    "digital_service", "safety", "accessibility",
})

FAILURE_PATTERN_VOCABULARY: frozenset[str] = frozenset({
    "delay", "access_blocked", "information_gap", "broken_infrastructure",
    "unsafe_condition", "bureaucratic_loop", "unclear_rules",
    "service_unavailable", "maintenance_gap",
})

CIVIC_SIGNAL_PRIORITY: tuple[str, ...] = (
    "systemic_pattern", "public_cost", "not_only_me", "recurring_issue",
    "equity_access", "trust_in_services", "city_for_people",
)
```

---

## 4. Что такое Кластер

**Кластер** — это группа stories, у которых значение одного конкретного сигнала совпадает.

Пример: все истории с `civic_domain = "roads"` → один кластер. Все истории с `failure_pattern = "broken_infrastructure"` → другой кластер. **Одна история может одновременно быть в нескольких кластерах** — по разным сигналам.

В коде (`src/core/cluster/types.py`):

```python
@dataclass(frozen=True)
class Cluster:
    cluster_id: str              # "cluster:civic_domain_micro:0473821956"
    lens: ClusterLens            # какая линза создала этот кластер
    members: tuple[ClusterMember, ...]  # story_ids в кластере
    readiness_score: int         # зрелость кластера (0-100)
    key: str                     # "civic_domain_micro:civic_domain:roads:micro"
```

`cluster_id` формируется через SHA-256 от строки `"{lens}:{key}"` → детерминистичен и стабилен между перезапусками:

```python
# src/core/cluster/engine.py:94-100
def stable_cluster_id(lens, key, *, id_algorithm="legacy_hash"):
    if id_algorithm == "sha256":
        digest_hex = hashlib.sha256(f"{lens.value}:{key}".encode()).hexdigest()
        numeric = int(digest_hex, 16) % 10_000_000_000
        return f"cluster:{lens.value}:{numeric:010d}"
```

---

## 5. Что такое Линза — ключевая концепция

**Линза (ClusterLens)** — это вопрос, который задаётся набору stories при кластеризации.

Один и тот же набор stories даёт разные кластеры в зависимости от того, какой вопрос задаётся:

| Линза | Вопрос | Ответ (ось группировки) | Кластер |
|-------|--------|------------------------|---------|
| `civic_domain_micro` | О чём эта жалоба? | `civic_domain` | "roads" |
| `failure_pattern_micro` | Как именно ломается? | `failure_pattern` | "broken_infrastructure" |
| `civic_weight_systemic` | Насколько это системно? | `civic_weight` | "systemic_pattern" |

Семь историй о дорогах в Ласнамяэ создадут **три cluster_id** — по одному в каждой линзе:

```
civic_domain_micro:roads:micro      → cluster:civic_domain_micro:0473821956
failure_pattern_micro:broken_infrastructure:micro  → cluster:failure_pattern_micro:1827364501
civic_weight_systemic:systemic_pattern:systemic    → cluster:civic_weight_systemic:0912847365
```

Это правильное поведение N:M: одна story участвует в нескольких issues по разным линзам.

### Анатомия линзы

Каждая линза — это пара из трёх компонентов:

```
{имя_линзы} = {SignalDimension} × {scope_suffix}

civic_domain_micro  =  CIVIC_DOMAIN  ×  micro
failure_systemic    =  SYSTEM_FAILURE × systemic
civic_weight_systemic = CIVIC_WEIGHT × systemic
```

**SignalDimension** — это ось (из какого сигнала брать значение для группировки).
**scope_suffix** (micro / local / systemic) — это семантический масштаб кластера:

| Suffix | Смысл | Пример линзы |
|--------|-------|-------------|
| `micro` | Конкретная, детальная проблема | `civic_domain_micro` = конкретный домен |
| `local` | Районный / локальный масштаб | `need_local` = локальная потребность |
| `systemic` | Системный паттерн, не единичный | `civic_weight_systemic` = все "systemic_pattern" |

В коде это выражено явным маппингом `engine.py:62-77`:

```python
def lens_dimension(lens: ClusterLens) -> SignalDimension:
    mapping = {
        ClusterLens.CIVIC_DOMAIN_MICRO:    SignalDimension.CIVIC_DOMAIN,
        ClusterLens.FAILURE_PATTERN_MICRO: SignalDimension.FAILURE_PATTERN,
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC: SignalDimension.CIVIC_WEIGHT,
        ClusterLens.DESIRED_OUTCOME_LOCAL: SignalDimension.DESIRED_OUTCOME,
        ...
    }
```

### Почему несколько линз, а не одна

Одна история — несколько ролей в обществе. Один кластер не может одновременно отвечать на вопросы трёх аудиторий:

| Аудитория | Их вопрос | Нужная линза |
|-----------|-----------|-------------|
| **Житель** | Я не один? | `civic_domain_micro` — "14 человек жалуются на roads" |
| **Государство** | Что и где чинить? | `failure_pattern_micro` × `geographic_district_micro` |
| **Бизнес / НКО** | Где незакрытый спрос? | `desired_outcome_local` = "digital_fix" — 8 историй |

Линза — это **угол зрения на один и тот же массив данных**. Меняется линза — меняется разбиение на кластеры, меняется смысл для читателя.

---

## 6. Как линза создаёт cluster_key

Алгоритм `cluster_key_for_lens` (`engine.py:80-91`):

```python
def cluster_key_for_lens(profile: StoryProfileSignals, lens: ClusterLens) -> str:
    signals = profile.signals                     # {"civic_domain": "roads", ...}
    dimension = lens_dimension(lens)              # SignalDimension.CIVIC_DOMAIN
    raw_value = signals.get(dimension.value, "unknown")  # "roads"

    if lens in _SYSTEMIC_LENSES:
        return f"{lens.value}:{dimension.value}:{raw_value}:systemic"
    if lens in _MICRO_LENSES:
        return f"{lens.value}:{dimension.value}:{raw_value}:micro"
```

Результат для примера: `"civic_domain_micro:civic_domain:roads:micro"`

Все stories с одинаковым cluster_key → один кластер. Разный cluster_key → разные кластеры.

---

## 7. Как engine работает: метод memberships

Центральный метод `ClusteringEngine.memberships` (`engine.py:249-268`):

```python
def memberships(self, profiles: tuple[StoryProfileSignals, ...]) -> dict[str, dict[str, str]]:
    """Map story_id -> {lens_name: cluster_id} for all active lenses."""
    result = {}
    for lens in self.active_lenses:          # итерируем по каждой активной линзе
        view = self.build_view(lens=lens, profiles=profiles, mode=ClusteringMode.ISSUE_READY)
        for cluster in view.clusters:
            for member in cluster.members:
                result.setdefault(member.story_id, {})[lens.value] = cluster.cluster_id
    return result
```

Входные данные: список `StoryProfileSignals` (story_id + словарь сигналов).
Выходные данные: словарь `{story_id: {lens_name: cluster_id}}`.

Пример вывода для трёх stories:

```python
{
    "story_abc": {
        "civic_domain_micro":  "cluster:civic_domain_micro:0473821956",
        "failure_pattern_micro": "cluster:failure_pattern_micro:1827364501",
    },
    "story_def": {
        "civic_domain_micro":  "cluster:civic_domain_micro:0473821956",  # тот же кластер
        "failure_pattern_micro": "cluster:failure_pattern_micro:9923847102",  # другой failure
    },
    "story_xyz": {
        "civic_domain_micro":  "cluster:civic_domain_micro:7712309854",  # другой домен
    }
}
```

---

## 8. Readiness Score: как кластер становится issue

Кластер не сразу становится публичным issue — он должен набрать достаточно зрелости. Формула из `engine.py:155-169`:

```python
def readiness_score_for_cluster(lens, members, mode):
    size       = len(members)
    base       = min(100, 20 + size * 15)    # растёт с числом историй
    lens_bonus = lens_readiness_bonus(lens)   # CIVIC_WEIGHT_SYSTEMIC → +10, FAILURE_SYSTEMIC → +5
    mode_bonus = 10 if mode == ClusteringMode.ISSUE_READY else 0
    score      = min(100, base + lens_bonus + mode_bonus)
    return score, factors
```

Таблица base score:

| Историй в кластере | base | +civic_weight_systemic | итого |
|-------------------|------|----------------------|-------|
| 1 | 35 | +10 | 45 |
| 2 | 50 | +10 | 60 |
| 3 | 65 | +10 | 75 |
| 4 | 80 | +10 | 90 |
| 5+ | 95+ | +10 | 100 |

`CLUSTER_READINESS_THRESHOLD` (env var, дефолт 60) — порог, выше которого кластер идёт на создание issue. Кластер из 2 systemic историй (score=60) пройдёт при threshold=60, но не пройдёт при threshold=70.

Логика `civic_weight_systemic` бонуса: `lens_readiness_bonus` (`engine.py:112-125`):

```python
def lens_readiness_bonus(lens: ClusterLens) -> int:
    high_bonus = frozenset({ClusterLens.CIVIC_WEIGHT_SYSTEMIC})
    med_bonus  = frozenset({ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
                            ClusterLens.FAILURE_SYSTEMIC, ClusterLens.RELEVANCE_SYSTEMIC})
    if lens in high_bonus: return 10
    if lens in med_bonus:  return 5
    return 0
```

Смысл: кластер из "systemic_pattern" историй более ценен → он должен промотироваться быстрее.

---

## 9. Primary Lens: из какой линзы создаётся issue

Если активных линз несколько, orchestrator создаёт issue только по **одной** — `primary_lens`. Остальные линзы формируют дополнительный контекст, но не создают separate issues (для simple случая).

Выбор primary lens (`cluster_orchestrator.py:179`):

```python
primary = self.clustering_engine.resolved_primary_lens()
# resolved_primary_lens():
#   if self.primary_lens is not None → return self.primary_lens
#   else → return self.active_lenses[0]
```

Конфигурируется через `CLUSTER_PRIMARY_LENS` env var. По умолчанию — первый элемент `CLUSTER_ACTIVE_LENSES`.

---

## 10. Полный pipeline от story до issue

```
POST /intake/stories
        │
        ▼
  StoryRecord сохранён
  lifecycle_status = READY_FOR_PROFILE
        │
        ▼  (синхронно: process_story / или асинхронно: cron process_all_pending)
  get_signals_for_story(story, signal_source)
        │  → infer_signals_from_canonical(canonical_type, canonical_labels, geo)
        │  → {"civic_domain": "roads", "failure_pattern": "broken_infrastructure", ...}
        │
        ▼
  clustering_engine.memberships(all_ready_profiles)
        │  → {story_id: {lens: cluster_id, ...}, ...}
        │
        ▼
  Выбор primary_lens cluster_id для trigger story
        │
        ▼
  readiness_score_for_cluster(lens, members, mode=ISSUE_READY)
        │  → score = base + lens_bonus + mode_bonus
        │
        ▼  (если score >= CLUSTER_READINESS_THRESHOLD)
  issue_create_service.create_issue(IssueCreateCommand)
        │  → DOGEIssue создан в doge_issues
        │
        ▼
  story.lifecycle_status → CLUSTERED
  cluster_memberships сохранены
```

---

## 11. Два поколения линз: legacy и civic

Система содержит два поколения линз. Оба набора зарегистрированы в коде; **целевым является civic**.

### Legacy (keyword-based) — устаревший

```python
LEGACY_LENSES = (
    ClusterLens.TOPIC_MICRO,          # topic: infrastructure / public_service
    ClusterLens.NEED_LOCAL,           # need: restore_access / resolve_issue
    ClusterLens.FAILURE_SYSTEMIC,     # system_failure: service_disruption / quality_gap
    ClusterLens.FAILURE_MICRO,        # system_failure: micro
    ClusterLens.REPEATABILITY_LOCAL,  # repeatability: recurrent / single_or_unknown
    ClusterLens.RELEVANCE_SYSTEMIC,   # relevance: "high" для всех → ВЫРОЖДЕННАЯ
)
```

Почему legacy не подходит для публичной ноды:
- `TOPIC` имеет только 2 значения (infrastructure/public_service) → слабая разделительная сила
- `DESIRED_STATE = "stable_public_service"` для всех → все stories в одном кластере → информация не несётся
- `RELEVANCE = "high"` для всех → аналогично вырожденная линза
- keyword-matching работает только с английским текстом; эстонские и русские жалобы получают дефолтные значения

### Civic (canonical, GPT-driven) — целевой

```python
# src/core/cluster/types.py:17-22
CIVIC_DOMAIN_MICRO          = "civic_domain_micro"          # 12 значений
FAILURE_PATTERN_MICRO       = "failure_pattern_micro"       # 9 значений
CIVIC_WEIGHT_SYSTEMIC       = "civic_weight_systemic"       # приоритизация
DESIRED_OUTCOME_LOCAL       = "desired_outcome_local"       # бизнес-аудитория
AFFECTED_GROUP_LOCAL        = "affected_group_local"        # демографика
GEOGRAPHIC_DISTRICT_MICRO   = "geographic_district_micro"   # район города
```

Преимущества civic:
- 12 значений `civic_domain` вместо 2 → чёткая тематическая разбивка
- Все оси вариативны → реальная разделяющая сила
- Языко-нейтральны: GPT нормализует ET/RU/EN → одинаковые canonical_labels → одинаковые сигналы

---

## 12. Статус реализации (аудит 2026-05-07)

Актуальная таблица: что сейчас в коде (`src/core/config/schema.py`) и что является целевым по civic lens model:

| Параметр | Сейчас в коде / schema.py | Целевое (civic lenses.md) | Статус |
|---------|--------------------------|---------------------------|--------|
| `CLUSTER_ACTIVE_LENSES` default | `topic_micro,need_local,failure_systemic,failure_micro,repeatability_local` | `civic_domain_micro,failure_pattern_micro,civic_weight_systemic,geographic_district_micro` | ❌ нужно переключить |
| `CLUSTER_PRIMARY_LENS` default | `topic_micro` | `failure_pattern_micro` | ❌ нужно переключить |
| `CLUSTER_ID_ALGORITHM` default | `sha256` | `sha256` | ✅ |
| `CLUSTER_MIN_SIZE` default | `8` | `5` | ❌ нужно изменить |
| `CLUSTER_READINESS_THRESHOLD` default | `60` | `60` | ✅ |
| Supabase bootstrap: `story_signals` | создаётся в `000_full_init.sql:105` | нужна таблица | ✅ |
| Supabase bootstrap: `cluster_memberships` | создаётся в `000_full_init.sql:114` | нужна таблица | ✅ |
| Все 6 civic ClusterLens enum values | реализованы в `types.py:17-22` | реализованы | ✅ |
| `infer_signals_from_canonical` | реализована в `enrichment.py:47-88` | реализована | ✅ |
| Vocabulary frozensets для 6 dimensions | реализованы в `vocabulary.py` | реализованы | ✅ |

**Вывод:** бизнес-логика и персистентный слой полностью реализованы. Оставшийся gap — только config defaults в `schema.py` и значения в `.env`.

---

## 13. Civic Lens Layer: полная продуктовая модель

### 13.1 Принцип публичной ноды

Публичная DOGEstonia-нода кластеризует **только по гражданским линзам** — тем, которые отражают гражданскую реальность, а не внутренние задачи клиента.

Клиентские линзы (`department_responsible`, `budget_category`, `procurement_priority`) могут существовать в частной инсталляции поверх civic слоя, но **не входят в public civic layer**.

### 13.2 Три аудитории, один массив данных

Одна и та же коллекция stories отвечает на вопросы трёх разных аудиторий — в зависимости от того, через какую линзу смотреть:

| Аудитория | Вопрос | Линза | Пример ответа |
|-----------|--------|-------|---------------|
| **Житель** | Я не один? Сколько людей с той же проблемой? | `civic_domain_micro` | "14 жалоб на roads" |
| **Государство** | Что именно и где нужно починить? | `failure_pattern_micro` + `geographic_district_micro` | "9 случаев broken_infrastructure в Lasnamäe" |
| **Бизнес / НКО** | Где незакрытый спрос на улучшение? | `desired_outcome_local` | "8 историй с desired_outcome = digital_fix" |

### 13.3 Lens Registry

Машиночитаемое описание каждой civic линзы (реализовать в `vocabulary.py`):

| Линза | Dimension | Scope | Audience | Вопрос линзы |
|-------|-----------|-------|----------|--------------|
| `civic_domain_micro` | `civic_domain` | micro | citizen | What is this complaint about? |
| `failure_pattern_micro` | `failure_pattern` | micro | city_government | How exactly is the system failing? |
| `civic_weight_systemic` | `civic_weight` | systemic | public_governance | Is this isolated or a broader civic signal? |
| `geographic_district_micro` | `geographic_district` | micro | citizen_and_city | Where is this problem happening? |
| `desired_outcome_local` | `desired_outcome` | local | citizen_business_ngo | What improvement do people want? |
| `affected_group_local` | `affected_group` | local | equity_and_service_design | Who is affected by this problem? |

`public_meaning` каждой линзы — человекочитаемое описание кластера для SPA и API-потребителей. Пример:
- `civic_domain_micro` → "Groups stories by civic topic, such as roads, transport, housing, or safety."
- `failure_pattern_micro` → "Groups stories by the type of failure: delay, broken infrastructure, unclear rules, service unavailable."

### 13.4 Primary lens: failure_pattern_micro

`CLUSTER_PRIMARY_LENS=failure_pattern_micro` — **не** `civic_domain_micro`.

Обоснование:
- `civic_domain_micro = "roads"` — это категория, широкая и неactionable
- `failure_pattern_micro = "broken_infrastructure"` — это конкретный тип сбоя, напрямую описывающий что нужно сделать

Issue, созданный по `failure_pattern_micro`, содержательно отвечает на вопрос "что чинить". Issue по `civic_domain_micro` отвечает только на "в какой сфере".

### 13.5 Config defaults для публичной ноды

Рекомендуемые значения env vars:

```bash
# MVP с районностью — рекомендуемый старт
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,geographic_district_micro
CLUSTER_PRIMARY_LENS=failure_pattern_micro
CLUSTER_ID_ALGORITHM=sha256
CLUSTER_MIN_SIZE=5
CLUSTER_READINESS_THRESHOLD=60

# Полный публичный слой — после стабилизации MVP
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,geographic_district_micro,desired_outcome_local,affected_group_local
```

### 13.6 Как выглядит civic кластеризация: функциональные примеры

#### Пример А: одна жалоба → три кластера

Поступает story: "Яма на Нарвском шоссе третий год не чинят, соседи тоже жалуются."

GPT присваивает canonical_labels: `["roads", "broken_infrastructure", "not_only_me"]`, geo: `"lasnamäe"`.

`infer_signals_from_canonical` превращает это в сигналы:
```python
{
    "civic_domain":        "roads",
    "failure_pattern":     "broken_infrastructure",
    "civic_weight":        "not_only_me",
    "geographic_district": "lasnamäe",
    "desired_outcome":     "unknown",   # в labels нет desired_outcome token
    "affected_group":      "unknown",   # в labels нет affected_group token
}
```

При активных 4 MVP-линзах эта story участвует в трёх кластерах одновременно:

```
civic_domain_micro:civic_domain:roads:micro
    → cluster:civic_domain_micro:0473821956

failure_pattern_micro:failure_pattern:broken_infrastructure:micro
    → cluster:failure_pattern_micro:1827364501

civic_weight_systemic:civic_weight:not_only_me:systemic   # not_only_me < systemic_pattern
    → (не проходит threshold, civic_weight_systemic ждёт systemic_pattern)

geographic_district_micro:geographic_district:lasnamäe:micro
    → cluster:geographic_district_micro:3847201956
```

---

#### Пример Б: та же проблема на эстонском и русском → один кластер

Story 1: "Tänav on katki, naabrid kurdavad ka." (эстонский)
Story 2: "Яма на дороге, соседи тоже жалуются." (русский)

GPT обе нормализует в одинаковые labels: `["roads", "broken_infrastructure", "not_only_me"]`.

→ Обе получают **идентичный** вектор сигналов.  
→ Обе попадают в **один и тот же** `cluster:failure_pattern_micro:1827364501`.

Языковая нейтральность обеспечивается GPT-слоем, а не кодом gateway.

---

#### Пример В: readiness gate — когда кластер становится issue

При `CLUSTER_READINESS_THRESHOLD=60` и `CLUSTER_MIN_SIZE=5`:

| Stories в кластере | base score | +civic_weight_systemic | +ISSUE_READY | Итого | Gate |
|-------------------|------------|----------------------|-------------|-------|------|
| 1 | 35 | 0 | +10 | 45 | ❌ ждём |
| 2 | 50 | 0 | +10 | 60 | ✅ issue создаётся |
| 2 (systemic) | 50 | +10 | +10 | 70 | ✅ issue создаётся |
| 1 (systemic) | 35 | +10 | +10 | 55 | ❌ ждём |

Кластер из 2 историй с `civic_weight=systemic_pattern` (score=70) создаст issue быстрее, чем кластер из 2 обычных (score=60). Смысл: системные сигналы приоритизируются.

---

#### Пример Г: N:M — одна story в нескольких issues

Одна жалоба "Яма в Ласнамяэ" попадает в:
- issue `failure_pattern_micro:broken_infrastructure` вместе с 5 другими жалобами на broken_infrastructure
- issue `geographic_district_micro:lasnamäe` вместе с 8 жалобами из Ласнамяэ на разные темы

Это **правильное поведение**: один и тот же факт может быть частью разных проблемных нарративов одновременно. Жалоба не "принадлежит" одному issue — она вносит вклад во все релевантные.

---

#### Пример Д: desired_outcome_local — линза для бизнеса и НКО

8 историй из Центрального района с `desired_outcome = "digital_fix"`:
```
cluster:desired_outcome_local:7293847102
```

Что это означает для НКО цифровой доступности: 8 человек просят что-то оцифровать. Это спрос, не жалоба — и он видим только через `desired_outcome_local` линзу, которую `civic_domain_micro` или `failure_pattern_micro` не показывают.

---

#### Пример Е: affected_group_local — линза для equity analysis

Три жалобы с `affected_group = "elderly_context"` накапливаются:
```
cluster:affected_group_local:5102938475
```

При достижении порога создаётся issue, который говорит: "существует паттерн проблем, специфически затрагивающих пожилых людей". Видно только через `affected_group_local` — не через тематическую или географическую линзу.

---

## 14. Как читать req25 и req26

После этого документа:

- **req25** (`25-clustering-engine-target-state-spec.md`) — технические инварианты и спецификация: SHA-256 детерминизм, idempotency, формула readiness, схема таблиц, orchestrator sequence. Это "как должна работать машинерия".

- **req26** (`26-clustering-signal-axes-from-gpt-taxonomy.md`) — семантическая модель: почему именно эти 6 осей, полные словари значений, бизнес-смысл для трёх аудиторий, примеры cluster-card. Это "что означает каждый кластер для людей".

---

## 14. Файлы кодовой базы

| Файл | Роль |
|------|------|
| `src/core/cluster/engine.py` | `ClusteringEngine`, `stable_cluster_id`, `readiness_score_for_cluster`, `memberships` |
| `src/core/cluster/types.py` | `ClusterLens` enum, `Cluster`, `ClusterView`, `ClusterMember`, `ClusteringMode` |
| `src/core/cluster/vocabulary.py` | frozenset словари: `CIVIC_DOMAIN_VOCABULARY`, `FAILURE_PATTERN_VOCABULARY`, `CIVIC_SIGNAL_PRIORITY`, etc. |
| `src/core/profile/enrichment.py` | `infer_signals_from_canonical`, `infer_signals_from_narrative`, `get_signals_for_story` |
| `src/core/domain/contracts.py` | `SignalDimension` enum, `StoryRecord`, `StoryLifecycleStatus` |
| `src/core/application/cluster_orchestrator.py` | `StoryClusterOrchestrator.process_story`, `process_all_pending` |
| `src/core/config/schema.py` | env vars: `CLUSTER_ACTIVE_LENSES`, `CLUSTER_ID_ALGORITHM`, `CLUSTER_MIN_SIZE`, etc. |
