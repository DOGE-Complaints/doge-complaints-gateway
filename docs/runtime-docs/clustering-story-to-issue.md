# Clustering: Story → Issue — Runtime Architecture

**Дата:** 2026-04-30  
**Методология:** analysis.mdc — только факты из кода, без предположений  
**Scope:** `doge-complaints-gateway` — cluster subsystem (wave 1, post 4 Supabase migrations)

---

## 1. Общая схема пайплайна

```
POST /stories/{id}/intake
        │
        ▼
StoryClusterOrchestrator.process_story(story_id)
        │
        ├─ guard: story.lifecycle_status == READY_FOR_PROFILE?
        │
        ▼
list_stories() → filter READY_FOR_PROFILE
        │
        ▼
infer_signals_from_narrative(text) × N stories
→ StoryProfileSignals(story_id, signals: dict[dimension → value])
        │
        ▼
ClusteringEngine.memberships(profiles)
→ {story_id → {lens_name → cluster_id}} для всех active_lenses
        │
        ▼
first_lens = active_lenses[0]              ← только первый линз!
cluster_id = memberships[story_id][first_lens]
member_story_ids = все истории в том же кластере по first_lens
        │
        ▼
IssueCreateService.create_issue(IssueCreateCommand(
    cluster_id=cluster_id,
    story_ids=member_story_ids,
    readiness_score=100,                   ← захардкожено!
    title=story.narrative_title_hint or f"cluster:{first_lens}",
))
        │
        ▼
→ issue_id | None
```

**Источники:**
- `src/core/application/cluster_orchestrator.py:18-70`
- `src/core/infrastructure/service_factory.py:71-118`

---

## 2. Сигнальные измерения (SignalDimension)

Каждый StoryProfileSignals содержит значения по 6 обязательным осям:

| Dimension | Смысл оси | Текущие значения |
|-----------|-----------|-----------------|
| `TOPIC` | Тематика жалобы | `infrastructure` / `public_service` |
| `SYSTEM_FAILURE` | Тип сбоя | `service_disruption` / `quality_gap` |
| `NEED` | Потребность гражданина | `restore_access` / `resolve_issue` |
| `DESIRED_STATE` | Желаемый результат | `stable_public_service` (всегда) |
| `REPEATABILITY` | Повторяемость проблемы | `recurrent` / `single_or_unknown` |
| `RELEVANCE` | Релевантность сигнала | `high` (всегда) |

**Источник:** `src/core/profile/schema.py` (REQUIRED_SIGNAL_DIMENSIONS)

---

## 3. Извлечение сигналов: `infer_signals_from_narrative()`

Единственный метод получения сигналов — keyword-matching по plain text нарратива:

```python
# src/core/profile/enrichment.py
def infer_signals_from_narrative(narrative: str) -> dict[str, str]:
    text = narrative.lower()

    # TOPIC: infrastructure если есть "road"/"water"/"bridge"/"infrastructure"
    TOPIC = "infrastructure" if any(k in text for k in ("road","water","bridge","infrastructure")) \
            else "public_service"

    # SYSTEM_FAILURE: service_disruption если "blocked"/"outage"/"leak"/"broken"
    SYSTEM_FAILURE = "service_disruption" if any(k in text for k in ("blocked","outage","leak","broken")) \
                     else "quality_gap"

    # NEED: restore_access если "blocked"
    NEED = "restore_access" if "blocked" in text else "resolve_issue"

    # DESIRED_STATE: всегда "stable_public_service" — нет вариации
    DESIRED_STATE = "stable_public_service"

    # REPEATABILITY: recurrent если "again"/"repeated"/"recurring"/"еще раз"
    REPEATABILITY = "recurrent" if any(k in text for k in ("again","repeated","recurring")) \
                    else "single_or_unknown"

    # RELEVANCE: всегда "high" — нет вариации
    RELEVANCE = "high"
```

**Критические ограничения:**
- Только английские ключевые слова — эстонские и русские нарративы дают TOPIC=`public_service`, SYSTEM_FAILURE=`quality_gap` по умолчанию
- `DESIRED_STATE` и `RELEVANCE` лишены вариативности — 2 из 6 измерений вырождены
- Бинарная классификация без градаций — нет вектора уверенности
- GPT canonical_type и canonical_labels (уже в StoryRecord) полностью игнорируются

