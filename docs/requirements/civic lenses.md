# Civic Lenses: публичный гражданский слой кластеризации

> **Назначение.** Продуктовая декларация для публичной DOGEstonia-ноды. Определяет, какие линзы кластеризации являются гражданскими, почему клиентские линзы в публичный слой не входят, и какие конкретные константы нужно использовать в конфигурации.

---

## 1. Принцип: гражданские линзы — не клиентские

В публичной DOGEstonia-ноде фиксируем только **civic core lenses** — линзы, которые отражают гражданскую реальность, а не внутренние задачи клиента.

Клиентские линзы типа `department_responsible`, `budget_category`, `procurement_priority`, `maintenance_team` — **не входят** в public civic layer. Они могут существовать в частной инсталляции поверх civic слоя, но не заменяют его.

**Публичная нода — это гражданская система, не муниципальная.** Она отвечает на вопросы жителя, города и гражданского общества.

---

## 2. Core Signal Dimensions

Шесть осей, по которым гражданская жалоба описывается в нормализованном виде:

```python
CIVIC_CORE_SIGNAL_DIMENSIONS = (
    "civic_domain",         # о какой сфере жизни жалоба
    "failure_pattern",      # как именно система ломается
    "civic_weight",         # насколько сигнал общественно значим
    "geographic_district",  # где проблема проявляется
    "desired_outcome",      # чего человек хочет вместо проблемы
    "affected_group",       # кого проблема затрагивает
)
```

| Dimension | Что фиксирует | Аудитория |
|-----------|--------------|-----------|
| `civic_domain` | о какой сфере жизни жалоба | Житель |
| `failure_pattern` | как именно система ломается | Государство |
| `civic_weight` | насколько сигнал общественно значим | Публичное управление |
| `geographic_district` | где проблема проявляется | Житель + город |
| `desired_outcome` | чего человек хочет вместо проблемы | Бизнес / НКО |
| `affected_group` | кого проблема затрагивает | Equity / service design |

---

## 3. Core Civic Lenses

### Минимальный обязательный слой (MVP)

Четыре линзы, на которых публичная нода уже может строить осмысленную кластеризацию:

```python
CIVIC_CORE_LENSES_MVP = (
    "civic_domain_micro",       # тематика жалобы: roads, transport, housing...
    "failure_pattern_micro",    # тип поломки: broken_infrastructure, delay...
    "civic_weight_systemic",    # системность: systemic_pattern, recurring_issue...
    "geographic_district_micro" # район: lasnamäe, kesklinn...
)
```

### Полный гражданский слой

Все шесть линз — для максимальной аналитической ценности:

```python
CIVIC_CORE_LENSES_FULL = (
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "geographic_district_micro",
    "desired_outcome_local",    # что хотят люди: better_maintenance, digital_fix...
    "affected_group_local",     # кто пострадал: residents, elderly_context, parents...
)
```

---

## 4. Lens Registry

Машиночитаемое описание каждой линзы — для API-ответов, i18n, SPA-отображения:

```python
CIVIC_LENS_REGISTRY = {
    "civic_domain_micro": {
        "dimension": "civic_domain",
        "scope": "micro",
        "status": "stable",
        "audience": "citizen",
        "question": "What is this complaint about?",
        "public_meaning": "Groups stories by civic topic, such as roads, transport, housing, or safety.",
    },
    "failure_pattern_micro": {
        "dimension": "failure_pattern",
        "scope": "micro",
        "status": "stable",
        "audience": "city_government",
        "question": "How exactly is the system failing?",
        "public_meaning": "Groups stories by the type of failure: delay, broken infrastructure, unclear rules, service unavailable, and similar patterns.",
    },
    "civic_weight_systemic": {
        "dimension": "civic_weight",
        "scope": "systemic",
        "status": "stable",
        "audience": "public_governance",
        "question": "Is this an isolated complaint or a broader civic signal?",
        "public_meaning": "Groups stories by civic significance, such as systemic pattern, recurring issue, public cost, or equity access.",
    },
    "geographic_district_micro": {
        "dimension": "geographic_district",
        "scope": "micro",
        "status": "stable",
        "audience": "citizen_and_city",
        "question": "Where is this problem happening?",
        "public_meaning": "Groups stories by normalized district or local area.",
    },
    "desired_outcome_local": {
        "dimension": "desired_outcome",
        "scope": "local",
        "status": "stable",
        "audience": "citizen_business_ngo",
        "question": "What improvement do people want?",
        "public_meaning": "Groups stories by the kind of outcome citizens are asking for.",
    },
    "affected_group_local": {
        "dimension": "affected_group",
        "scope": "local",
        "status": "stable",
        "audience": "equity_and_service_design",
        "question": "Who is affected by this problem?",
        "public_meaning": "Groups stories by affected population: residents, parents, elderly people, commuters, disabled people, and similar groups.",
    },
}
```

