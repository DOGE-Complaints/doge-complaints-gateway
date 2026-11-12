# 03. SOA и Service Factory

## Концепция

Архитектура сервисов построена на двух принципах:

**1. Protocol-based interfaces** — каждый репозиторий/стор описан как `Protocol` в `domain/contracts.py`. Нет ABCs, нет наследования. Любой класс, у которого есть нужные методы, удовлетворяет Protocol (structural subtyping).

**2. Service Factory** — единственное место, где infrastructure (репозитории) связывается с application (сервисами). Factory знает, какой репозиторий подать в какой сервис. Снаружи фабрики это невидимо.

Результат: в сервисе `StoryIntakeService` нет импорта `SupabaseStoryRepository`. Сервис знает только `StoryRepository(Protocol)` — ему всё равно, как реализован бэкенд.

## Реализация в проекте

### Слой 1: Domain Protocols (`domain/contracts.py`)

```python
class StoryRepository(Protocol):
    def save_story(self, record: StoryRecord) -> StoryRecord: ...
    def get_story(self, story_id: str) -> StoryRecord | None: ...
    def list_stories(self) -> list[StoryRecord]: ...
    def list_stories_ready_for_clustering(self) -> list[StoryRecord]: ...
    def update_lifecycle_status(self, story_id: str, status: StoryLifecycleStatus) -> None: ...

class IdempotencyRepository(Protocol):
    def get_by_key(self, key: str) -> IdempotencyRecord | None: ...
    def save(self, record: IdempotencyRecord) -> IdempotencyRecord: ...

class StorySignalStore(Protocol):
    def save_signals(self, story_id: str, policy: str, signals: Mapping[str, str]) -> None: ...
    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None: ...

class ClusterMembershipStore(Protocol):
    def save_membership(self, story_id: str, lens: str, cluster_id: str) -> None: ...
    def get_cluster_members(self, cluster_id: str, lens: str) -> list[str]: ...
```

Все Protocol классы живут в `domain/` — слое без инфраструктурных зависимостей. Domain не импортирует httpx, sqlite, fastapi.

### Слой 2: Три реализации каждого Protocol

| Protocol | InMemory | SQLite | Supabase |
|----------|----------|--------|----------|
| `StoryRepository` | `InMemoryStoryRepository` | `SqliteStoryRepository` | `SupabaseStoryRepository` |
| `IdempotencyRepository` | `InMemoryIdempotencyRepository` | `SqliteIdempotencyRepository` | `SupabaseIdempotencyRepository` |
| `StorySignalStore` | `InMemoryStorySignalStore` | `SqliteStorySignalStore` | `SupabaseStorySignalStore` |
| `ClusterMembershipStore` | `InMemoryClusterMembershipStore` | `SqliteClusterMembershipStore` | `SupabaseClusterMembershipStore` |

`InMemory*` — в `infrastructure/repositories.py`  
`Sqlite*` — в `infrastructure/db_sqlite.py`  
`Supabase*` — в `infrastructure/db_supabase.py`

### Слой 3: ServiceFactory Protocol (`application/factory.py`)

```python
class ServiceFactory(Protocol):
    @property
    def config(self) -> AppConfig: ...

    def get_health_service(self) -> HealthService: ...
    def get_story_intake_service(self) -> StoryIntakeService: ...
    def get_story_cluster_orchestrator(self) -> StoryClusterOrchestrator: ...
    def get_issue_create_service(self) -> IssueCreateService: ...
    def get_issue_projection_read_store(self) -> IssueProjectionReadStore: ...
    def get_clustering_engine(self) -> ClusteringEngine: ...
    def get_issue_promotion_service(self) -> IssuePromotionService: ...
    def get_issue_projection_service(self) -> IssueProjectionService: ...
    def get_story_projection_policy(self) -> StoryToProjectionPolicy: ...
    def get_evidence_pack_service(self) -> EvidencePackService: ...
    def get_geo_service(self) -> GeoService: ...
    def get_signal_profile_service(self) -> SignalProfileService: ...
```

`ServiceFactory` — это тоже Protocol. Можно подменить всю фабрику в тестах, реализовав Protocol.

### Слой 4: DefaultServiceFactory (`infrastructure/service_factory.py`)

```python
@dataclass(frozen=True)
class DefaultServiceFactory:
    health_repository: HealthRepository
    story_repository: StoryRepository              # ← Protocol, не конкретный класс
    idempotency_repository: IdempotencyRepository
    signal_profile_repository: SignalProfileRepository
    issue_candidate_store: IssueCandidateStore
    review_audit_log_repository: ReviewAuditLogRepository
    evidence_pack_repository: EvidencePackRepository
    geo_service: GeoService
    config: AppConfig
    story_embedding_store: StoryEmbeddingStore | None = None
    issue_projection_store: IssueProjectionReadWriteStore | None = None
    story_signal_store: StorySignalStore | None = None
    cluster_membership_store: ClusterMembershipStore | None = None

    def get_story_intake_service(self) -> StoryIntakeService:
        return StoryIntakeService(
            repository=self.story_repository,             # инжектим Protocol
            idempotency_repository=self.idempotency_repository,
            geo_service=self.geo_service,
            story_signal_store=self.story_signal_store,
            log_debug_dir=self.config.log_debug_dir,
        )

    def get_story_cluster_orchestrator(self) -> StoryClusterOrchestrator:
        return StoryClusterOrchestrator(
            story_repository=self.story_repository,
            clustering_engine=self.get_clustering_engine(),
            issue_create_service=self.get_issue_create_service(),
            story_signal_store=self.story_signal_store,
            cluster_membership_store=self.cluster_membership_store,
        )
```

