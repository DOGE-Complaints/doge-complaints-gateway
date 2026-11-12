# 02. Dependency Injection

## Концепция

Проект использует **manual singleton DI** — не IoC контейнер, не Pydantic DI, не `dependency_injector`. Паттерн:

1. Один `@dataclass(frozen=True)` содержит все сервисы (`ApiDependencies`)
2. Функция `build_api_dependencies()` строит его один раз — создаёт фабрику, фабрика создаёт сервисы
3. `@lru_cache(maxsize=1)` делает из `_cached_dependencies()` singleton per process
4. FastAPI роуты получают singleton через `Depends(get_api_dependencies)` — FastAPI вызывает функцию per-request, но `lru_cache` возвращает то же самое

Почему не FastAPI native DI (нет `@injectable`): сервисы имеют сложные зависимости с persistence backend, который определяется при старте из env. `@lru_cache` гарантирует, что backend инициализируется ровно один раз.

## Реализация в проекте

**Файл:** `src/core/api/dependencies.py`

### `ApiDependencies` — контейнер всех сервисов

```python
@dataclass(frozen=True)
class ApiDependencies:
    health_service: HealthService
    story_intake_service: StoryIntakeService
    story_cluster_orchestrator: StoryClusterOrchestrator
    issue_create_service: IssueCreateService
    issue_projection_read_store: IssueProjectionReadStore
    config: AppConfig
    service_auth: ServiceTokenAuth
    metrics: ApiMetrics
    db_backend: str           # "in_memory" | "sqlite" | "supabase"
    db_ready: bool            # False если Supabase healthcheck упал при старте
    db_checks: dict[str, bool]  # {"connectivity": True, "schema": True, ...}
```

`frozen=True` — immutable после создания. Нельзя случайно заменить сервис в runtime.

`db_ready` и `db_checks` — результаты healthcheck Supabase при старте, пробрасываются в `/ready` ответ.

### `build_api_dependencies()` — сборка контейнера

```python
def build_api_dependencies() -> ApiDependencies:
    service_factory = provide_service_factory()   # ← читает env, выбирает backend
    db_backend = service_factory.config.db_backend

    # healthcheck для Supabase при старте
    if db_backend == "supabase":
        health_db = SupabaseDatabase.from_http(...)
        db_checks = {
            "connectivity": health_db.healthcheck(),
            "schema": health_db.required_tables_ready(),
            "columns": health_db.required_columns_ready(),
            "columns_v2": health_db.required_stories_intake_v2_columns_ready(),
            "policy_probe": health_db.service_role_policy_probe(),
        }
        db_ready = all(db_checks.values())

    return ApiDependencies(
        health_service=service_factory.get_health_service(),
        story_intake_service=service_factory.get_story_intake_service(),
        story_cluster_orchestrator=service_factory.get_story_cluster_orchestrator(),
        issue_create_service=service_factory.get_issue_create_service(),
        issue_projection_read_store=service_factory.get_issue_projection_read_store(),
        config=service_factory.config,
        service_auth=build_service_auth_from_env(),
        ...
    )
```

### Singleton pattern в `asgi_app.py`

```python
@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()

def _clear_api_dependencies_cache() -> None:
    _cached_dependencies.cache_clear()   # используется в тестах

def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()
```

`@lru_cache(maxsize=1)` — после первого вызова `build_api_dependencies()` результат кешируется. Все последующие вызовы `get_api_dependencies()` возвращают тот же объект.

`_clear_api_dependencies_cache()` нужен только для тестов — позволяет пересоздать singleton с другим env.

### Использование в роутах

```python
@app.get("/health")
async def health(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),  # ← FastAPI инжектирует
) -> JSONResponse:
    payload = handle_health(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload)
```

FastAPI вызывает `get_api_dependencies()` при каждом запросе, но `lru_cache` возвращает тот же `ApiDependencies` объект — overhead минимален.

### Защищённые роуты

```python
def require_service_auth(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    deps.service_auth.require(dict(request.headers.items()))   # бросает UnauthorizedError

@app.get("/protected/status", dependencies=[Depends(require_service_auth)])
async def protected_status(request: Request, deps: ApiDependencies = Depends(get_api_dependencies)):
    ...
```

`dependencies=[Depends(require_service_auth)]` — FastAPI вызывает эту функцию до handler. Если бросает `UnauthorizedError` → `unauthorized_handler` → 401.

### Backward compatibility alias

```python
HandlerDependencies = ApiDependencies  # используется в тестах и story docs
```

---

## Поток инициализации при старте

```
uvicorn starts
    ↓
FastAPI lifespan enters
    ↓
get_api_dependencies() → _cached_dependencies() [first call]
    ↓
build_api_dependencies()
    ↓
provide_service_factory()         ← читает DB_BACKEND из env
    ↓
SupabaseDatabase.from_http(...)   ← если DB_BACKEND=supabase
    ↓
healthcheck + schema checks
    ↓
service_factory.get_*_service()   ← создание сервисов
    ↓
ApiDependencies(...) cached       ← singleton сохранён
    ↓
lifespan yields                   ← сервер принимает запросы
```

---

## Шаги репликации в новом проекте

### 1. Создать `dependencies.py`

```python
from dataclasses import dataclass, field
from core.config import AppConfig, load_config_from_env
from core.infrastructure import provide_service_factory
# импорты ваших сервисов

@dataclass(frozen=True)
class ApiDependencies:
    # добавить все сервисы вашего приложения
    my_service: MyService
    config: AppConfig = field(default_factory=lambda: load_config_from_env({"APP_PROFILE": "demo", "API_BASE_URL": "http://localhost"}))
    service_auth: ServiceTokenAuth = field(default_factory=ServiceTokenAuth.disabled)
    db_backend: str = "in_memory"
    db_ready: bool = True
    db_checks: dict[str, bool] = field(default_factory=dict)


def build_api_dependencies() -> ApiDependencies:
    factory = provide_service_factory()
    # healthcheck если нужен
    return ApiDependencies(
        my_service=factory.get_my_service(),
        config=factory.config,
        service_auth=build_service_auth_from_env(),
        db_backend=factory.config.db_backend,
    )
```

### 2. Добавить singleton в `asgi_app.py`

```python
from functools import lru_cache
from core.api.dependencies import ApiDependencies, build_api_dependencies

@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()

def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()
```

### 3. Добавить healthcheck fields если есть remote backend

```python
if db_backend == "supabase":
    db = SupabaseDatabase.from_http(url, key)
    db_checks = {"connectivity": db.healthcheck(), "schema": db.required_tables_ready()}
    db_ready = all(db_checks.values())
```

### Pitfalls

- `lru_cache` кешируется на время процесса — при тестах нужно вызывать `_clear_api_dependencies_cache()` или использовать `monkeypatch` для env перед первым вызовом
- Если lifespan вызывает `get_api_dependencies()` при старте — singleton инициализируется до первого HTTP-запроса (это хорошо, иначе первый запрос будет с latency инициализации)
- `frozen=True` на dataclass предотвращает случайную мутацию сервисов — не убирай
- Не добавляй mutable state в `ApiDependencies` — это shared singleton
