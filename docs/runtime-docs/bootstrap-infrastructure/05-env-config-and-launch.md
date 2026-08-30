# 05. Env, Config и Launch

## Концепция

Конфигурация — это pure function от env mapping. `AppConfig` — immutable dataclass. Нет магии: нет `python-dotenv`, нет Pydantic Settings, нет settings-синглтонов. Приложение получает config один раз при старте через `provide_app_config()`.

`.env` файл — это удобство для оператора, не для кода. Приложение не загружает `.env` само по себе — это делает `make serve`/`make dev`. Это сознательное решение: чёткое разграничение что загружает `.env` (shell) и что читает env (приложение).

## Реализация в проекте

### `AppConfig` — immutable dataclass (`config/schema.py`)

```python
@dataclass(frozen=True)
class AppConfig:
    profile: DeploymentProfile         # demo | pilot
    api_base_url: str                  # required
    request_timeout_s: int             # default 15
    flags: FeatureFlags                # FF_WALLET_ADAPTER etc.
    log_level: str                     # INFO, DEBUG, WARNING, ERROR, CRITICAL
    log_debug_dir: str | None          # директория для per-story debug logs
    log_format: str                    # text | json
    db_backend: str                    # in_memory | sqlite | supabase
    db_enabled: bool                   # True если db_backend != in_memory
    database_url: str | None           # для sqlite: sqlite:///path/to/db
    supabase_url: str | None
    supabase_service_role: str | None
    cluster_min_size: int              # default 5
    cluster_readiness_threshold: int   # default 60
    cluster_active_lenses: tuple[str, ...]
    cluster_primary_lens: str
    # ... ещё 8 cluster-специфичных полей
```

`frozen=True` — config нельзя изменить после создания. Всегда immutable.

`SCHEMA_PACKS_ROOT` **не** поле `AppConfig` — см. таблицу env ниже (читает [`resolver.py`](../../../src/core/schema/resolver.py)).

### `load_config_from_env()` — pure function

```python
def load_config_from_env(env: Mapping[str, str] | None = None) -> AppConfig:
    source = env or environ
    profile = _parse_profile(_get_value(source, "APP_PROFILE"))
    # ... валидация и парсинг каждого поля
    return AppConfig(...)
```

Принимает `Mapping[str, str]` — можно передать любой dict, `os.environ`, или специально подготовленный mapping для тестов. Без глобального состояния.

Fail-fast: при любой невалидной переменной бросает `ConfigError` — сервер не стартует с неверной конфигурацией.

### `merge_dotenv_from_cwd()` — кастомный dotenv без library

```python
def merge_dotenv_from_cwd(target: MutableMapping[str, str], *, priority: Mapping[str, str]) -> None:
    merge_dotenv_from_path(Path.cwd() / ".env", target, priority=priority)

def merge_dotenv_from_path(path: Path, target, *, priority) -> None:
    if not path.is_file():
        return
    fixed = frozenset(priority.keys())      # ← shell env vars заморожены
    for line in path.read_text().splitlines():
        key, value = line.split("=", 1)
        if key not in fixed:               # ← не перезаписывает shell vars
            target[key] = value.strip('"').strip("'")
```

**Приоритет**: `os.environ` (shell exports) > `.env` файл.  
Если переменная уже есть в shell — `.env` её не перезапишет.

### `provide_app_config()` — объединение источников

```python
def provide_app_config(env: Mapping[str, str] | None = None) -> AppConfig:
    if env is None:
        priority = dict(environ)          # snapshot os.environ
        source = dict(priority)
        merge_dotenv_from_cwd(source, priority=priority)   # заполняет из .env
    else:
        source = dict(env)                # для тестов: брать из переданного dict
    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "https://demo.local")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    return load_config_from_env(source)
```

Когда `env=None` (production) — читает `os.environ` + `.env` из CWD.  
Когда `env=dict(...)` (тесты) — работает только с переданным mapping (не трогает process env).

---

## Полная таблица переменных окружения

