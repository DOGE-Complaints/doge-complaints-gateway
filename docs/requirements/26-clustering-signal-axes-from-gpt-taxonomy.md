# 26. Оси кластеризации: GPT таксономия → смысловые сигналы для публичного узла

## 1. Назначение и контекст

Документ проектирует **смысловую модель кластеризации** для публичного узла `doge-complaints-gateway`, где кластеры видят три аудитории — жители города, государственный сектор, бизнес.

Основан на:
- полной таксономии GPT: `GPT UI/docs/requirements/REQ-20-label-taxonomy-and-extraction-axes.md` и `GPT UI/instructions/story-label-taxonomy.md`;
- технической спецификации: `25-clustering-engine-target-state-spec.md`;
- текущей реализации: `docs/analysis/clustering-audit-story-to-issue.md`.

**Сопоставление текущего и целевого:**

| Аспект | Текущее (as-is) | Целевое (this doc) |
|--------|-----------------|-------------------|
| Источник сигналов | keyword-matching на `narrative_original_text` | vocabulary-lookup на `canonical_labels[]` (GPT) |
| Оси сигналов | 2 вырожденных из 6 (DESIRED_STATE, RELEVANCE — константы) | 6 информативных осей, все вариативны |
| Разрешение по topic | 2 значения (infrastructure / public_service) | 12 значений (transport, roads, waste, ...) |
| Языковая нейтральность | нарушена (ET/RU истории → дефолт) | соблюдена через canonical GPT labels |
| Географическая кластеризация | нет | geographic_district как отдельная линза |
| Смысл для жителей | нет прямого | `civic_domain` × `failure_pattern` × `geographic_district` |

---

## 2. Три аудитории: модель чтения кластеров

### 2.1 Принцип проектирования

**Кластер имеет смысл только тогда, когда он отвечает на вопрос "что надо сделать?"**

Три аудитории задают разные вопросы одному кластеру:

| Аудитория | Вопрос к кластеру | Ожидаемый ответ |
|-----------|-------------------|-----------------|
| **Житель** | Я не один? Это известная проблема? | "14 жителей Ласнамяэ сообщают о том же" |
| **Государство** | Что приоритизировать, в каком районе, какой отдел? | "Системная проблема с дорогами в Ласнамяэ — нужен ремонт" |
| **Бизнес / НКО** | Где незакрытая потребность? | "8 историй с desired_outcome=digital_fix — возможность для сервиса" |

### 2.2 Ни одна ось не должна быть "служебной" — каждая читается человеком

Провальный паттерн текущей реализации: `DESIRED_STATE = "stable_public_service"` для всех историй. Эта ось не несёт информации — она не читается ни одной аудиторией.

**Правило:** ось включается в дефолтный набор, только если её значение меняется от истории к истории И это изменение значимо хотя бы для одной аудитории.

### 2.3 Cluster = читаемая карточка, а не технический ID

Целевой human-readable формат кластерной карточки для публичного отображения:

```
[civic_domain] × [failure_pattern] в [geographic_district]
N историй · [civic_weight]

Пример:
"roads × broken_infrastructure в Lasnamäe
14 историй · systemic_pattern"

Смысл для жителя:  "В Ласнамяэ 14 людей жалуются на разрушенное дорожное покрытие"
Смысл для города:  "Системная проблема дорожной инфраструктуры — приоритет для ремонтного плана"
Смысл для бизнеса: "Потребность в дорожном обслуживании в Ласнамяэ"
```

---

## 3. Бизнес-анализ: принципы выбора осей

### 3.1 Ось должна разделять истории, а не объединять всё в один кластер

| Ось | Разделительная сила | Вывод |
|-----|---------------------|-------|
| `RELEVANCE = "high"` для всех | ≈ 0, все в одном кластере | Удалить из дефолтного набора |
| `DESIRED_STATE = "stable_public_service"` | ≈ 0 | Удалить до появления вариативности |
| `civic_domain` (12 значений) | высокая | Добавить |
| `failure_pattern` (9 значений) | высокая | Добавить |
| `civic_weight` (5 уровней) | средняя — важна для приоритизации | Добавить |

### 3.2 Ось должна быть actionable — порождать конкретное действие

