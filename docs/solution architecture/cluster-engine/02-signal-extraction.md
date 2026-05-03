# Cluster Engine — Signal Extraction Pipeline

---

## 1. Архитектура источников сигналов

```
StoryRecord
  ├─ narrative_canonical_type   (GPT)
  ├─ narrative_canonical_labels (GPT) ["roads", "broken_infrastructure", "recurring_issue"]
  ├─ narrative_original_text    (user)
  └─ geo.normalized_label       (geo service)
          │
          ▼
  CLUSTER_SIGNAL_SOURCE (env)
          │
    ┌─────┼──────┐
    │     │      │
 canonical keyword hybrid
    │     │      │
    ▼     │      ▼
infer_signals_from_canonical()   ← primary (language-agnostic)
          │
          ▼ (если canonical_labels пустой)
infer_signals_from_narrative()   ← legacy fallback
          │
          ▼
    dict[str, str]               ← StoryProfileSignals.signals
```

**Инвариант:** функция всегда возвращает все 6 новых SignalDimension ключей. Отсутствие данных → `"unknown"` (не None, не пустая строка).

---

## 2. Vocabulary Registries (src/core/cluster/vocabulary.py)

Новый файл. Все frozenset верифицированы по `GPT UI/instructions/story-label-taxonomy.md` §4.

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

# Порядок определяет приоритет при выборе dominant civic_weight
CIVIC_SIGNAL_PRIORITY: tuple[str, ...] = (
    "systemic_pattern",   # 1 — системный сбой, не единичный
    "public_cost",        # 2 — публичные издержки
    "not_only_me",        # 3 — другие тоже страдают
    "recurring_issue",    # 4 — повторяется
    "equity_access",      # 5 — неравный доступ
    "trust_in_services",  # 6 — потеря доверия
    "city_for_people",    # 7 — стратегический ориентир
)
CIVIC_WEIGHT_DEFAULT = "isolated"   # дефолт при отсутствии civic_signal labels

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
AFFECTED_GROUP_DEFAULT = "general_public"

# Версионирование политики извлечения — зашита в константу
CANONICAL_EXTRACTION_POLICY = "v2.canonical"
KEYWORD_EXTRACTION_POLICY   = "v1.keyword"
```

---

## 3. infer_signals_from_canonical() (src/core/profile/enrichment.py)

Новая функция. Старая `infer_signals_from_narrative()` сохраняется для `CLUSTER_SIGNAL_SOURCE=keyword`.

```python
def infer_signals_from_canonical(
    canonical_type: str | None,
    canonical_labels: tuple[str, ...],
    geo_normalized_label: str | None = None,
) -> dict[str, str]:
    """Extract cluster signals from GPT canonical fields.

    Language-agnostic. Works regardless of narrative language.
    canonical_labels must contain only keys from story-label-taxonomy.md §4.
    """
    labels = set(canonical_labels)

    # civic_domain: first matching label preserving canonical_labels order
    civic_domain = next(
        (label for label in canonical_labels if label in CIVIC_DOMAIN_VOCABULARY),
        "unknown",
    )

    # failure_pattern: first matching label
    failure_pattern = next(
        (label for label in canonical_labels if label in FAILURE_PATTERN_VOCABULARY),
        "unknown",
    )

    # civic_weight: highest-priority civic_signal label
    civic_weight = next(
        (priority_label for priority_label in CIVIC_SIGNAL_PRIORITY if priority_label in labels),
        CIVIC_WEIGHT_DEFAULT,
    )

    # desired_outcome: first matching label
    desired_outcome = next(
        (label for label in canonical_labels if label in DESIRED_OUTCOME_VOCABULARY),
        "unknown",
    )

    # affected_group: first matching label
    affected_group = next(
        (label for label in canonical_labels if label in AFFECTED_SCOPE_VOCABULARY),
        AFFECTED_GROUP_DEFAULT,
    )

    # geographic_district: from StoryGeoSnapshot
    geographic_district = (
        geo_normalized_label.strip().lower()
        if geo_normalized_label and geo_normalized_label.strip()
        else "unknown"
    )

    return {
        SignalDimension.CIVIC_DOMAIN.value:        civic_domain,
        SignalDimension.FAILURE_PATTERN.value:     failure_pattern,
        SignalDimension.CIVIC_WEIGHT.value:        civic_weight,
        SignalDimension.DESIRED_OUTCOME.value:     desired_outcome,
        SignalDimension.AFFECTED_GROUP.value:      affected_group,
        SignalDimension.GEOGRAPHIC_DISTRICT.value: geographic_district,
    }
