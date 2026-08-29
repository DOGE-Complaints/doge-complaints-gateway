# 01. FastAPI Transport Layer

## Концепция

HTTP Transport — тонкий слой между сетью и бизнес-логикой. Его задача: принять запрос, извлечь параметры, вызвать обработчик и вернуть ответ. Никакой бизнес-логики здесь нет — она вынесена в `handlers.py` и сервисы ниже.

Архитектурное правило: `asgi_app.py` **не импортирует** ничего из domain/application слоёв напрямую, кроме типов ошибок для exception handlers. Весь доступ к сервисам идёт через `ApiDependencies` (см. [02-dependency-injection.md](02-dependency-injection.md)).

## Реализация в проекте

**Файл:** `src/core/api/asgi_app.py`

### Создание приложения

```python
app = FastAPI(title="doge-complaints-gateway", version="0.1.0", lifespan=_lifespan)
```

`lifespan=` передаёт async context manager для startup/shutdown. FastAPI вызывает его при старте ASGI-сервера.

### ASGI Lifespan

```python
@asynccontextmanager
async def _lifespan(_: FastAPI):
    # startup
    deps = get_api_dependencies()          # инициализация DI singleton
    configure_logging(...)                 # настройка логирования
    cron_job = ClusterCronJob(...)         # запуск фонового cron
    cron_job.start()
    try:
        yield                              # сервер живёт здесь
    finally:
        cron_job.stop()                    # shutdown: остановить cron
```

Lifespan выполняет три задачи:
1. Форсирует инициализацию `ApiDependencies` singleton при старте (а не при первом запросе)
2. Конфигурирует логирование из `AppConfig`
3. Стартует/стопает `ClusterCronJob` (фоновый цикл кластеризации)

Сигналы `SIGINT`/`SIGTERM` перехватываются в `_install_signal_reason_hooks()` для логирования причины shutdown.

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-trace-id", "authorization"],
)
```

Разрешены только методы GET/POST/OPTIONS. Для предварительных CORS-запросов добавлены явные `OPTIONS` роуты:

```python
@app.options("/node/issues")
async def issues_options() -> Response:
    return Response(status_code=200)
```

### HTTP Middleware (трейс ошибок)

```python
@app.middleware("http")
async def runtime_exception_diagnostics(request: Request, call_next: Any) -> Any:
    trace_id = _read_trace_id(request)
    try:
        return await call_next(request)
    except Exception as exc:
        log_runtime_exception(..., trace_id=trace_id, path=request.url.path)
        raise
```

Middleware логирует необработанные исключения с `trace_id` и пробрасывает их вверх (не глотает).

### Exception Handlers

```python
@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request, exc) -> JSONResponse:
    return JSONResponse(content=..., status_code=401)

@app.exception_handler(ConfigError)
async def config_error_handler(request, exc) -> JSONResponse:
    return JSONResponse(content=..., status_code=500)
```

`UnauthorizedError` и `ConfigError` перехватываются на уровне приложения и возвращают envelope-ответ без stack trace.

### Структура роутов

```python
PUBLIC_ROUTES  = ("/health", "/ready", "/demo/auth-page", "/story-drafts", "/telemetry/label-misses", "/node/issues", "/node/network-pulse", "/node/emerging-signals")
PROTECTED_ROUTES = ("/protected/status", "/metrics")
```

Защищённые роуты используют `Depends(require_service_auth)`:

```python
@app.get("/protected/status", dependencies=[Depends(require_service_auth)])
async def protected_status(request: Request, deps: ApiDependencies = Depends(get_api_dependencies)):
    ...
```

`require_service_auth` проверяет `Authorization: Bearer <SERVICE_API_TOKEN>` через `deps.service_auth.require(headers)`.

### Паттерн роута (все 12 роутов)

```python
@app.post("/intake/stories")
async def intake_stories(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),   # ← инжекция DI
) -> JSONResponse:
    raw_body = await request.body()
    payload = json.loads(raw_body)
    envelope, status_code = handle_story_intake(              # ← логика в handlers.py
        deps, payload=payload, ..., trace_id=_read_trace_id(request)
    )
    return JSONResponse(content=envelope, status_code=status_code)