| Ось | Действие, которое порождает кластер |
|-----|-------------------------------------|
| `civic_domain = roads` | Маршрутизация в дорожный департамент |
| `failure_pattern = broken_infrastructure` | Включить в план технического обслуживания |
| `civic_weight = systemic_pattern` | Высокий приоритет, требует системного решения |
| `desired_outcome = digital_fix` | Кандидат для IT-команды портала |
| `geographic_district = Lasnamäe` | Территориальная привязка для местного самоуправления |

### 3.3 Дефолтный набор = пересечение максимальной actionability и доступных данных

Критерий включения в `CLUSTER_ACTIVE_LENSES` по умолчанию:
1. Ось варьируется для типичных историй жителей Таллинна
2. Кластеры по этой оси читаются хотя бы одной из трёх аудиторий
3. Значения оси извлекаются из уже доступных данных (`canonical_labels[]`, `canonical_type`, `geo`)

---

## 4. Сопоставление: GPT taxonomy axes → Signal Dimensions

### 4.1 Полная карта маппинга

| GPT Axis (REQ-20) | GPT disposition | Signal Dimension (новое) | Использование в кластеризации |
|-------------------|-----------------|--------------------------|-------------------------------|
| `topic_domain` | canonical | `civic_domain` | Первичная ось — что это за проблема |
| `failure_mode` | canonical | `failure_pattern` | Как именно ломается |
| `civic_signal` | canonical | `civic_weight` | Насколько системно / приоритетно |
| `desired_outcome` | metadata_only* | `desired_outcome` | Что хотят жители (бизнес-линза) |
| `affected_scope` | metadata_only* | `affected_group` | Кого касается |
| `location_context` | metadata_only* | — | Заменяется `geographic_district` из `StoryGeoSnapshot` |
| `issue_archetype_support` | metadata_only | — | Не используется в кластеризации |
| `deep_need` | metadata_only | — | Метаданные, не кластерная ось на текущем этапе |
| `risk_privacy_safety` | internal only | — | Никогда не в кластерной оси |
| `confidence_state` | internal only | — | Никогда не в кластерной оси |

\*`desired_outcome` и `affected_scope` — metadata-only в GPT taxonomy по умолчанию. Их включение в кластерные оси допустимо, если они присутствуют в `canonical_labels[]` с disposition `canonical`. Когда отсутствуют — `"unknown"`.

### 4.2 canonical_type → дополнительный signal

| GPT `canonical_type` | Производный сигнал для кластеризации |
|---------------------|-------------------------------------|
| `complaint` | `issue_archetype = complaint` (для будущей priority-линзы) |
| `observation` | `issue_archetype = observation` |
| `absurdity` | `issue_archetype = absurdity` → может усилить `civic_weight` |
| `system_bug` | `issue_archetype = system_bug` → `failure_pattern = bureaucratic_loop` как fallback |

На текущем этапе `canonical_type` используется для формирования `SpaIssueType` (doc 23), не как отдельная кластерная ось.

---

## 5. Новые Signal Dimensions: полные словари

### 5.1 `civic_domain` — тематическая область

Заменяет текущий `TOPIC` (infrastructure / public_service).

Источник: первый `canonical_label` из `CIVIC_DOMAIN_VOCABULARY`.

| Значение | Смысл | Пример истории |
|----------|-------|----------------|
| `transport` | Общественный транспорт, маршруты, остановки | "Автобус 18 отменили" |
| `roads` | Дороги, перекрёстки, трафик | "Ямы на Нарвском шоссе" |
| `parking` | Парковка, правила, доступность | "Негде парковаться у поликлиники" |
| `public_space` | Улицы, парки, площади, дворы | "Разрушена детская площадка" |
| `waste` | Вывоз мусора, урны, переполненные баки | "Мусор не вывозят третью неделю" |
| `environment` | Шум, воздух, зелень, вода | "Строительный шум до 22:00" |
| `housing` | Жилые дома, дворы, ЖКУ | "Протекает крыша в Ласнамяэ" |
| `education` | Школы, детские сады | "Очередь в детский сад 3 года" |
| `healthcare` | Доступность медицины | "Запись к врачу — 2 месяца ожидания" |
| `digital_service` | Порталы, формы, онлайн-сервисы | "Портал eesti.ee не принимает документы" |
| `safety` | Публичная безопасность (без PII) | "Тёмная дорожка — опасно вечером" |
| `accessibility` | Физические и цифровые барьеры | "Нет пандуса на автобусной остановке" |
| `unknown` | Fallback при отсутствии labels | — |