---

## 4. Кластерные линзы (ClusterLens)

6 линз определяют, по какому сигнальному измерению объединяются истории:

| Lens | Измерение | Суффикс ключа | Бонус readiness |
|------|-----------|--------------|-----------------|
| `topic_micro` | TOPIC | `:micro` | — |
| `need_local` | NEED | `:local` | — |
| `failure_systemic` | SYSTEM_FAILURE | `:systemic` | **+5** |
| `failure_micro` | SYSTEM_FAILURE | `:micro` | — |
| `repeatability_local` | REPEATABILITY | `:local` | — |
| `relevance_systemic` | RELEVANCE | `:systemic` | **+5** |

**Формирование cluster_id:**
```python
# src/core/cluster/engine.py
key = f"{lens}:{dimension}:{value}:{suffix}"   # e.g. "topic_micro:TOPIC:infrastructure:micro"
cluster_id = f"cluster:{lens}:{abs(hash((lens.value, key))) % 1_000_000_000}"
```

ID детерминирован: одинаковое значение dimension для одного lens → один и тот же cluster_id.

**Источник:** `src/core/cluster/engine.py:lens_dimension(), cluster_key_for_lens(), stable_cluster_id()`

---

## 5. Оценка готовности кластера (readiness_score)

```python
# src/core/cluster/engine.py:readiness_score_for_cluster()
base = min(100, 20 + size * 15)       # size = количество историй в кластере
lens_bonus = 5 if lens in (FAILURE_SYSTEMIC, RELEVANCE_SYSTEMIC) else 0
mode_bonus = 10 if mode == ISSUE_READY else 0
score = base + lens_bonus + mode_bonus
```

Таблица base-score по размеру кластера:

| Stories | base | + FAILURE/RELEVANCE_SYSTEMIC | + ISSUE_READY mode |
|---------|------|-----------------------------|--------------------|
| 1 | 35 | 40 | 45 |
| 2 | 50 | 55 | 60 |
| 3 | 65 | 70 | 75 |
| 4 | 80 | 85 | 90 |
| 5 | 95 | 100 | 105→100 |
| 6+ | 100 | 100 | 100 |

**Важно:** `StoryClusterOrchestrator.process_story()` передаёт `readiness_score=100` захардкоженно (`cluster_orchestrator.py:66`). Реальный score кластера при issue creation не используется.

---

## 6. Ворота продвижения (PromotionGatePolicy)

```python
# src/core/promotion/gates.py
@dataclass(frozen=True)
class PromotionGatePolicy:
    min_readiness_score: int = 70    # default fallback
    min_stories: int = 2             # default fallback

# Реальные значения из AppConfig (service_factory.py:82-85):
PromotionGatePolicy(
    min_readiness_score=config.cluster_readiness_threshold,  # CLUSTER_READINESS_THRESHOLD
    min_stories=config.cluster_min_size,                     # CLUSTER_MIN_SIZE
)
```

Кандидат блокируется если:
1. `candidate.readiness_score < min_readiness_score` → `"readiness_below_threshold"`
2. `len(candidate.story_ids) < min_stories` → `"insufficient_story_evidence"`

**Но:** т.к. orchestrator передаёт `readiness_score=100` захардкоженно — gate по readiness всегда проходит. Gate по `min_stories` активен.

---

## 7. Текущая конфигурация (env vars)

| Переменная | Default | Тип | Проверка | Используется в runtime |
|------------|---------|-----|----------|----------------------|
| `CLUSTER_MIN_SIZE` | `8` | int >0 | да | `PromotionGatePolicy.min_stories` |
| `CLUSTER_READINESS_THRESHOLD` | `70` | int 1-100 | да | `PromotionGatePolicy.min_readiness_score` |
| `CLUSTER_ACTIVE_LENSES` | все 6 | comma-list | валидация enum | `ClusteringEngine.active_lenses` |
| `CLUSTER_GEO_FILTER` | `any` | str | нет | **хранится в AppConfig, в engine НЕ передаётся** |
| `CLUSTER_TIE_BREAKER` | `lexical` | str | нет | **хранится в AppConfig, не используется** |
| `CLUSTER_TYPE_RESOLUTION` | `canonical_priority` | str | нет | **хранится в AppConfig, не используется** |