Каждый `get_*()` метод создаёт новый экземпляр сервиса с нужными зависимостями. Сервисы не кешируются — кешируется только `ApiDependencies` (в DI layer).

### Слой 5: `provide_service_factory()` — выбор backend (`infrastructure/providers.py`)

```python
def provide_service_factory(config: AppConfig | None = None) -> ServiceFactory:
    resolved_config = config or provide_app_config()  # читает env + .env

    # default: InMemory для всех репозиториев
    story_repository = InMemoryStoryRepository()
    story_signal_store: StorySignalStore = InMemoryStorySignalStore()
    # ... все остальные InMemory*

    if resolved_config.db_backend == "supabase" and ...:
        supabase_db = SupabaseDatabase.from_http(
            supabase_url=resolved_config.supabase_url,
            service_role_key=resolved_config.supabase_service_role,
            timeout_s=float(resolved_config.request_timeout_s),
        )
        story_repository = SupabaseStoryRepository(supabase_db)
        story_signal_store = SupabaseStorySignalStore(supabase_db)
        # ... остальные Supabase*

    return DefaultServiceFactory(
        story_repository=story_repository,
        story_signal_store=story_signal_store,
        config=resolved_config,
        ...
    )
```

Переключение backend = одна точка в `providers.py`. Снаружи невидимо.

---

## Граф зависимостей (упрощённый)

```
provide_service_factory()
    ├── DB_BACKEND=in_memory  →  InMemory* repositories
    ├── DB_BACKEND=supabase   →  SupabaseDatabase → Supabase* repositories
    └── DB_BACKEND=sqlite     →  SqliteDatabase → Sqlite* repositories
           ↓
    DefaultServiceFactory(repositories...)
           ↓
    get_story_intake_service()    →  StoryIntakeService(repository, geo_service, ...)
    get_story_cluster_orchestrator() →  StoryClusterOrchestrator(story_repository, ...)
    get_issue_create_service()    →  IssueCreateService(promotion_service, ...)
```

---

## Добавить новый сервис: пошаговый рецепт

### Шаг 1: Protocol в domain

```python
# domain/contracts.py
class MyStore(Protocol):
    def save(self, record: MyRecord) -> None: ...
    def get(self, id: str) -> MyRecord | None: ...
```

### Шаг 2: InMemory реализация

```python
# infrastructure/repositories.py
class InMemoryMyStore:
    def __init__(self):
        self._data: dict[str, MyRecord] = {}

    def save(self, record: MyRecord) -> None:
        self._data[record.id] = record

    def get(self, id: str) -> MyRecord | None:
        return self._data.get(id)
```

### Шаг 3: Supabase реализация

```python
# infrastructure/db_supabase.py
class SupabaseMyStore:
    def __init__(self, db: SupabaseDatabase):
        self._db = db

    def save(self, record: MyRecord) -> None:
        self._db._request(
            method="POST",
            path="/rest/v1/my_table",
            json_body={"id": record.id, ...},
            prefer="resolution=merge-duplicates",
        )

    def get(self, id: str) -> MyRecord | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/my_table",
            params={"id": f"eq.{id}", "limit": "1"},
        )
        return MyRecord(...) if rows else None
```

### Шаг 4: В DefaultServiceFactory

```python
# infrastructure/service_factory.py
@dataclass(frozen=True)
class DefaultServiceFactory:
    my_store: MyStore | None = None      # ← добавить поле

    def get_my_service(self) -> MyService:
        return MyService(store=self.my_store)
```

### Шаг 5: В ServiceFactory Protocol

```python
# application/factory.py
class ServiceFactory(Protocol):
    def get_my_service(self) -> MyService: ...  # ← добавить метод
```

### Шаг 6: В providers.py — выбор реализации

```python
my_store: MyStore = InMemoryMyStore()  # default

if resolved_config.db_backend == "supabase":
    my_store = SupabaseMyStore(supabase_db)

return DefaultServiceFactory(my_store=my_store, ...)
```

### Шаг 7: В ApiDependencies

```python
# dependencies.py
@dataclass(frozen=True)
class ApiDependencies:
    my_service: MyService           # ← добавить

def build_api_dependencies() -> ApiDependencies:
    return ApiDependencies(
        my_service=service_factory.get_my_service(),   # ← добавить
        ...
    )
```

---

## Шаги репликации в новом проекте

### 1. Определить domain Protocols

Для каждого хранилища данных → Protocol с методами CRUD в `domain/contracts.py`.

### 2. Создать InMemory реализации

Все тесты без Supabase работают через InMemory — реализуй их первыми.

### 3. Создать Supabase реализации

По паттерну `_db._request(method, path, ...)` из `infrastructure/db_supabase.py`.

### 4. ServiceFactory Protocol

Список `get_*()` методов для каждого сервиса — контракт фабрики.

### 5. DefaultServiceFactory

`@dataclass(frozen=True)` принимает репозитории, отдаёт сервисы через `get_*()`.

### 6. provide_service_factory() — switch

Одна функция, которая на основе `AppConfig.db_backend` выбирает реализации и собирает фабрику.

### Pitfalls

- Protocol не является базовым классом — `isinstance(obj, StoryRepository)` вернёт True только при `runtime_checkable`. Для тайп-чекинга используй `mypy`/`pyright`
- `DefaultServiceFactory` создаёт новые сервисы при каждом вызове `get_*()` — если сервис имеет heavy init, рассмотри кеширование на уровне фабрики (но осторожно с shared state)
- Все `Optional` поля в DefaultServiceFactory должны быть проверены внутри `get_*()` методов — иначе `AttributeError` при обращении к `None`
