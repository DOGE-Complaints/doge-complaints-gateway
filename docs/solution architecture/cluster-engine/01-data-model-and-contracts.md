# Cluster Engine — Data Model & Contracts

---

## 1. Domain types: изменения и дополнения

### 1.1 SignalDimension — новые оси (src/core/domain/contracts.py)

```python
class SignalDimension(StrEnum):
    # ── Новые (semantic, GPT-driven) ───────────────────────────────────
    CIVIC_DOMAIN        = "civic_domain"         # replaces TOPIC
    FAILURE_PATTERN     = "failure_pattern"      # replaces SYSTEM_FAILURE
    CIVIC_WEIGHT        = "civic_weight"         # replaces REPEATABILITY + RELEVANCE
    DESIRED_OUTCOME     = "desired_outcome"      # new
    AFFECTED_GROUP      = "affected_group"       # new
    GEOGRAPHIC_DISTRICT = "geographic_district"  # new

    # ── Legacy (deprecated, backward-compat, used with CLUSTER_SIGNAL_SOURCE=keyword) ──
    TOPIC         = "topic"           # @deprecated use CIVIC_DOMAIN
    SYSTEM_FAILURE = "system_failure" # @deprecated use FAILURE_PATTERN
    NEED          = "need"            # @deprecated
    DESIRED_STATE = "desired_state"   # @deprecated (constant value, no info)
    REPEATABILITY = "repeatability"   # @deprecated use CIVIC_WEIGHT
    RELEVANCE     = "relevance"       # @deprecated (constant value, no info)
```

### 1.2 StoryLifecycleStatus — добавить CLUSTERED

```python
class StoryLifecycleStatus(StrEnum):
    ACCEPTED         = "accepted"
    PARTIAL_READY    = "partial_ready"
    READY_FOR_PROFILE = "ready_for_profile"
    CLUSTERED        = "clustered"          # новый: story включена в promoted issue
```

Переход `READY_FOR_PROFILE → CLUSTERED` — только после успешного `IssueCreateService.create_issue()`.  
Откат при `PromotionStateError` — story остаётся в `READY_FOR_PROFILE` (orchestrator не вызывает update при исключении).

### 1.3 StoryRepository — новые методы протокола

```python
class StoryRepository(Protocol):
    def save_story(self, record: StoryRecord) -> StoryRecord: ...
    def get_story(self, story_id: str) -> StoryRecord | None: ...
    def list_stories(self) -> list[StoryRecord]: ...       # сохранить, но не использовать в clustering

    # ── Новые ───────────────────────────────────────────────
    def list_stories_ready_for_clustering(self) -> list[StoryRecord]:
        """DB-side filter по lifecycle_status = READY_FOR_PROFILE."""

    def update_lifecycle_status(
        self, story_id: str, status: StoryLifecycleStatus
    ) -> None:
        """Обновить статус без замены всего StoryRecord."""
```

**Реализации:**
- `InMemoryStoryRepository` — filter в Python над `self._store`
- `SQLiteStoryRepository` — `WHERE lifecycle_status = 'ready_for_profile'`
- `SupabaseStoryRepository` — `.eq("lifecycle_status", "ready_for_profile")`

### 1.4 ClusterLens — новые semantic линзы (src/core/cluster/types.py)

```python
class ClusterLens(StrEnum):
    # ── Новые (semantic, GPT canonical labels) ──────────────────────────
    CIVIC_DOMAIN_MICRO        = "civic_domain_micro"
    FAILURE_PATTERN_MICRO     = "failure_pattern_micro"
    CIVIC_WEIGHT_SYSTEMIC     = "civic_weight_systemic"
    DESIRED_OUTCOME_LOCAL     = "desired_outcome_local"
    AFFECTED_GROUP_LOCAL      = "affected_group_local"
    GEOGRAPHIC_DISTRICT_MICRO = "geographic_district_micro"

    # ── Legacy (keyword-based) ──────────────────────────────────────────
    TOPIC_MICRO         = "topic_micro"          # @deprecated
    NEED_LOCAL          = "need_local"           # @deprecated
    FAILURE_SYSTEMIC    = "failure_systemic"     # @deprecated
    FAILURE_MICRO       = "failure_micro"        # @deprecated
    REPEATABILITY_LOCAL = "repeatability_local"  # @deprecated
    RELEVANCE_SYSTEMIC  = "relevance_systemic"   # @deprecated (degenerate)
```