**Факт:** `cluster_geo_filter`, `cluster_tie_breaker`, `cluster_type_resolution` парсятся и хранятся в `AppConfig` (строки 48-50, 401-403 config/schema.py), но НЕ передаются в `ClusteringEngine` (`service_factory.py:71-76`) и НЕ подключены ни к какой логике. Это config-заглушки для будущей реализации.

---

## 8. Что фактически конфигурируется сегодня

1. **Набор активных линз** — можно исключить линзы. Например, `CLUSTER_ACTIVE_LENSES=topic_micro,failure_systemic` включит только две.
   - **Критично:** orchestrator использует только `active_lenses[0]`. Порядок в списке определяет, по какой линзе создаётся issue.

2. **CLUSTER_MIN_SIZE** — минимум историй для promotion. Default=8 означает, что issue создаётся только при ≥8 историях в кластере по первому линзу.

3. **CLUSTER_READINESS_THRESHOLD** — порог readiness. Фактически игнорируется в orchestrator (см. п.5).

**Что НЕ конфигурируется:**
- Алгоритм извлечения сигналов (хардкод keyword-matching)
- Язык keyword-matching (только English)
- Веса линз при агрегации (все одинаковы)
- Приоритет линза для создания issue (только первый в списке)
- Источник сигналов (GPT canonical не используется)

---

## 9. Архитектурные ограничения текущей реализации

### 9.1 Один линз для создания issue

`process_story()` использует только `active_lenses[0]`. Если topic_micro кластер → 2 истории "road damage" и 2 истории "water leak" — это 4 истории в одном кластере TOPIC=infrastructure. Но это семантически разные проблемы.

Линз failure_micro различил бы их: "road" → `quality_gap`, "water/leak" → `service_disruption`. Но failure_micro не задействован при создании issue.

### 9.2 Сигналы не персистируются

`infer_signals_from_narrative()` вызывается каждый раз при `process_story()` для всех READY_FOR_PROFILE историй. Нет кэша сигналов в БД — пересчёт при каждом вызове.

### 9.3 GPT canonical данные игнорируются

StoryRecord хранит `narrative_canonical_type` и `narrative_canonical_labels` (из GPT через intake). Эти поля имеют прямой mapping на SYSTEM_FAILURE / TOPIC / labels. Но clustering их не читает — применяет keyword-matching к сырому тексту.

### 9.4 DESIRED_STATE и RELEVANCE — константы

Два из шести измерений не несут информации (`stable_public_service`, `high` для всех). Clustering по линзам `relevance_systemic` объединяет 100% историй в один кластер — т.к. все имеют RELEVANCE=`high`.

### 9.5 Языковой барьер

Эстонские и русские нарративы ("Katki läinud tänav", "Сломанная дорога") не содержат English keywords → получают дефолтные значения: TOPIC=`public_service`, SYSTEM_FAILURE=`quality_gap`. Две семантически идентичные истории на разных языках попадут в разные кластеры, если одна написана по-английски.

---

## 10. Технические возможности для расширения

### 10.1 Подключить GPT canonical → сигналы (GAP-IMP-02)

Уже есть `StoryRecord.narrative_canonical_type`, `StoryRecord.narrative_canonical_labels`. Маппинг:

```python
# Пример маппинга (не реализован)
CANONICAL_TYPE_TO_SYSTEM_FAILURE = {
    "INCIDENT": "service_disruption",
    "SERVICE_REQUEST": "restore_access",
    "IMPROVEMENT": "quality_gap",
}
CANONICAL_LABEL_TO_TOPIC = {
    "infrastructure": "infrastructure",
    "waste": "public_service",
    "safety": "infrastructure",
}
```

Это устранило бы языковой барьер — GPT разговаривает с гражданином на его языке и возвращает canonical поля, независимые от языка нарратива.

### 10.2 Персистировать StoryProfileSignals в БД

Вычислять сигналы один раз при intake, хранить в отдельной таблице `story_signals`. Clustering использует готовые векторы, а не пересчитывает при каждом вызове.

### 10.3 Использовать несколько линз при создании issue

Сейчас: `first_lens = active_lenses[0]` (hardcode).  
Вместо этого: найти пересечение кластеров по 2+ линзам → более точный кластер.