### 5.2 `failure_pattern` — тип сбоя

Заменяет текущий `SYSTEM_FAILURE` (service_disruption / quality_gap).

Источник: первый `canonical_label` из `FAILURE_PATTERN_VOCABULARY`.

| Значение | Смысл | Пример |
|----------|-------|--------|
| `broken_infrastructure` | Физическая инфраструктура повреждена / отсутствует | "Яма посреди дороги" |
| `maintenance_gap` | Обслуживание не проводится / опаздывает | "Газон не стригут 2 месяца" |
| `access_blocked` | Доступ закрыт — место, сервис, маршрут | "Перекрыт проход через двор" |
| `unsafe_condition` | Условия создают практический риск | "Наледь на ступеньках" |
| `service_unavailable` | Ожидаемый сервис недоступен или регулярно отказывает | "Банкомат не работает 2 недели" |
| `delay` | Ожидание, медленный ответ, пропущенные сроки | "Ответ на обращение — 3 месяца" |
| `information_gap` | Правила / статус / ответственность непонятны | "Непонятно, кто отвечает за этот тротуар" |
| `bureaucratic_loop` | Гражданин ходит по кругу | "Отправляют из ведомства в ведомство" |
| `unclear_rules` | Правила противоречивы / трудно понять | "Инструкция на портале устарела" |
| `unknown` | Fallback | — |

### 5.3 `civic_weight` — вес гражданского сигнала

Заменяет текущие `REPEATABILITY` и `RELEVANCE` (оба деградированы).

Источник: наивысший по приоритету `civic_signal_label` из `canonical_labels[]`.

| Приоритет | Значение | Смысл | Сигнал для государства |
|-----------|----------|-------|----------------------|
| 1 (высший) | `systemic_pattern` | Отражает системный сбой, не единичный случай | Требует системного решения |
| 2 | `public_cost` | Создаёт издержки за пределами отдельного эпизода | Высокий приоритет по экономике |
| 3 | `not_only_me` | Житель указывает — проблема общая | Валидация кластерности |
| 4 | `recurring_issue` | Повторяется во времени | Нужен мониторинг, не разовый фикс |
| 5 | `equity_access` | Неравный доступ, дискриминационный барьер | Социальная приоритизация |
| 6 | `trust_in_services` | Потеря доверия к работе публичных сервисов | Сигнал для PR / коммуникационной политики |
| 7 | `city_for_people` | Желаемое состояние — более человечный город | Стратегический ориентир |
| 8 (дефолт) | `isolated` | Единичный случай, нет системного сигнала | Обычная обработка |

**Алгоритм:** перебрать `CIVIC_SIGNAL_PRIORITY` по порядку; вернуть первый, присутствующий в `canonical_labels[]`.

### 5.4 `desired_outcome` — желаемый результат

Новая ось, источник — GPT `desired_outcome` labels в `canonical_labels[]`.

| Значение | Смысл | Кому читаемо |
|----------|-------|-------------|
| `better_maintenance` | Лучшее обслуживание / уход | Государство (план обслуживания) |
| `safer_space` | Более безопасное пространство | Государство (безопасность), жители |
| `faster_response` | Более быстрый ответ / реакция | Государство (SLA) |
| `accessible_service` | Физически или цифрово доступный сервис | Государство, бизнес (accessibility) |
| `digital_fix` | Исправление цифрового сервиса | Бизнес (IT), государство |
| `clear_rules` | Понятные правила и процессы | Государство (регуляция) |
| `transparent_process` | Прозрачный процесс принятия решений | Государство (коммуникация) |
| `human_contact` | Возможность поговорить с живым человеком | Государство (клиентский сервис) |
| `unknown` | Fallback | — |

### 5.5 `affected_group` — кого касается

Новая ось, источник — GPT `affected_scope` labels в `canonical_labels[]`.

| Значение | Смысл |
|----------|-------|
| `pedestrians` | Пешеходы |
| `elderly_context` | Пожилые жители |
| `children_context` | Дети, контекст с детьми |
| `parents` | Родители |
| `drivers` | Водители |
| `residents` | Жители района / дома |
| `visitors` | Туристы, гости города |
| `small_business` | Малый бизнес |
| `public_users` | Широкая публика |
| `general_public` | Дефолт при отсутствии конкретики |

