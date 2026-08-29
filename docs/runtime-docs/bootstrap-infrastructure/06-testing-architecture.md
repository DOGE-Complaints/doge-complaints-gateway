# 06. Testing Architecture

## Концепция

Тест-сюита разделена на слои с чёткой изоляцией. Главное правило: **unit и integration тесты не трогают реальный Supabase**. Это гарантируется autouse фикстурой `_block_dotenv_leakage`, которая при каждом тесте подменяет `DB_BACKEND=in_memory` и очищает Supabase credentials.

Тесты против реального Supabase помечаются маркером `live_integration` и запускаются отдельно — только на `main` ветке или вручную в CI.

## Конфигурация pytest (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
pythonpath = ["src", "tests"]           # ← импорты core.* и helper модулей из tests/
testpaths = ["tests"]
asyncio_mode = "auto"                   # ← все async тесты авто-запускаются без @pytest.mark.asyncio
asyncio_default_fixture_loop_scope = "function"
markers = [
  "live_integration: tests requiring SUPABASE_TEST_URL and live Supabase project",
]
```

`pythonpath = ["src", "tests"]` — критично: позволяет `import core.*` в тестах без установки пакета в режиме editable.

---

## `tests/conftest.py` — три обязательные фикстуры

### 1. `_block_dotenv_leakage` — изоляция от .env

```python
@pytest.fixture(autouse=True)
def _block_dotenv_leakage(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent .env vars from leaking into tests (DB_BACKEND=supabase would hit real DB)."""
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "60")
    monkeypatch.setenv("CLUSTER_ACTIVE_LENSES", "civic_domain_micro,failure_pattern_micro,...")
    monkeypatch.setenv("CLUSTER_PRIMARY_LENS", "civic_domain_micro")
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "canonical")
    monkeypatch.setenv("CLUSTER_TIE_BREAKER", "alpha")
```

**Почему это необходимо**: `provide_app_config()` вызывает `merge_dotenv_from_cwd()`, которая читает `.env` из CWD. Если `.env` содержит `DB_BACKEND=supabase`, тест попадёт в реальную БД без этой фикстуры.

Фикстура — `autouse=True`, применяется к каждому тесту автоматически.

Тесты, которым нужен не-in_memory бэкенд, переопределяют через `monkeypatch.setenv()` в своих фикстурах (они применяются после autouse).

### 2. `_pytest_session_logging` — настройка логирования

```python
@pytest.fixture(scope="session", autouse=True)
def _pytest_session_logging() -> None:
    """Without ASGI lifespan, tests still get predictable log levels."""
    configure_logging(
        os.environ.get("LOG_LEVEL", "INFO"),
        log_format="text",
        log_debug_dir=None,
    )
```

В тестах lifespan не запускается → `configure_logging()` не вызывается из приложения. Эта фикстура делает то же самое на уровне pytest session.

### 3. `pytest_collection_modifyitems` — автотегирование live integration

```python
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Auto-tag tests/integration/supabase/ as live_integration."""
    marker = pytest.mark.live_integration
    for item in items:
        path = str(item.path).replace("\\", "/")
        if "/tests/integration/supabase/" in path:
            item.add_marker(marker)
```

Тесты в `tests/integration/supabase/` автоматически получают маркер — не нужно декорировать каждый тест вручную.

---

## Слои тестов

### Слой 1: Domain Unit Tests

```
tests/test_alpha_score.py
tests/test_clustering_engine.py
tests/test_geo_intelligence.py
tests/test_signal_vocabulary.py
tests/test_filter_projection_rows_contract.py
...
```

**Backend:** InMemory (через autouse `_block_dotenv_leakage`)  
**Что тестируют:** чистую бизнес-логику — scoring, clustering, geo, filters  
**Зависимости:** только `core.domain`, `core.cluster`, `core.projection` etc.

Паттерн:
```python
def test_alpha_score_with_canonical_type():
    record = StoryRecord(
        story_id="test-1",
        narrative_canonical_type="complaint",
        # ...
    )
    score = compute_alpha_score(record)
    assert score >= 12  # canonical_type bonus
```

### Слой 2: Service / Factory Tests

```
tests/test_di_service_factory.py
tests/test_story_intake_contract.py
tests/test_story_repository_lifecycle.py
tests/test_gpt_signals_intake.py
tests/test_institution_intake.py
...
```

**Backend:** InMemory  
**Что тестируют:** сервисы с реальными (InMemory) репозиториями  

Паттерн:
```python
def _factory() -> DefaultServiceFactory:
    return DefaultServiceFactory(
        story_repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=provide_geo_service(),
        config=provide_app_config(),
        ...
    )

def test_story_intake_creates_record():
    factory = _factory()
    service = factory.get_story_intake_service()
    result = service.create_story(request)
    assert result.story_id is not None
```

### Слой 3: HTTP Transport Tests

```
tests/test_http_intake_endpoint.py
tests/test_http_transport_smoke.py
tests/test_error_envelope_contract.py
tests/test_api_route_edges.py
tests/test_api_security_and_ops.py
tests/test_trace_propagation.py
...
```

**Backend:** InMemory + ASGI TestClient  
**Что тестируют:** HTTP слой: статус коды, envelope format, auth, CORS, idempotency

Паттерн с `httpx.AsyncClient`:
```python
import pytest
from httpx import AsyncClient, ASGITransport
from core.api.asgi_app import app, _clear_api_dependencies_cache

@pytest.fixture(autouse=True)
def _reset_deps():
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()

async def test_health_returns_200():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "ok"
```

`_clear_api_dependencies_cache()` важен: без него тест использует singleton из предыдущего теста с другими env vars.

### Слой 4: E2E Pipeline Tests (In-Memory)

```
tests/test_e2e_story_cluster_issue_pipeline.py
tests/test_e2e_intake_create_doge_issue_contract.py
tests/test_e2e_create_story_fullpath.py
tests/test_e2e_sandbox_full_pipeline.py
tests/test_db_backed_pipeline_e2e.py
...
```

**Backend:** InMemory  
**Что тестируют:** полный pipeline: intake → clustering → issue creation → GET /node/issues

Паттерн:
```python
async def test_full_pipeline_creates_issue():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Submit story
        resp = await client.post("/intake/stories", json=story_payload)
        assert resp.status_code == 202
        story_id = resp.json()["data"]["story_id"]

        # 2. Run clustering
        deps = get_api_dependencies()
        await deps.story_cluster_orchestrator.run()

        # 3. Check issue exists
        resp = await client.get("/node/issues?status=PUBLISHED")
        assert len(resp.json()["data"]) > 0
```

### Слой 5: Live Supabase Integration

```
tests/integration/supabase/
├── test_supabase_dotenv_connectivity.py     # базовая connectivity
├── test_supabase_live_smoke.py              # smoke против реального проекта
├── test_supabase_live_story_roundtrip.py    # write → read roundtrip
├── test_supabase_live_full_pipeline_roundtrip.py
├── test_rls_policy_validation.py
└── ...
```

**Backend:** реальный Supabase из `.env`  
**Marker:** `live_integration`  
**Skip если нет creds:** автоматически через `pytest.skip()`

Паттерн:
```python
def _require_supabase_creds_from_dotenv() -> tuple[str, str]:
    dotenv = _parse_dotenv_file(Path(__file__).parents[3] / ".env")
    url = dotenv.get("SUPABASE_URL", "")
    key = dotenv.get("SUPABASE_SERVICE_ROLE", "")
    if not url or not key:
        pytest.skip("No Supabase creds in .env")
    return url, key

def test_story_roundtrip():
    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    repo = SupabaseStoryRepository(db)
    # write → read → assert
```

### Слой 6: Smoke Tests (живой сервер)

```
tests/smoke/
├── conftest.py
├── test_local_server_smoke.py
├── test_local_server_async_read.py
└── test_gpt_pirita_demo_intake_smoke.py
```

**Backend:** реально запущенный сервер (localhost или Railway URL)  
**Когда:** после деплоя или вручную  
**Не входят в стандартный pytest run без специального conftest**

---

## CI Architecture

### `.github/workflows/test-offline.yml` — основной

```yaml
on: [push, pull_request]

jobs:
  pytest-offline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[dev]"
      - run: python -m pytest -q -m "not live_integration"
```

Запускается на каждый push и PR. Исключает `live_integration` тесты.

### `.github/workflows/integration-live.yml` — live Supabase

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:      # ← ручной запуск

jobs:
  pytest-live-integration:
    steps:
      - run: pip install -e ".[dev]"
      - env:
          SUPABASE_TEST_URL: ${{ secrets.SUPABASE_TEST_URL }}
          SUPABASE_TEST_SERVICE_ROLE: ${{ secrets.SUPABASE_TEST_SERVICE_ROLE_KEY }}
        run: python -m pytest -q -m live_integration
```

Запускается только при мерже в `main` или вручную. Требует GitHub Secrets.

**GitHub Secrets для live integration:**
- `SUPABASE_TEST_URL` — URL тестового Supabase проекта (отдельный от production!)
- `SUPABASE_TEST_SERVICE_ROLE_KEY` — service_role key тестового проекта

---

## Команды для локальной разработки

```bash
# Стандартный run (offline, ~15 секунд)
python3.11 -m pytest tests/ -q --tb=short

# Только offline (исключить live_integration)
python3.11 -m pytest -m "not live_integration" -q

# Только live Supabase (нужен .env с creds)
python3.11 -m pytest -m live_integration -v

# Конкретный файл
python3.11 -m pytest tests/test_story_intake_contract.py -v

# С debug логами
LOG_LEVEL=DEBUG python3.11 -m pytest tests/test_e2e_story_cluster_issue_pipeline.py -v -s

# Базовый smoke (быстрая проверка после изменений)
python3.11 -m pytest tests/test_bootstrap_smoke.py tests/test_http_transport_smoke.py -q
```

---

## Шаги репликации в новом проекте

### 1. Настроить `pyproject.toml`

```toml
[tool.pytest.ini_options]
pythonpath = ["src", "tests"]
testpaths = ["tests"]
asyncio_mode = "auto"
markers = ["live_integration: requires live backend"]
```

### 2. Создать `tests/conftest.py`

```python
import pytest
from core.logging_setup import configure_logging

def pytest_collection_modifyitems(items):
    for item in items:
        if "/tests/integration/" in str(item.path):
            item.add_marker(pytest.mark.live_integration)

@pytest.fixture(scope="session", autouse=True)
def _session_logging():
    configure_logging("INFO", log_format="text")

@pytest.fixture(autouse=True)
def _block_env_leakage(monkeypatch):
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    # добавь все переменные, которые могут прийти из .env
```

### 3. Создать два CI workflow

`test-offline.yml`: `pytest -m "not live_integration"` на каждый push  
`integration-live.yml`: `pytest -m live_integration` на main + secrets

### 4. Для HTTP тестов — сбрасывать DI singleton

```python
from core.api.asgi_app import app, _clear_api_dependencies_cache

@pytest.fixture(autouse=True)
def reset_deps():
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()
```

### Pitfalls

- Без `_block_dotenv_leakage` тесты могут случайно попасть в реальный Supabase — данные не те, скорость упадёт, тесты могут падать из-за сетевых ошибок
- `asyncio_mode = "auto"` — иначе каждый async тест нужно декорировать `@pytest.mark.asyncio`
- `_clear_api_dependencies_cache()` нужно вызывать ДО теста — singleton создаётся при первом вызове, нужен чистый env к этому моменту
- Live integration тесты должны использовать **отдельный** тестовый Supabase проект, не production
- `pytest.skip()` в `_require_supabase_creds_from_dotenv()` позволяет запускать live тесты в CI (с secrets) и пропускать локально (без .env) без fail
