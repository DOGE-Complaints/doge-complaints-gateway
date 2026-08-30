# Quickstart: запуск runtime и переменные окружения

## Для кого

Короткий мануал для локального запуска `doge-complaints-gateway` по практическому, типичному для Python-проектов сценарию:

1. подготовить окружение,
2. выставить env-переменные,
3. проверить runtime boundary.

## Запуск локального сервера (as-is)

В проекте используется ASGI entrypoint на `FastAPI` + единый `uvicorn` подход:

- `src/core/api/asgi_app.py`
- запуск: `python -m uvicorn --app-dir src core.api.asgi_app:app`

Он обслуживает:

- `GET /health`
- `GET /ready`
- `GET /protected/status` (auth required)
- `GET /metrics` (auth required)
- `GET /demo/auth-page` (static)
- `POST /intake/stories` (story intake, public)

## 1) Prerequisites

- Python `3.11+` (см. `pyproject.toml`)
- `pip`
- `venv`

## 2) Установка зависимостей (типичный flow)

Из корня проекта `doge-complaints-gateway`:

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

## 3) Переменные окружения

Переменные читаются строго из `os.environ` процесса — приложение **не загружает `.env` само**.
Используйте `make serve` / `make dev` или `source .env` перед ручным `python -m uvicorn ...`.

Минимально необходимые и поддерживаемые в текущем runtime:

- `APP_PROFILE` (`demo` или `pilot`, default `demo`)
- `API_BASE_URL` (required)
- `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` (оба required — см. секцию ниже)
- `REQUEST_TIMEOUT_S` (default `15`)
- `LOG_LEVEL` (default `INFO`)
- `SERVICE_API_TOKEN` (для strict auth режима; обязателен при `APP_PROFILE=pilot`)

### Node active schema (GW-SSR-16)

Рабочая модель ноды — **одна** пара required env (без default, fail-fast). Несколько каталогов в `schema-packs/` — склад для отладки; процесс поднимает только эту пару. Не invent `DEFAULT_SCHEMA_PACK` и не «первый pack».

| Переменная | Назначение | Если не задана / пустая / нет каталога |
|---|---|---|
| `NODE_SCHEMA_ID` | id каталога `schema-packs/<id>/` | `ConfigError`, процесс не стартует |
| `NODE_SCHEMA_VERSION` | версия `schema-packs/<id>/<version>/` | `ConfigError`, процесс не стартует |

Пример на диске: `NODE_SCHEMA_ID=tallinn_civic` и `NODE_SCHEMA_VERSION=v1`.

`SCHEMA_PACKS_ROOT` остаётся optional override корня склада: читает [`resolver.py`](../../../src/core/schema/resolver.py) через `os.environ`, **не** поле `AppConfig`.

**Авторизация legacy public-content writes (GW-DRAFT-04) — для `POST /intake/stories` и `POST /node/issues`:**

Мутации публичного контента на legacy-маршрутах требуют **только** сервисный токен канала (`SERVICE_API_TOKEN`). Пользовательский слой OAuth-introspection снят (GW-DRAFT-04); маршруты — **trusted service channel** для seed/simulation/операторских скриптов, не для браузерного submit.

| Переменная | Назначение | Если не задана |
|---|---|---|
| `SERVICE_API_TOKEN` | Сервисный токен для `require_public_content_service_auth` | **401** на write при strict auth; в `pilot` обязателен при старте |

> **Продуктовый user submit:** браузер `POST /story-drafts/{id}/submit` (Bearer → identity `/me` + `phone_verified` gate) — см. [`security-env-api-access.md`](../security-env-api-access.md) §4.1 и [`server-env-quickstart.md`](./server-env-quickstart.md) ниже (browser env).
> Источники: EnvSpec [`schema.py`](../../../src/core/config/schema.py); deps — [`asgi_app.py:require_public_content_service_auth`](../../../src/core/api/asgi_app.py).

**Browser story-draft auth (GW-DRAFT-02) — для `GET/POST /story-drafts*`:**

| Переменная | Назначение | Если не задана |
|---|---|---|
| `IDENTITY_BASE_URL` | База identity для `GET {base}/me` (browser session) | `/me` не сконфигурирован → story-draft routes **503** (fail-closed) |
| `SPA_VERIFY_BASE_URL` | База для `verify_url` в ответе **403** `verification_required` (default `http://localhost:3000`) | в 403-теле уйдёт дефолтный verify-URL |