### 5.6 `geographic_district` — административный район

Источник: `StoryGeoSnapshot.normalized_label` из `StoryRecord.geo`.

Эталонные значения для Таллинна:

| Значение (normalized_label) | Район |
|----------------------------|-------|
| `kesklinn` | Kesklinn (Центр) |
| `lasnamäe` | Lasnamäe |
| `mustamäe` | Mustamäe |
| `põhja-tallinn` | Põhja-Tallinn |
| `kristiine` | Kristiine |
| `haabersti` | Haabersti |
| `nõmme` | Nõmme |
| `pirita` | Pirita |
| `unknown` | Дефолт при отсутствии / неопределённом geo |

Линза `geographic_district` **зависит** от персистенции `StoryGeoSnapshot` (GAP-IMP-03). До её реализации — `"unknown"` для всех историй → линза вырожденная, не включать в default.

---

## 6. Label Vocabulary Registries (code-ready)

Верифицированы по `GPT UI/instructions/story-label-taxonomy.md` §4 (canonical allowed labels).

```python
# src/core/cluster/vocabulary.py

CIVIC_DOMAIN_VOCABULARY: frozenset[str] = frozenset({
    "transport",
    "roads",
    "parking",
    "public_space",
    "waste",
    "environment",
    "housing",
    "education",
    "healthcare",
    "digital_service",
    "safety",
    "accessibility",
})

FAILURE_PATTERN_VOCABULARY: frozenset[str] = frozenset({
    "delay",
    "access_blocked",
    "information_gap",
    "broken_infrastructure",
    "unsafe_condition",
    "bureaucratic_loop",
    "unclear_rules",
    "service_unavailable",
    "maintenance_gap",
})

CIVIC_SIGNAL_VOCABULARY: frozenset[str] = frozenset({
    "recurring_issue",
    "systemic_pattern",
    "public_cost",
    "not_only_me",
    "equity_access",
    "trust_in_services",
    "city_for_people",
})

CIVIC_SIGNAL_PRIORITY: tuple[str, ...] = (
    "systemic_pattern",
    "public_cost",
    "not_only_me",
    "recurring_issue",
    "equity_access",
    "trust_in_services",
    "city_for_people",
)

DESIRED_OUTCOME_VOCABULARY: frozenset[str] = frozenset({
    "clear_rules",
    "faster_response",
    "safer_space",
    "better_maintenance",
    "accessible_service",
    "transparent_process",
    "human_contact",
    "digital_fix",
})

AFFECTED_SCOPE_VOCABULARY: frozenset[str] = frozenset({
    "pedestrians",
    "parents",
    "children_context",
    "elderly_context",
    "drivers",
    "residents",
    "visitors",
    "small_business",
    "public_users",
})
```

---

## 7. Алгоритм извлечения сигналов из canonical labels

```python
# src/core/profile/enrichment.py — целевая реализация

from core.cluster.vocabulary import (
    CIVIC_DOMAIN_VOCABULARY,
    FAILURE_PATTERN_VOCABULARY,
    CIVIC_SIGNAL_PRIORITY,
    DESIRED_OUTCOME_VOCABULARY,
    AFFECTED_SCOPE_VOCABULARY,
)
from core.domain import SignalDimension


def infer_signals_from_canonical(
    canonical_type: str | None,
    canonical_labels: tuple[str, ...],
    geo_normalized_label: str | None = None,
) -> dict[str, str]:
    """Extract cluster signals from GPT canonical fields.

    Language-agnostic: canonical_labels are normalized by GPT regardless of narrative language.
    Precondition: canonical_labels contains keys from story-label-taxonomy.md §4 only.
    """
    labels = set(canonical_labels)

    civic_domain = next(
        (label for label in canonical_labels if label in CIVIC_DOMAIN_VOCABULARY),
        "unknown",
    )
    failure_pattern = next(
        (label for label in canonical_labels if label in FAILURE_PATTERN_VOCABULARY),
        "unknown",
    )
    civic_weight = next(
        (label for label in CIVIC_SIGNAL_PRIORITY if label in labels),
        "isolated",
    )
    desired_outcome = next(
        (label for label in canonical_labels if label in DESIRED_OUTCOME_VOCABULARY),
        "unknown",
    )
    affected_group = next(
        (label for label in canonical_labels if label in AFFECTED_SCOPE_VOCABULARY),
        "general_public",
    )
    geographic_district = geo_normalized_label.strip().lower() if geo_normalized_label else "unknown"

    return {
        SignalDimension.CIVIC_DOMAIN.value: civic_domain,
        SignalDimension.FAILURE_PATTERN.value: failure_pattern,
        SignalDimension.CIVIC_WEIGHT.value: civic_weight,
        SignalDimension.DESIRED_OUTCOME.value: desired_outcome,
        SignalDimension.AFFECTED_GROUP.value: affected_group,
        SignalDimension.GEOGRAPHIC_DISTRICT.value: geographic_district,
    }
```