| Переменная | Default | Required | Описание |
|-----------|---------|----------|----------|
| `APP_PROFILE` | `demo` | no | `demo` (FF off) или `pilot` (FF on + auth required) |
| `API_BASE_URL` | — | **yes** | Base URL API (включая схему: https://...) |
| `REQUEST_TIMEOUT_S` | `15` | no | Таймаут исходящих запросов в секундах |
| `LOG_LEVEL` | `INFO` | no | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT` | `text` | no | `text` или `json` |
| `LOG_DEBUG_DIR` | — | no | Директория для per-story debug log файлов |
| `SERVICE_API_TOKEN` | — | если `pilot` | Bearer token для защищённых эндпоинтов |
| `DB_BACKEND` | `in_memory` | no | `in_memory`, `sqlite`, `supabase` |
| `DATABASE_URL` | — | если `sqlite` | `sqlite:///path/to/db.sqlite` |
| `SUPABASE_URL` | — | если `supabase` | `https://<ref>.supabase.co` |
| `SUPABASE_SERVICE_ROLE` | — | если `supabase` | service_role key |
| `FF_WALLET_ADAPTER` | profile default | no | Переопределение feature flag |
| `FF_BLOCKCHAIN_ADAPTER` | profile default | no | Переопределение feature flag |
| `FF_TOKENIZATION_PIPELINE` | profile default | no | Переопределение feature flag |
| ~~`CLUSTER_MIN_SIZE`~~ / ~~`CLUSTER_READINESS_THRESHOLD`~~ / ~~`CLUSTER_ACTIVE_LENSES`~~ / ~~`CLUSTER_PRIMARY_LENS`~~ / ~~`CLUSTER_SIGNAL_SOURCE`~~ / ~~`CLUSTER_ID_ALGORITHM`~~ / ~~`CLUSTER_GEO_FILTER`~~ / ~~`CLUSTER_GEO_SCOPE`~~ / ~~`CLUSTER_TIE_BREAKER`~~ / ~~`CLUSTER_TYPE_RESOLUTION`~~ | — | — | **Не текущий SSOT.** Перенесено в активный pack `node_clustering.civic` (SSR-20). Задаются в env — игнорируются OS. Как сменить пороги/линзы/geo: [мануал ноды](../manuals/schema-packs-node-data-model-ru.md) §два контура. |
| `CLUSTER_CRON_INTERVAL_S` | `60` | no | Интервал фонового cron в секундах (процесс; **не** в pack) |
| `CLUSTER_CRON_ENABLED` | `true` | no | `true`/`false`/`1`/`0`/`yes`/`no` |
| `SCHEMA_PACKS_ROOT` | `<gateway-root>/schema-packs/` | no | Корень каталогов `schema-packs/<schema_id>/<schema_version>/`. Читается **только** в [`resolver.py`](../../../src/core/schema/resolver.py) (`os.environ`); поля в `AppConfig` **нет** (не fail-fast в `load_config_from_env`). Пустое/absent → default рядом с исходниками gateway. |
| `PORT` | `8000` | no | Порт uvicorn (читается в `asgi_app.py`, не в AppConfig) |
| `HOST` | `127.0.0.1` | no | Хост uvicorn (для Railway: `0.0.0.0`) |

### Правила совместимости backend

| `DB_BACKEND` | Требует | Запрещает |
|-------------|---------|----------|
| `in_memory` | — | `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE` |
| `sqlite` | `DATABASE_URL=sqlite:///...` | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE` |
| `supabase` | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE` | `DATABASE_URL` |

Нарушение правил → `ConfigError` при старте (fail-fast).

---

## Makefile

**Файл:** `Makefile` (в корне проекта)

```makefile
serve:
    set -a && . ./.env && set +a && \
    .venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
      --host 127.0.0.1 --port $${PORT:-8000}

dev:
    set -a && . ./.env && set +a && \
    .venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
      --host 127.0.0.1 --port $${PORT:-8000} --reload --reload-dir src

simulate:
    .venv/bin/python tests/simulation_runner.py

check-env:
    @set -a && . ./.env && set +a && \
    echo "DB_BACKEND     = $${DB_BACKEND:-<not set>}" && \
    echo "SUPABASE_URL   = $${SUPABASE_URL:-<not set>}"
```

`set -a && . ./.env && set +a` — загружает все переменные из `.env` в текущий shell процесс перед запуском uvicorn. Без этого uvicorn не видит `.env`.

### Команды

```bash
make serve      # production-like: загружает .env, запускает без reload
make dev        # development: загружает .env, --reload при изменениях в src/
make check-env  # диагностика: покажет DB_BACKEND и SUPABASE_URL
make simulate   # запуск simulation_runner.py против GATEWAY_URL из .env.test
```

---

## Запуск Uvicorn

### Через make (рекомендовано)

```bash
cd doge-complaints-gateway
make serve
```

### Вручную (нужно загрузить .env самостоятельно)

```bash
set -a && . ./.env && set +a
.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
  --host 127.0.0.1 --port ${PORT:-8000}
```

### Production / Railway

```bash
python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

`--host 0.0.0.0` обязателен для доступности снаружи контейнера.

### Проверить что backend подключён правильно

В стартовых логах:
```
startup.config db_backend=supabase ...
startup.persistence_backend backend=supabase db_ready=True checks=connectivity:ok,schema:ok,...
```

Если `db_backend=in_memory` — `.env` не загружен в процесс.

---

## Деплой на Railway

**Файл:** `railpack.json` (в корне проекта)

```json
{
  "packages": { "python": "3.11" },
  "deploy": {
    "startCommand": "python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}"
  }
}
```

Railpack автоматически устанавливает зависимости из `pyproject.toml`.

**Переменные в Railway Variables:**
- `API_BASE_URL` — обязательно
- `APP_PROFILE` — `demo` или `pilot`
- `DB_BACKEND=supabase`
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`
- `SERVICE_API_TOKEN` — если `pilot`

`PORT` Railway задаёт автоматически — не переопределяй.

---

## Установка и первый запуск

```bash
# 1. Клонировать и перейти в проект
cd doge-complaints-gateway

# 2. Создать virtualenv
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Установить зависимости
python -m pip install -U pip
python -m pip install -e '.[dev]'

# 4. Создать .env (скопировать пример)
cp .env.test.example .env.test
# Заполнить .env (минимум для Supabase):
cat > .env <<EOF
APP_PROFILE=demo
API_BASE_URL=https://demo.local
DB_BACKEND=supabase
SUPABASE_URL=https://<ref>.supabase.co
SUPABASE_SERVICE_ROLE=<key>
EOF

# 5. Проверить конфигурацию
make check-env

# 6. Запустить
make serve
```

---

## `.env` template для Supabase (production-like)

```bash
# ─── Core ────────────────────────────────────
APP_PROFILE=demo
API_BASE_URL=https://your-service.up.railway.app
REQUEST_TIMEOUT_S=15

# ─── Auth ────────────────────────────────────
SERVICE_API_TOKEN=your-secret-token

# ─── Persistence ─────────────────────────────
DB_BACKEND=supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service_role_key>

# ─── Logging ─────────────────────────────────
LOG_LEVEL=INFO
LOG_FORMAT=text

# ─── Clustering (cron = процесс; семантика — pack) ──
# Не задавать CLUSTER_MIN_SIZE / CLUSTER_ACTIVE_LENSES / CLUSTER_GEO_SCOPE:
# перенесено в pack node_clustering.civic (см. мануал ноды).
CLUSTER_CRON_ENABLED=true
CLUSTER_CRON_INTERVAL_S=60
```

---

## Шаги репликации в новом проекте

### 1. Создать `config/schema.py`

```python
from dataclasses import dataclass
from os import environ
from typing import Mapping

class ConfigError(ValueError): pass

@dataclass(frozen=True)
class AppConfig:
    profile: str
    api_base_url: str
    db_backend: str
    # ... ваши поля

def load_config_from_env(env: Mapping[str, str] | None = None) -> AppConfig:
    source = env or environ
    return AppConfig(
        profile=source.get("APP_PROFILE", "demo"),
        api_base_url=_require(source, "API_BASE_URL"),
        db_backend=source.get("DB_BACKEND", "in_memory"),
    )
```

### 2. Создать `config/env_file.py`

Скопировать `merge_dotenv_from_cwd()` из проекта — 40 строк без зависимостей.

### 3. Создать `Makefile`

```makefile
serve:
    set -a && . ./.env && set +a && \
    .venv/bin/python -m uvicorn --app-dir src your_package.api.asgi_app:app \
      --host 127.0.0.1 --port $${PORT:-8000}

dev:
    set -a && . ./.env && set +a && \
    .venv/bin/python -m uvicorn --app-dir src your_package.api.asgi_app:app \
      --host 127.0.0.1 --port $${PORT:-8000} --reload --reload-dir src
```

### 4. Создать `pyproject.toml`

```toml
[project]
requires-python = ">=3.11"
dependencies = ["fastapi>=0.115.0", "uvicorn>=0.30.0", "httpx>=0.27.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "pytest-asyncio>=0.24.0", "httpx>=0.27.0"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src", "tests"]
asyncio_mode = "auto"
```

### Pitfalls

- `DB_BACKEND=in_memory` не позволяет задавать `SUPABASE_*` — fail-fast при старте. Убери Supabase-переменные или поставь `DB_BACKEND=supabase`
- `python -m uvicorn` без `--app-dir src` → `ModuleNotFoundError: core`. Всегда указывай `--app-dir src`
- `python3 -m pip install -e '.[dev]'` — в zsh нужны кавычки вокруг `.[dev]`
- Railway: PORT задаётся платформой — используй `${PORT:-8000}`, не хардкоди
- Civic `primary_lens` должен быть в `node_clustering.civic.active_lenses` активного pack — иначе loader/`ConfigError`. Исторические env `CLUSTER_PRIMARY_LENS` / `CLUSTER_ACTIVE_LENSES` больше не читаются.