```python
# Пример (не реализован): пересечение topic_micro + failure_systemic
topic_cluster = memberships[story_id]["topic_micro"]
failure_cluster = memberships[story_id]["failure_systemic"]
refined_members = [s for s in profiles
                   if memberships[s.story_id]["topic_micro"] == topic_cluster
                   and memberships[s.story_id]["failure_systemic"] == failure_cluster]
```

### 10.4 Передать cluster_geo_filter в ClusteringEngine

Config-заглушка `CLUSTER_GEO_FILTER` уже парсится. При наличии `story.geo` (normalized_label) можно группировать только истории из одного гео-района:

```python
# Пример (не реализован)
if geo_filter != "any":
    ready_stories = [s for s in ready_stories
                     if s.geo and s.geo.normalized_label == target.geo.normalized_label]
```

Требует сначала GAP-IMP-03 (geo persistence в Supabase).

### 10.5 Реализовать cluster_type_resolution = canonical_priority

Config-заглушка. Логика: если все истории в кластере имеют одинаковый `narrative_canonical_type` → использовать его как issue_type вместо keyword-derived `_derive_issue_type()`.

---

## 11. Семантические возможности для расширения

### 11.1 Новые линзы

| Потенциальный линз | Измерение | Смысл |
|-------------------|-----------|-------|
| `geo_district` | GEO (новое) | Кластеризация по административному районам Таллина |
| `institution_responsible` | INSTITUTION (новое) | Ответственное ведомство: Tallinn Transpordi Amet, AS Tallinna Vesi |
| `urgency_level` | URGENCY (новое) | срочная → дорожная авария, несрочная → просьба покрасить скамейку |
| `citizen_sentiment` | SENTIMENT (новое) | повторная жалоба (frustrated) vs. первичная |

### 11.2 Geo-кластеризация

Если `story.geo.normalized_label` персистирована (требует GAP-IMP-03), можно объединять истории по Таллинским районам: Kesklinn, Lasnamäe, Mustamäe и т.д. Это даёт кластеры типа "5 жалоб на дороги в Lasnamäe" — напрямую адресует городской администрации.

### 11.3 Taxonomy-aware labelling

`story-label-taxonomy.md` определяет canonical labels. Текущий `_derive_labels()` использует English keywords и не знает о taxonomy. GPT уже выдаёт taxonomy-совместимые labels — нужно только их читать.

### 11.4 Weighted clustering (по повторяемости)

Recurrent-истории (REPEATABILITY=`recurrent`) могут получать повышенный вес при подсчёте readiness_score — т.к. повторная жалоба от разных граждан означает системную проблему, а не единичный инцидент.

### 11.5 Институциональная маршрутизация

Когда кластер сформирован → нужно определить ответственное ведомство. Текущий pipeline этого не делает. Новый линз `institution_responsible` позволит строить кластеры сразу с routing hint для SPA-дашборда.

---

## 12. Сводная таблица состояния

| Компонент | Состояние | Примечание |
|-----------|-----------|------------|
| SignalDimension (6) | Реализовано | 2 из 6 вырождены (DESIRED_STATE, RELEVANCE) |
| ClusterLens (6) | Реализовано | Вычисляются все, используется только первый |
| infer_signals_from_narrative() | Реализовано | English-only, без GPT canonical |
| stable_cluster_id() | Реализовано | Детерминирован, hash-based |
| readiness_score_for_cluster() | Реализовано | Hardcode=100 в orchestrator override |
| PromotionGatePolicy | Реализовано | min_stories актуален; readiness bypassed |
| CLUSTER_ACTIVE_LENSES | Конфигурируется | Порядок = приоритет (только [0] используется) |
| CLUSTER_MIN_SIZE | Конфигурируется | Активный gate |
| CLUSTER_READINESS_THRESHOLD | Конфигурируется | Parsed, но bypassed в orchestrator |
| CLUSTER_GEO_FILTER | Config-заглушка | Parsed, не подключён |
| CLUSTER_TIE_BREAKER | Config-заглушка | Parsed, не подключён |
| CLUSTER_TYPE_RESOLUTION | Config-заглушка | Parsed, не подключён |
| GPT canonical → signals | Не реализовано | GAP-IMP-02 |
| Geo clustering | Не реализовано | Требует GAP-IMP-03 |
| Multi-lens intersection | Не реализовано | Архитектурная возможность |
| Signal persistence in DB | Не реализовано | Пересчёт при каждом вызове |