**Требование к `CLUSTER_SIGNAL_SOURCE=canonical`:** `canonical_labels` не пустой. Если пустой → fallback на keyword-matching (legacy) или `"unknown"`.

**Требование к порядку canonical_labels:** порядок имеет значение для первого совпадения. GPT должен ставить наиболее конфидентные labels первыми (disposition `canonical` > остальные). Если это не гарантировано API — сортировать по приоритетной vocabulary таблице.

---

## 8. Новые ClusterLens под новые Signal Dimensions

| Новый Lens enum value | Signal Dimension | Scope suffix | readiness_bonus | Назначение |
|-----------------------|-----------------|--------------|-----------------|-----------|
| `civic_domain_micro` | `civic_domain` | `micro` | 0 | Что за проблема (дороги, мусор, транспорт...) |
| `failure_pattern_micro` | `failure_pattern` | `micro` | 0 | Как ломается (разрушено, нет обслуживания, петля) |
| `civic_weight_systemic` | `civic_weight` | `systemic` | **+10** | Системность / приоритет для государства |
| `desired_outcome_local` | `desired_outcome` | `local` | 0 | Что хотят (для бизнес-аудитории) |
| `affected_group_local` | `affected_group` | `local` | 0 | Кого касается |
| `geographic_district_micro` | `geographic_district` | `micro` | **+5** | Район города |

### 8.1 Дефолтный набор для публичного узла

```
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic
CLUSTER_PRIMARY_LENS=civic_domain_micro
```

**Обоснование дефолтного набора:**

1. `civic_domain_micro` — первичная для людей. Ответ на "о чём?" — 12 значений, высокая разделительная сила, читаема всеми тремя аудиториями, не требует доп. данных.

2. `failure_pattern_micro` — первичная для государства. Ответ на "как ломается?" — 9 значений, actionable для технических департаментов.

3. `civic_weight_systemic` — приоритизирующая. Ответ на "насколько важно?" — отделяет системные паттерны от единичных жалоб, критична для Government/Business аудиторий.

**Не включены в дефолт (почему):**
- `desired_outcome_local` — подключить когда `desired_outcome` регулярно присутствует в canonical_labels (требует аналитики по реальным данным)
- `affected_group_local` — подключить когда GPT стабильно извлекает affected_scope с disposition canonical
- `geographic_district_micro` — подключить после GAP-IMP-03 (geo persistence)

### 8.2 readiness_bonus для новых линз

| Линза | bonus | Обоснование |
|-------|-------|-------------|
| `civic_weight_systemic` | +10 | Кластер по `systemic_pattern` / `public_cost` — наиболее зрелый для issue-formation |
| `geographic_district_micro` | +5 | Гео-привязка повышает actionability кластера |

---

## 9. Как кластеры читаются тремя аудиториями: примеры

### 9.1 Пример кластера

Условие: 7 историй с `canonical_labels = ["roads", "broken_infrastructure", "systemic_pattern"]` из Lasnamäe.

**Кластер по `civic_domain_micro`:**
```
cluster_id:  cluster:civic_domain_micro:0473821956
lens:        civic_domain_micro
dimension:   CIVIC_DOMAIN = "roads"
members:     7 stories
readiness:   base=min(100,20+7*15)=100, civic_weight bonus нет → 100
```