```

`asgi_app.py` не содержит бизнес-логики: только парсинг запроса → вызов handler → JSONResponse.

### Trace ID

```python
def _read_trace_id(request: Request) -> str:
    incoming = request.headers.get("x-trace-id")
    return ensure_trace_id(incoming)   # генерирует uuid4 если header отсутствует
```

Каждый запрос получает `trace_id` — либо из заголовка `x-trace-id`, либо сгенерированный. Передаётся во все обработчики и логируется.

### Запуск сервера

```python
def run_asgi_server(*, host: str | None = None, port: int | None = None) -> None:
    resolved_host = host or os.getenv("HOST", "127.0.0.1")
    resolved_port = port if port is not None else _parse_port(os.getenv("PORT"))
    uvicorn.run("core.api.asgi_app:app", host=resolved_host, port=resolved_port)

if __name__ == "__main__":
    run_asgi_server()
```

Порт из env `PORT`, хост из env `HOST` (default `127.0.0.1`). Для Railway — `0.0.0.0`.

## Полный список роутов

| Method | Path | Auth | Handler |
|--------|------|------|---------|
| GET | `/health` | public | `handle_health` |
| GET | `/ready` | public | `handle_readiness` |
| GET | `/protected/status` | Bearer | `handle_protected_status` |
| GET | `/metrics` | Bearer | `handle_metrics` |
| GET | `/demo/auth-page` | public | `FileResponse` |
| GET | `/demo/auth-page/` | public | `FileResponse` |
| GET | `/demo/auth-page/styles.css` | public | `FileResponse` |
| OPTIONS | `/node/issues` | public | `Response(200)` |
| OPTIONS | `/node/issues/{issue_id}` | public | `Response(200)` |
| OPTIONS | `/node/network-pulse` | public | `Response(200)` |
| OPTIONS | `/node/emerging-signals` | public | `Response(200)` |
| GET | `/node/issues` | public | `handle_issues_list` |
| GET | `/node/issues/{issue_id}` | public | `handle_issue_get` |
| POST | `/node/issues` | Bearer | `handle_issue_create` |
| GET | `/node/network-pulse` | public | `handle_network_pulse` |
| GET | `/node/emerging-signals` | public | `handle_emerging_signals` |
| POST | `/intake/stories` | public | `handle_story_intake` |

---

## Шаги репликации в новом проекте

### 1. Создать файловую структуру

```
src/
└── core/
    └── api/
        ├── asgi_app.py      ← HTTP transport
        ├── dependencies.py  ← DI container
        ├── handlers.py      ← бизнес-логика обработки
        ├── envelope.py      ← сборка response envelope
        ├── security.py      ← auth
        └── idempotency.py   ← idempotency key
```

### 2. Создать `asgi_app.py` по шаблону

```python
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

@asynccontextmanager
async def _lifespan(_: FastAPI):
    deps = get_api_dependencies()          # инициализировать DI singleton при старте
    configure_logging(deps.config.log_level, log_format=deps.config.log_format)
    # запустить cron jobs если нужно
    try:
        yield
    finally:
        # остановить cron jobs
        pass

app = FastAPI(title="my-service", version="0.1.0", lifespan=_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-trace-id", "authorization"],
)

@app.middleware("http")
async def diagnostics(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # log exc with trace_id
        raise

@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request, exc):
    return JSONResponse({"error": {"code": "UNAUTHORIZED"}}, status_code=401)
```

### 3. Добавить routers / endpoints

Следуй паттерну: каждый endpoint = парсинг params → `handle_*(deps, ...)` → `JSONResponse`.

### 4. Запуск

```bash
python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

Для локального dev:
```bash
python -m uvicorn --app-dir src core.api.asgi_app:app --host 127.0.0.1 --port 8000 --reload --reload-dir src
```

### Pitfalls

- `host=127.0.0.1` не доступен снаружи контейнера — для Railway/Docker используй `0.0.0.0`
- `lifespan` инициализирует DI singleton — без него первый запрос будет медленнее и логи startup не появятся
- Не добавляй бизнес-логику в `asgi_app.py` — только routing, exception handlers, middleware
- `OPTIONS` роуты нужно добавлять явно — FastAPI не делает это автоматически