### 1.5 Cluster — добавить readiness_score

```python
@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    lens: ClusterLens
    members: tuple[ClusterMember, ...]
    readiness_score: int              # добавить
    readiness_factors: dict[str, int] # добавить
    key: str                          # добавить — cluster_key для debugging
```

### 1.6 ClusteringEngine — расширить параметры

```python
@dataclass(frozen=True)
class ClusteringEngine:
    active_lenses: tuple[ClusterLens, ...]
    primary_lens: ClusterLens         # из CLUSTER_PRIMARY_LENS; заменяет active_lenses[0]
    id_algorithm: str                 # "sha256" | "legacy_hash"
    signal_source: str                # "canonical" | "keyword" | "hybrid"
    geo_filter: str                   # "any" | district normalized_label
    tie_breaker: str                  # "lexical" | "oldest_first" | "systemic_priority"
    type_resolution: str              # "canonical_priority" | "majority" | "first"
```

---

## 2. Новые domain протоколы

### 2.1 StorySignalStore

```python
class StorySignalStore(Protocol):
    def save_signals(
        self,
        story_id: str,
        policy: str,              # e.g. "v2.canonical" | "v1.keyword"
        signals: dict[str, str],
    ) -> None: ...

    def get_signals(
        self,
        story_id: str,
        policy: str,
    ) -> dict[str, str] | None:
        """None если сигналы не вычислены для данной политики."""
```

**Реализации:**

| Класс | Хранилище |
|-------|-----------|
| `InMemoryStorySignalStore` | `dict[tuple[str,str], dict[str,str]]` keyed by `(story_id, policy)` |
| `SQLiteStorySignalStore` | таблица `story_signals` |
| `SupabaseStorySignalStore` | таблица `story_signals` |

### 2.2 ClusterMembershipStore

```python
class ClusterMembershipStore(Protocol):
    def save_membership(
        self,
        story_id: str,
        lens: str,
        cluster_id: str,
    ) -> None:
        """Upsert (story_id, lens) → cluster_id."""

    def get_cluster_members(
        self,
        cluster_id: str,
        lens: str,
    ) -> list[str]:
        """Все story_ids в кластере по данной линзе."""
```

**Реализации:** аналогично StorySignalStore.

### 2.3 IssueCandidateStore — дополнительный метод

```python
class IssueCandidateStore(Protocol):
    ...
    def find_promoted_by_cluster_id(
        self, cluster_id: str
    ) -> IssueCandidateRecord | None:
        """None если нет PROMOTED кандидата с данным cluster_id."""
```

---

## 3. Схема таблиц БД

### 3.1 story_signals (новая)

```sql
CREATE TABLE story_signals (
    story_id          TEXT        NOT NULL,
    extraction_policy TEXT        NOT NULL,   -- "v2.canonical" | "v1.keyword"
    signals_json      JSONB       NOT NULL,   -- {"civic_domain": "roads", ...}
    extracted_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (story_id, extraction_policy)
);

CREATE INDEX idx_story_signals_policy ON story_signals(extraction_policy);
```

### 3.2 cluster_memberships (новая)

```sql
CREATE TABLE cluster_memberships (
    story_id     TEXT        NOT NULL,
    lens         TEXT        NOT NULL,
    cluster_id   TEXT        NOT NULL,
    computed_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (story_id, lens)           -- upsert-friendly
);

CREATE INDEX idx_cluster_memberships_cluster ON cluster_memberships(cluster_id);
CREATE INDEX idx_cluster_memberships_lens    ON cluster_memberships(lens);
```

### 3.3 Изменение: stories — constraint на новый статус

```sql
-- При наличии CHECK constraint — обновить:
ALTER TABLE stories DROP CONSTRAINT IF EXISTS stories_lifecycle_check;
ALTER TABLE stories ADD CONSTRAINT stories_lifecycle_check
    CHECK (lifecycle_status IN (
        'accepted', 'partial_ready', 'ready_for_profile', 'clustered'
    ));
```

### 3.4 issue_candidate_store — индекс для find_promoted_by_cluster_id