**Кластер по `failure_pattern_micro`:**
```
cluster_id:  cluster:failure_pattern_micro:1827364501
lens:        failure_pattern_micro
dimension:   FAILURE_PATTERN = "broken_infrastructure"
members:     7 stories (те же, плюс возможно другие с тем же failure)
```

**Кластер по `civic_weight_systemic`:**
```
cluster_id:  cluster:civic_weight_systemic:0912847365
lens:        civic_weight_systemic
dimension:   CIVIC_WEIGHT = "systemic_pattern"
members:     все истории с civic_weight="systemic_pattern" (не только roads)
readiness:   base + 10 bonus
```

### 9.2 Одна история — три разные cluster_id

Story "Ямы на Narva mnt, 3 года не ремонтируют, соседи тоже жалуются":
- `civic_domain_micro` → `cluster:civic_domain_micro:0473821956` ("roads")
- `failure_pattern_micro` → `cluster:failure_pattern_micro:1827364501` ("broken_infrastructure")
- `civic_weight_systemic` → `cluster:civic_weight_systemic:0912847365` ("systemic_pattern")

Это корректное N:M поведение (doc 23 D-10): одна история участвует в трёх issues по трём линзам.

### 9.3 Читаемость по аудиториям

**Для жителя Ласнамяэ:**
> "Cluster: roads в Lasnamäe — 7 историй о проблемах с дорогами"
→ "Я не один, это общая проблема"

**Для муниципального чиновника:**
> "roads × broken_infrastructure × systemic_pattern — 7 историй, readiness=100"
→ "Это должно войти в план дорожного ремонта Ласнамяэ на следующий квартал"

**Для бизнеса (дорожный сервис / мобильность):**
> "broken_infrastructure на roads × desired_outcome=better_maintenance — 7 историй"
→ "Здесь есть спрос на дорожное обслуживание"

---

## 10. Обновлённый реестр SignalDimension

Расширить `src/core/domain/contracts.py`:

```python
class SignalDimension(StrEnum):
    # Новые (заменяют/расширяют legacy)
    CIVIC_DOMAIN         = "civic_domain"           # replaces TOPIC
    FAILURE_PATTERN      = "failure_pattern"        # replaces SYSTEM_FAILURE
    CIVIC_WEIGHT         = "civic_weight"           # replaces REPEATABILITY + RELEVANCE
    DESIRED_OUTCOME      = "desired_outcome"        # new
    AFFECTED_GROUP       = "affected_group"         # new
    GEOGRAPHIC_DISTRICT  = "geographic_district"    # new

    # Legacy (сохраняются для обратной совместимости с existing data)
    TOPIC         = "topic"
    SYSTEM_FAILURE = "system_failure"
    NEED          = "need"
    DESIRED_STATE = "desired_state"
    REPEATABILITY = "repeatability"
    RELEVANCE     = "relevance"
```

Legacy dimensions остаются для existing data; новые — для `CLUSTER_SIGNAL_SOURCE=canonical`.

---

## 11. Обновлённый реестр ClusterLens

Расширить `src/core/cluster/types.py`:

```python
class ClusterLens(StrEnum):
    # Новые (semantic, GPT-driven)
    CIVIC_DOMAIN_MICRO         = "civic_domain_micro"
    FAILURE_PATTERN_MICRO      = "failure_pattern_micro"
    CIVIC_WEIGHT_SYSTEMIC      = "civic_weight_systemic"
    DESIRED_OUTCOME_LOCAL      = "desired_outcome_local"
    AFFECTED_GROUP_LOCAL       = "affected_group_local"
    GEOGRAPHIC_DISTRICT_MICRO  = "geographic_district_micro"

    # Legacy (keyword-based, backward-compat)
    TOPIC_MICRO          = "topic_micro"
    NEED_LOCAL           = "need_local"
    FAILURE_SYSTEMIC     = "failure_systemic"
    FAILURE_MICRO        = "failure_micro"
    REPEATABILITY_LOCAL  = "repeatability_local"
    RELEVANCE_SYSTEMIC   = "relevance_systemic"
```

`CLUSTER_ACTIVE_LENSES` validation обновить: принимать как legacy, так и новые enum values.

---

## 12. Конфигурация env vars для публичного узла