> Коды browser submit: **401** — нет/битый Bearer; **403** `verification_required` (+`verify_url`) — `phone_verified=false`; **503** — identity недоступен. Подробнее — [`seed-demo-data-runbook-ru.md`](./seed-demo-data-runbook-ru.md).

**Persistence backend (DB_BACKEND):**

| Значение | Поведение | Требует |
|---|---|---|
| `in_memory` (default) | Всё в RAM; данные не переживают рестарт | — (SUPABASE_* должны быть **не заданы**) |
| `sqlite` | Локальный SQLite-файл | `DATABASE_URL=sqlite:///path/to/db` |
| `supabase` | Hosted Supabase через PostgREST | `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE` |

> ⚠️ `in_memory` + `SUPABASE_URL` в env → `ConfigError` при старте. Либо убирайте Supabase-переменные, либо ставьте `DB_BACKEND=supabase`.

### Production logging — рекомендации

| Переменная | Production значение | Почему |
|-----------|--------------------|--------|
| `LOG_LEVEL` | `INFO` | При `DEBUG` `httpx`/`httpcore` генерируют шум на каждый Supabase запрос |
| `LOG_FORMAT` | `json` | Structured logs для Railway / Datadog / Loki / любого log-агрегатора |
| `LOG_DEBUG_DIR` | *(не задавать)* | Только для краткосрочной диагностики |

`LOG_FORMAT=json` переводит каждую строку в структурированный JSON-лог:

```json
{"ts":"2026-05-25T10:01:23","level":"INFO","logger":"core.api","msg":"story_intake_created","trace_id":"abc","story_id":"def"}
```

`LOG_DEBUG_DIR` на Railway пишет файлы в ephemeral filesystem контейнера, поэтому они исчезают после redeploy/restart. Используйте это как временную диагностику, а не постоянное хранилище.

**Cluster knobs (не env):** семантические `CLUSTER_ACTIVE_LENSES` / `CLUSTER_PRIMARY_LENS` / `CLUSTER_MIN_SIZE` **не** кастомизируют ноду. Пороги, линзы и geo — в активном pack `node_clustering.civic`; смена = правка `pack.json` + рестарт. См. [мануал ноды](./schema-packs-node-data-model-ru.md) §два контура. В env остаются только `CLUSTER_CRON_*` (процесс) + `NODE_SCHEMA_*`.

Источник civic knobs: активный `pack.json`. Cron/env: `src/core/config/schema.py`.

### Пример для demo (in_memory, только локально)

```bash
export APP_PROFILE=demo
export API_BASE_URL=https://demo.local
export LOG_LEVEL=INFO
export SERVICE_API_TOKEN=demo-secret-token
# DB_BACKEND не задан → in_memory (данные только в RAM)
```

### Пример для demo с Supabase

```bash
export APP_PROFILE=demo
export API_BASE_URL=https://demo.local
export DB_BACKEND=supabase
export SUPABASE_URL=https://<ref>.supabase.co
export SUPABASE_SERVICE_ROLE=<service-role-key>
# Civic lenses/min_size — в pack node_clustering.civic, не CLUSTER_ACTIVE_LENSES.
# или просто: source .env && make serve
```

### Пример для pilot

```bash
export APP_PROFILE=pilot
export API_BASE_URL=https://pilot.local
export SERVICE_API_TOKEN=pilot-secret-token
```

`APP_PROFILE=pilot` без `SERVICE_API_TOKEN` приведет к fail-fast в конфиге.

## 4) Runtime smoke с реальным HTTP transport

### 4.1 Установка dev-зависимостей (исправляет `No module named pytest`)

Если получаете ошибку `No module named pytest` или `No module named uvicorn`, установите зависимости в активное venv:

```bash
python -m pip install -e '.[dev]'
```

### 4.2 Запуск сервера

**Рекомендуемый способ** — через `make`, который автоматически загружает `.env`:

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway

make serve      # production-like локальный запуск (без reload)
make dev        # горячий reload при изменении кода в src/
make check-env  # показывает какой DB_BACKEND и Supabase URL увидит сервер
```

> Без `make serve` / `make dev` переменные из `.env` **не попадают** в процесс uvicorn.
> Сервер молча стартует с `DB_BACKEND=in_memory` и все данные живут только в RAM.

**Если нужен голый `uvicorn` без make** — сначала загрузите `.env`:

```bash
set -a && . ./.env && set +a
.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
  --host 127.0.0.1 --port ${PORT:-8000}