```

### 3.1 Порядок labels: почему важен

GPT должен возвращать labels с наиболее конфидентными первыми. В `story-label-taxonomy.md` §4 labels сгруппированы по axes, но конкретный порядок внутри группы документом не фиксирован.

**Правило для extraction:** `civic_domain` и `failure_pattern` берут ПЕРВЫЙ matching label из `canonical_labels` в том порядке, в котором они присланы GPT. `civic_weight` использует `CIVIC_SIGNAL_PRIORITY` — не порядок из labels, а предопределённую важность.

### 3.2 Fallback chain при CLUSTER_SIGNAL_SOURCE=hybrid

```python
def get_signals_for_story(
    story: StoryRecord,
    signal_source: str,  # из AppConfig
) -> dict[str, str]:
    if signal_source == "canonical":
        return infer_signals_from_canonical(
            story.narrative_canonical_type,
            story.narrative_canonical_labels,
            story.geo.normalized_label if story.geo else None,
        )
    if signal_source == "keyword":
        return infer_signals_from_narrative(story.narrative_original_text)
    # hybrid: canonical first, keyword fallback for missing fields
    canonical = infer_signals_from_canonical(
        story.narrative_canonical_type,
        story.narrative_canonical_labels,
        story.geo.normalized_label if story.geo else None,
    )
    if all(v != "unknown" for v in canonical.values()):
        return canonical
    # fallback для полей где canonical дал "unknown"
    keyword = infer_signals_from_narrative(story.narrative_original_text)
    return {
        key: (val if val != "unknown" else keyword.get(key, "unknown"))
        for key, val in canonical.items()
    }
```

---

## 4. Маппинг новых линз к Signal Dimensions (src/core/cluster/engine.py)

Обновить `lens_dimension()`:

```python
def lens_dimension(lens: ClusterLens) -> SignalDimension:
    mapping: dict[ClusterLens, SignalDimension] = {
        # ── Новые semantic линзы ──────────────────────────────────────
        ClusterLens.CIVIC_DOMAIN_MICRO:        SignalDimension.CIVIC_DOMAIN,
        ClusterLens.FAILURE_PATTERN_MICRO:     SignalDimension.FAILURE_PATTERN,
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC:     SignalDimension.CIVIC_WEIGHT,
        ClusterLens.DESIRED_OUTCOME_LOCAL:     SignalDimension.DESIRED_OUTCOME,
        ClusterLens.AFFECTED_GROUP_LOCAL:      SignalDimension.AFFECTED_GROUP,
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO: SignalDimension.GEOGRAPHIC_DISTRICT,
        # ── Legacy линзы ─────────────────────────────────────────────
        ClusterLens.TOPIC_MICRO:         SignalDimension.TOPIC,
        ClusterLens.NEED_LOCAL:          SignalDimension.NEED,
        ClusterLens.FAILURE_SYSTEMIC:    SignalDimension.SYSTEM_FAILURE,
        ClusterLens.FAILURE_MICRO:       SignalDimension.SYSTEM_FAILURE,
        ClusterLens.REPEATABILITY_LOCAL: SignalDimension.REPEATABILITY,
        ClusterLens.RELEVANCE_SYSTEMIC:  SignalDimension.RELEVANCE,
    }
    return mapping[lens]