```sql
-- Если issue_candidates таблица существует:
CREATE INDEX IF NOT EXISTS idx_issue_candidates_cluster_status
    ON issue_candidates(cluster_id, status);
```

### 3.5 issue_story_links (существует, не изменяем структуру)

```sql
-- Верифицирован по src/core/infrastructure/repositories.py
-- Структура остаётся, добавляем индекс если не было:
CREATE INDEX IF NOT EXISTS idx_issue_story_links_cluster ON issue_story_links(cluster_id);
```

---

## 4. Обновление AppConfig

### 4.1 Новые поля

```python
@dataclass(frozen=True)
class AppConfig:
    ...
    # Существующие (не менять)
    cluster_min_size: int
    cluster_readiness_threshold: int
    cluster_active_lenses: tuple[str, ...]
    cluster_geo_filter: str
    cluster_tie_breaker: str
    cluster_type_resolution: str

    # ── Новые ─────────────────────────────────────────────────────────
    cluster_primary_lens: str        # из CLUSTER_PRIMARY_LENS
    cluster_signal_source: str       # из CLUSTER_SIGNAL_SOURCE
    cluster_id_algorithm: str        # из CLUSTER_ID_ALGORITHM
```

### 4.2 Новые env specs и валидация

```python
# В ENV_SCHEMA добавить:
EnvSpec(
    name="CLUSTER_PRIMARY_LENS",
    required=False,
    default="civic_domain_micro",
    description="Primary lens for issue creation. Must be in CLUSTER_ACTIVE_LENSES.",
),
EnvSpec(
    name="CLUSTER_SIGNAL_SOURCE",
    required=False,
    default="canonical",
    description="Signal extraction source: canonical | keyword | hybrid.",
),
EnvSpec(
    name="CLUSTER_ID_ALGORITHM",
    required=False,
    default="sha256",
    description="Cluster ID hashing algorithm: sha256 | legacy_hash.",
),
```

**Validation в `load_config_from_env()`:**

```python
# CLUSTER_SIGNAL_SOURCE validation
_ALLOWED_SIGNAL_SOURCES = frozenset({"canonical", "keyword", "hybrid"})
cluster_signal_source = _require_value(source, name="CLUSTER_SIGNAL_SOURCE").strip().lower()
if cluster_signal_source not in _ALLOWED_SIGNAL_SOURCES:
    raise ConfigError(f"CLUSTER_SIGNAL_SOURCE must be one of: {sorted(_ALLOWED_SIGNAL_SOURCES)}")

# CLUSTER_ID_ALGORITHM validation
_ALLOWED_ID_ALGORITHMS = frozenset({"sha256", "legacy_hash"})
cluster_id_algorithm = _require_value(source, name="CLUSTER_ID_ALGORITHM").strip().lower()
if cluster_id_algorithm not in _ALLOWED_ID_ALGORITHMS:
    raise ConfigError(f"CLUSTER_ID_ALGORITHM must be one of: {sorted(_ALLOWED_ID_ALGORITHMS)}")

# CLUSTER_PRIMARY_LENS validation (после парсинга active_lenses):
cluster_primary_lens = _require_value(source, name="CLUSTER_PRIMARY_LENS").strip()
if cluster_primary_lens not in cluster_active_lenses:
    raise ConfigError(
        f"CLUSTER_PRIMARY_LENS={cluster_primary_lens!r} must be in CLUSTER_ACTIVE_LENSES."
    )
```

---

## 5. Service factory: обновление wiring

```python
# src/core/infrastructure/service_factory.py

@dataclass(frozen=True)
class DefaultServiceFactory:
    ...
    story_signal_store: StorySignalStore | None = None
    cluster_membership_store: ClusterMembershipStore | None = None

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

    def get_story_cluster_orchestrator(self) -> StoryClusterOrchestrator:
        return StoryClusterOrchestrator(
            story_repository=self.story_repository,
            clustering_engine=self.get_clustering_engine(),
            issue_create_service=self.get_issue_create_service(),
            signal_store=self.story_signal_store,
            membership_store=self.cluster_membership_store,
        )
```

**Fallback при None stores:** если `story_signal_store is None` → вычислять сигналы каждый раз (in-memory mode). Если `cluster_membership_store is None` → не персистировать memberships. Оба Optional — для обратной совместимости с текущими тестами.