```

Проверка что сервер использует правильный backend — ищите в стартовом логе:
```
startup.config db_backend=supabase ...
startup.persistence_backend backend=supabase db_ready=True
```
Если там `db_backend=in_memory` — `.env` не загружен.

### 4.3 Как задается порт запуска

Порт задается переменной окружения `PORT` в `.env` или в шелле:

```bash
PORT=8010 make serve
# или
export PORT=8010 && make serve
```

Если `PORT` не задан, используется `8000`.

### 4.4 Локальные URL

- Health check URL: `http://127.0.0.1:${PORT:-8000}/health`
- Readiness URL: `http://127.0.0.1:${PORT:-8000}/ready`
- Protected status URL: `http://127.0.0.1:${PORT:-8000}/protected/status`
- Metrics URL: `http://127.0.0.1:${PORT:-8000}/metrics`
- Mock auth page URL: `http://127.0.0.1:${PORT:-8000}/demo/auth-page`
- Story intake URL: `http://127.0.0.1:${PORT:-8000}/intake/stories` (POST)

### 4.5 Базовая проверка boundary/config/auth

```bash
python3 -m pytest tests/test_bootstrap_smoke.py tests/test_api_security_and_ops.py tests/test_http_transport_smoke.py tests/test_config_loading.py tests/test_http_intake_endpoint.py tests/test_e2e_story_cluster_issue_pipeline.py -q
```

### 4.6 Расширенная проверка envelope/trace

```bash
python3 -m pytest tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q
```

### 4.7 Railway (Railpack): ошибка «No start command detected»

**Симптом (лог Railpack):** `No start command detected` — план сборки не доходит до деплоя.

**Проверяемые гипотезы (по убыванию вероятности):**

1. **Нет явного start command** — приложение лежит в `src/core/api/asgi_app.py` (`app`), а не в корневых `app.py` / `main.py`, которые Railpack ищет по умолчанию.
2. **Неверный bind после запуска** — в контейнере нужен **`0.0.0.0`**, иначе health снаружи не достижим даже при успешном старте.

**Что сделать:**