```dotenv
# .env (публичный узел, дефолтная смысловая кластеризация)
CLUSTER_SIGNAL_SOURCE=canonical
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic
CLUSTER_PRIMARY_LENS=civic_domain_micro
CLUSTER_MIN_SIZE=5
CLUSTER_READINESS_THRESHOLD=60
CLUSTER_ID_ALGORITHM=sha256
```

**Обоснование CLUSTER_MIN_SIZE=5 (вместо legacy 8):**
- При более широком наборе осей (12 значений civic_domain) кластеры более специфичны
- Специфичный кластер из 5 историй информативнее общего из 8
- Ниже порог → быстрее появляются первые issues при запуске → важно для bootstrap

**Обоснование CLUSTER_READINESS_THRESHOLD=60 (вместо 70):**
- `civic_weight_systemic` lens дает bonus +10 → кластер из 3 systemic stories = 65+10=75 > 60
- Позволяет системным кластерам промотироваться раньше, не ждать 5+ историй

---

## 13. Acceptance criteria

### AC-01 — Языковая нейтральность
- [ ] ET-нарратив "Tänav on katki" с `canonical_labels=["roads", "broken_infrastructure"]` попадает в тот же кластер `civic_domain_micro`, что и EN-нарратив "Road is broken" с теми же labels

### AC-02 — Гражданский вес
- [ ] Две истории с `civic_weight="systemic_pattern"` получают readiness_score ≥ 70 по линзе `civic_weight_systemic` (base=50 + bonus=10 = 60... нет, wait: base=min(100,20+2*15)=50, 50+10=60 < 70)
- [ ] **Откорректировать:** 3 истории с `systemic_pattern` → base=65+10=75 ≥ 60 → AC при CLUSTER_READINESS_THRESHOLD=60 ✓

### AC-03 — Разделительная сила
- [ ] "roads × broken_infrastructure" и "waste × maintenance_gap" НЕ попадают в один кластер по `civic_domain_micro`
- [ ] "roads × broken_infrastructure" и "roads × maintenance_gap" попадают в один кластер по `civic_domain_micro`, но в разные по `failure_pattern_micro`

### AC-04 — Human-readable cluster card
- [ ] Для кластера `civic_domain_micro:roads` narrative содержит слово "roads" или значение dimension
- [ ] Issue title для этого кластера не является `f"cluster:civic_domain_micro"` (raw technical string)

### AC-05 — desired_outcome читается бизнес-аудиторией
- [ ] Кластер `desired_outcome_local:digital_fix` собирает только истории с `canonical_labels ∋ "digital_fix"`
- [ ] При добавлении `desired_outcome_local` в `CLUSTER_ACTIVE_LENSES` — issue по этому линзу создаётся корректно

### AC-06 — Backward compatibility
- [ ] При `CLUSTER_SIGNAL_SOURCE=keyword` legacy keyword-matching всё ещё работает
- [ ] При `CLUSTER_ACTIVE_LENSES=topic_micro` (legacy) pipeline работает без ошибок

---

## 14. Open decisions

| ID | Суть | Зависимость |
|----|------|-------------|
| OD-01 | Нужно ли хранить ВСЕ matching labels или только первый при extracting civic_domain? Первый = более простая кластеризация; все = multi-membership по domain | Решение продукта |
| OD-02 | Включать ли `desired_outcome_local` и `affected_group_local` в дефолт при достаточном покрытии? Требует аналитики по первым N историям | После запуска с реальными данными |
| OD-03 | Нужен ли composite lens `domain_failure` = civic_domain × failure_pattern как единица кластеризации? Дало бы "roads × broken_infrastructure" как атомарный кластер | Сложнее реализация, но мощнее для государства |
| OD-04 | Как обрабатывать истории без canonical_labels (если GPT не заполнил)? fallback на keyword vs. `"unknown"` vs. reject story | Решение по умолчанию: `"unknown"` + fallback |
| OD-05 | geographic_district: использовать Tallinn-specific нормализацию или generic? | После GAP-IMP-03 |

---

## 15. Трассировка