```

Обновить `cluster_key_for_lens()`:

```python
def cluster_key_for_lens(profile: StoryProfileSignals, lens: ClusterLens) -> str:
    signals = profile.signals
    dimension = lens_dimension(lens)
    raw_value = str(signals.get(dimension.value, "unknown")).strip() or "unknown"

    # Новые semantic линзы
    _MICRO_LENSES = frozenset({
        ClusterLens.CIVIC_DOMAIN_MICRO,
        ClusterLens.FAILURE_PATTERN_MICRO,
        ClusterLens.AFFECTED_GROUP_LOCAL,  # local scope, micro suffix
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
    })
    _SYSTEMIC_LENSES = frozenset({
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
    })
    _LOCAL_LENSES = frozenset({
        ClusterLens.DESIRED_OUTCOME_LOCAL,
        ClusterLens.AFFECTED_GROUP_LOCAL,  # alternative
    })

    if lens in _SYSTEMIC_LENSES or lens in (ClusterLens.FAILURE_SYSTEMIC, ClusterLens.RELEVANCE_SYSTEMIC):
        return f"{lens.value}:{dimension.value}:{raw_value}:systemic"
    if lens in _LOCAL_LENSES or lens in (ClusterLens.NEED_LOCAL, ClusterLens.REPEATABILITY_LOCAL):
        return f"{lens.value}:{dimension.value}:{raw_value}:local"
    return f"{lens.value}:{dimension.value}:{raw_value}:micro"
```

---

## 5. Персистенция сигналов: flow в orchestrator

```
process_story(story_id)
    │
    ├─ story = story_repository.get_story(story_id)
    │
    ├─ ready_stories = list_stories_ready_for_clustering()
    │
    └─ для каждой story в ready_stories:
           │
           ├─ cached = signal_store.get_signals(story.story_id, policy)
           │
           ├─ если cached: использовать cached
           │
           └─ иначе:
                  signals = get_signals_for_story(story, signal_source)
                  signal_store.save_signals(story.story_id, policy, signals)
                  использовать signals
```

**Policy string:** `"v2.canonical"` при `CLUSTER_SIGNAL_SOURCE=canonical`, `"v1.keyword"` при keyword, `"v2.hybrid"` при hybrid. Позволяет параллельно хранить сигналы по разным политикам.

---

## 6. readiness_bonus для новых линз (engine.py)

```python
def lens_readiness_bonus(lens: ClusterLens) -> int:
    _HIGH_BONUS = frozenset({
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC,      # systemic pattern = приоритет
    })
    _MED_BONUS = frozenset({
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,  # гео-привязка повышает actionability
        ClusterLens.FAILURE_SYSTEMIC,           # legacy systemic
        ClusterLens.RELEVANCE_SYSTEMIC,         # legacy (degenerate, но bonus сохраняем)
    })
    if lens in _HIGH_BONUS:
        return 10
    if lens in _MED_BONUS:
        return 5
    return 0
```

---

## 7. Тесты для signal extraction (целевые)

| Тест | Суть |
|------|------|
| `test_canonical_signals_language_neutral` | ET-нарратив с `canonical_labels=["roads"]` → `civic_domain="roads"` |
| `test_civic_weight_priority_order` | Labels с `systemic_pattern` + `recurring_issue` → `civic_weight="systemic_pattern"` |
| `test_civic_weight_default_isolated` | Labels без civic_signal → `civic_weight="isolated"` |
| `test_hybrid_fallback_on_unknown` | canonical дал "unknown" для civic_domain, keyword имеет "road" → fallback применён |
| `test_vocabulary_completeness` | Все значения из taxonomy §4 присутствуют в vocabulary registries |
| `test_signal_persistence_read_after_write` | save → get возвращает те же данные |
| `test_signals_not_recomputed_if_cached` | При наличии записи в signal_store → get_signals_for_story не вызывается |