- **В репозитории (рекомендуется):** в корне проекта есть [`railpack.json`](../../railpack.json) с полем `deploy.startCommand` (см. [Railpack: configuration file](https://railpack.com/config/file)).
- Для стабильного dependency install в Railpack добавить/держать в корне проекта `requirements.txt` (дублирует runtime deps из `pyproject.toml`).
- **В UI Railway (Settings):** задайте **Custom Start Command** (аналогично):

```bash
python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

- **Переменные в Railway (Variables):** как минимум `API_BASE_URL`, при необходимости `APP_PROFILE`, `SERVICE_API_TOKEN`, `REQUEST_TIMEOUT_S` (см. раздел 3 выше). Порт **`PORT`** Railway задаёт сам — не подменяйте вручную, если только не отлаживаете локально.

Для консистентности runtime и Railway используйте тот же `uvicorn --app-dir src` формат и локально.

### 4.8 Railway: ошибка «uvicorn: command not found» и 502 на `/health`

**Симптомы:**

- в Deploy Logs повторяется `/bin/bash: line 1: uvicorn: command not found`;
- endpoint `/health` отвечает `502` (контейнер не удерживает процесс приложения).

**Гипотезы (приоритизировано):**

1. **🔴 H1 / P0:** в runtime PATH нет бинарника `uvicorn` (console script), хотя Python окружение может быть валидным.
2. **🟡 H2 / P1:** сервис стартует не из корня `doge-complaints-gateway`, поэтому Python не видит пакет `core` из `src`.
3. **🟢 H3 / P1:** `uvicorn` действительно не установлен как зависимость в build image.

**Проверка и действие (применено в `railpack.json`):**

- используем модульный запуск через интерпретатор и явно задаём source-root:

```bash
python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

Install-step в `railpack.json` не задаем вручную: Python provider Railpack сам обрабатывает `pyproject.toml` и устанавливает зависимости автоматически.

И зафиксирована версия Python `3.11`, чтобы не зависеть от изменений дефолта Railpack:

```json
"packages": { "python": "3.11" }
```

Это устраняет зависимость от наличия CLI-бинарника `uvicorn` в PATH и фиксирует импорт `core.*` из `src`.

**Если после этого останется ошибка:**

- `No module named uvicorn` → подтверждается H3 (проверить, что build использует root с `pyproject.toml`, а install не переопределен кастомным `steps`);
- `No module named core` → подтверждается H2 (проверить Root Directory сервиса в Railway, должен указывать на `doge-complaints-gateway`).

### 4.9 Живой pytest smoke (`tests/smoke`) — канон `/node/*`

Против **уже запущенного** `make serve` (не in-process TestClient). Цель только localhost: `GATEWAY_URL=http://127.0.0.1:8000` в `.env.test`.

Покрывает `GET /health`, `GET /ready`, список и карточку `GET /node/issues`, Pulse, Emerging, 404 на старый `GET /tallinn/issues`.

Команды и таблица кейсов: [test-matrix — Local real-HTTP smoke](../testing/test-matrix-by-type-layer-mocks.md).

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
make serve
# другой терминал:
.venv/bin/python -m pytest tests/smoke/test_local_server_smoke.py -q
```

### 4.10 Curl-скрипт `scripts/smoke_real_urls.sh`

POSIX-скрипт **отдельный** от pytest `tests/smoke`. Он проверяет:

- `GET /health` (ожидается HTTP 200)
- `POST /intake/stories` с валидным payload (ожидается HTTP 200)

Параметризация URL:

- сначала используется `SMOKE_BASE_URL`;
- если не задан, берется `API_BASE_URL`.

Опционально:

- если задан `SERVICE_API_TOKEN`, скрипт добавляет `Authorization: Bearer ...`.

Команды:

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
sh -n scripts/smoke_real_urls.sh
SMOKE_BASE_URL="https://dogestonia-tallinn-demo.up.railway.app" sh scripts/smoke_real_urls.sh
```

## 5) Частые проблемы

1. `Missing required environment variable: API_BASE_URL`
   - выставить `API_BASE_URL`, или использовать `make serve` (подгружает из `.env`).
2. `SERVICE_API_TOKEN is required for APP_PROFILE='pilot' strict auth mode`
   - выставить `SERVICE_API_TOKEN` или вернуться к `APP_PROFILE=demo`.
3. `zsh: no matches found: .[dev]`
   - в `zsh` ставить зависимости только в кавычках: `python -m pip install -e '.[dev]'`.
4. Импорт `core.*` не резолвится
   - запускать команды из корня `doge-complaints-gateway`;
   - использовать `python -m uvicorn --app-dir src core.api.asgi_app:app ...`.
5. Railway build не ставит `uvicorn` (`No module named uvicorn`)
   - убедиться, что в корне есть `requirements.txt` с `fastapi`, `uvicorn`, `psycopg[binary]`;
   - проверить, что Railway Root Directory указывает на `doge-complaints-gateway`.
6. **Сервер стартует, но данные не попадают в Supabase (истории только в памяти)**
   - стартовый лог показывает `db_backend=in_memory` → `.env` не загружен в процесс uvicorn.
   - Используйте `make serve` вместо голого `python -m uvicorn ...`.
   - Проверьте: `make check-env` должен показывать `DB_BACKEND = supabase`.
7. Loader/`ConfigError` на `node_clustering.civic` (missing block / `primary_lens` ∉ `active_lenses`)
   - Исторический env `CLUSTER_PRIMARY_LENS` / `CLUSTER_ACTIVE_LENSES` больше не читается.
   - Править активный `pack.json` → `node_clustering.civic`, затем рестарт. См. [мануал ноды](./schema-packs-node-data-model-ru.md).
8. `ConfigError: DB_BACKEND='in_memory' does not allow SUPABASE_URL`
   - В env одновременно заданы Supabase-кредс и отсутствует `DB_BACKEND=supabase`.
   - Добавьте `DB_BACKEND=supabase` в `.env`.

## 6) DB backend env quick reference

- `DB_BACKEND=in_memory` (default)
  - не допускает `DATABASE_URL` и `SUPABASE_*` — иначе `ConfigError`.
  - Данные живут только в RAM процесса; `200 OK` возвращается, но в БД ничего нет.
- `DB_BACKEND=sqlite`
  - требует `DATABASE_URL=sqlite:///...`.
- `DB_BACKEND=supabase`
  - требует `SUPABASE_URL` и `SUPABASE_SERVICE_ROLE`;
  - не требует `DATABASE_URL` (runtime работает через Supabase HTTP/PostgREST client).
  - Стартовый лог при успехе: `startup.persistence_backend backend=supabase db_ready=True`.

**Важно: `DB_BACKEND` читается строго из `os.environ` процесса.** Файл `.env` не загружается автоматически — всегда используйте `make serve` / `make dev` для локального запуска.