---

## 5. Рекомендуемые значения CLUSTER_ACTIVE_LENSES

Для **production-safe MVP** (минимальный набор, максимальная надёжность):

```
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic
```

Для MVP **с районностью** (рекомендуется):

```
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,geographic_district_micro
```

Для **полного публичного слоя**:

```
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,civic_weight_systemic,geographic_district_micro,desired_outcome_local,affected_group_local
```

---

## 6. Primary Lens

**Рекомендация:** `CLUSTER_PRIMARY_LENS=failure_pattern_micro`

Не `civic_domain_micro` — потому что она слишком широкая:

```
civic_domain_micro  = "дороги"               # категориальная — слишком широко
failure_pattern_micro = "broken_infrastructure"  # actionable — ведёт к конкретному действию
```

`failure_pattern_micro` — это линза, которая напрямую описывает *что нужно сделать городу*. Именно из неё создаётся primary issue.

---

## 7. Прочие config defaults

```
CLUSTER_ID_ALGORITHM=sha256
CLUSTER_MIN_SIZE=5
CLUSTER_READINESS_THRESHOLD=60
```

| Параметр | Значение | Обоснование |
|----------|----------|-------------|
| `CLUSTER_ID_ALGORITHM` | `sha256` | Детерминизм между перезапусками процесса (INV-01) |
| `CLUSTER_MIN_SIZE` | `5` | Достаточная статистическая значимость для civic сигнала |
| `CLUSTER_READINESS_THRESHOLD` | `60` | Кластер из 2 systemic историй (score=60) уже проходит gate |

---

## 8. Формат canonical issue key

Для разработки зафиксирован формат ключа кластера:

```
{lens}:{dimension}:{value}:{scope}
```

Пример:

```
failure_pattern_micro:failure_pattern:broken_infrastructure:micro
civic_domain_micro:civic_domain:roads:micro
civic_weight_systemic:civic_weight:systemic_pattern:systemic
geographic_district_micro:geographic_district:lasnamäe:micro
```

---

## 9. Stable cluster ID

```python
cluster_id = sha256(f"{lens}:{cluster_key}")
```

Формат результата:

```
cluster:{lens}:{10_digit_numeric_hash}
```

Примеры:

```
cluster:failure_pattern_micro:1827364501
cluster:civic_domain_micro:0473821956
cluster:civic_weight_systemic:0912847365
cluster:geographic_district_micro:3847201956
```

Алгоритм детерминистичен: одна и та же пара `(lens, cluster_key)` всегда даёт один и тот же `cluster_id` — независимо от перезапуска Python-процесса.

---

## 10. Итоговый блок для передачи разработчику

```python
PUBLIC_CIVIC_CORE_LENS_IDS = (
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "geographic_district_micro",
    "desired_outcome_local",
    "affected_group_local",
)

PUBLIC_CIVIC_PRIMARY_LENS = "failure_pattern_micro"

PUBLIC_CIVIC_SIGNAL_DIMENSIONS = (
    "civic_domain",
    "failure_pattern",
    "civic_weight",
    "geographic_district",
    "desired_outcome",
    "affected_group",
)

PUBLIC_CIVIC_CLUSTER_ID_ALGORITHM = "sha256"
PUBLIC_CIVIC_CLUSTER_MIN_SIZE = 5
PUBLIC_CIVIC_READINESS_THRESHOLD = 60
```

**Главное решение:** публичная нода кластеризует по гражданским линзам. Клиентские линзы добавляются только поверх этого слоя, не заменяя его.