| Зона | Документ / задача |
|------|------------------|
| Технические требования к кластеризации | `25-clustering-engine-target-state-spec.md` |
| GPT taxonomy source of truth | `GPT UI/docs/requirements/REQ-20-label-taxonomy-and-extraction-axes.md` |
| GPT label controlled vocabulary | `GPT UI/instructions/story-label-taxonomy.md` |
| canonical_labels в StoryRecord | `22-m2-demo-story-intake-interview-ssot-v1.md` |
| Продуктовая рамка кластеров | `07-dynamic-clusters-product-model.md` |
| Аудит текущей реализации | `docs/analysis/clustering-audit-story-to-issue.md` |
| Реализация новых vocabulary + enrichment | `TASK-CLUSTER-TAXONOMY-SIGNALS-01` |
| Новые ClusterLens enum values | `TASK-CLUSTER-LENS-SEMANTIC-01` |
| Geographic district lens | `TASK-CLUSTER-GEO-DISTRICT-01` (зависит от GAP-IMP-03) |

---

## 16. Gap Analysis: текущее состояние vs. спецификация (аудит 2026-05-05)

Аудит проведён по фактическому коду. Статусы — **факты из кода**, не предположения.

### 16.1 Статус реализации

| Требование (раздел) | Статус | Файл / строка |
|--------------------|--------|---------------|
| `vocabulary.py` с frozenset registries (6) | ✅ | `src/core/cluster/vocabulary.py` — все 5 словарей присутствуют |
| 6 новых `SignalDimension` значений (10) | ✅ | `src/core/domain/contracts.py` |
| 6 новых `ClusterLens` значений (11) | ✅ | `src/core/cluster/types.py` |
| `infer_signals_from_canonical()` через vocabulary (7) | ✅ | `src/core/cluster/enrichment.py` |
| `civic_weight_systemic` бонус +10 (8.2) | ✅ | `src/core/cluster/engine.py:113` — `high_bonus` frozenset |
| **`CLUSTER_ACTIVE_LENSES` default = civic triple (12)** | ❌ | `src/core/config/schema.py` — дефолт legacy lenses (`topic_micro,...`) |
| **`CLUSTER_ID_ALGORITHM` default = `"sha256"` (12)** | ❌ | `src/core/config/schema.py` — дефолт `"legacy_hash"` |
| **`CLUSTER_MIN_SIZE` default = 5 (12)** | ❌ | `src/core/config/schema.py` — дефолт `8` |
| **`story_signals` в Supabase bootstrap** | ❌ | `supabase/bootstrap/000_full_init.sql` — отсутствует |
| **`cluster_memberships` в Supabase bootstrap** | ❌ | `supabase/bootstrap/000_full_init.sql` — отсутствует |

### 16.2 Незакрытые пункты → задачи

| GAP-ID | Проблема | Файл | Задача |
|--------|---------|------|--------|
| GAP-26-01 | `CLUSTER_ACTIVE_LENSES` default = legacy вместо `civic_domain_micro,failure_pattern_micro,civic_weight_systemic` | `src/core/config/schema.py` | `TASK-CLUSTER-CONFIG-DEFAULT-01` |
| GAP-26-02 | `CLUSTER_ID_ALGORITHM` default = `"legacy_hash"` вместо `"sha256"` | `src/core/config/schema.py` | `TASK-CLUSTER-CONFIG-DEFAULT-01` (совмещается) |
| GAP-26-03 | `CLUSTER_MIN_SIZE` default = 8 вместо 5 | `src/core/config/schema.py` | `TASK-CLUSTER-CONFIG-DEFAULT-01` (совмещается) |
| GAP-26-04 | `story_signals` отсутствует в Supabase bootstrap | `supabase/bootstrap/000_full_init.sql` | `TASK-CLUSTER-SUPABASE-SCHEMA-01` |
| GAP-26-05 | `cluster_memberships` отсутствует в Supabase bootstrap | `supabase/bootstrap/000_full_init.sql` | `TASK-CLUSTER-SUPABASE-SCHEMA-01` (совмещается) |

### 16.3 Рекомендуемый порядок закрытия

1. **GAP-26-01 + GAP-26-02 + GAP-26-03** — три строки в `schema.py`; один компактный PR; критично для правильного поведения публичного узла из коробки
2. **GAP-26-04 + GAP-26-05** — один SQL блок в bootstrap; нужен для Supabase fresh install и полноты схемы

**Важно:** GAP-26-01 (смена дефолтных линз) — breaking change для существующих dev/test сред с данными в legacy-кластерах. Рекомендуется выполнять при чистом перезапуске dev-среды или после миграции данных.
