# Quickstart: запуск runtime и переменные окружения

## Для кого

Короткий мануал для локального запуска `doge-complaints-gateway` по практическому, типичному для Python-проектов сценарию:

1. подготовить окружение,
2. выставить env-переменные,
3. проверить runtime boundary.

## Запуск локального сервера (as-is)

В проекте используется ASGI entrypoint на `FastAPI` + `uvicorn`:

- `src/core/api/asgi_app.py`
- запуск: `python3 -m core.api.asgi_app`

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
python -m pip install -e .[dev]
```

## 3) Переменные окружения

Минимально необходимые и поддерживаемые в текущем runtime:

- `APP_PROFILE` (`demo` или `pilot`, default `demo`)
- `API_BASE_URL` (required)
- `REQUEST_TIMEOUT_S` (default `15`)
- `LOG_LEVEL` (default `INFO`)
- `FF_WALLET_ADAPTER` (optional override)
- `FF_BLOCKCHAIN_ADAPTER` (optional override)
- `FF_TOKENIZATION_PIPELINE` (optional override)
- `SERVICE_API_TOKEN` (для strict auth режима; обязателен при `APP_PROFILE=pilot`)

Источник: `src/core/config/schema.py`, `src/core/api/security.py`.

### Пример для demo

```bash
export APP_PROFILE=demo
export API_BASE_URL=https://demo.local
export REQUEST_TIMEOUT_S=15
export LOG_LEVEL=INFO
export SERVICE_API_TOKEN=demo-secret-token
```

### Пример для pilot

```bash
export APP_PROFILE=pilot
export API_BASE_URL=https://pilot.local
export REQUEST_TIMEOUT_S=15
export LOG_LEVEL=INFO
export SERVICE_API_TOKEN=pilot-secret-token
```

`APP_PROFILE=pilot` без `SERVICE_API_TOKEN` приведет к fail-fast в конфиге.

## 4) Runtime smoke с реальным HTTP transport

### 4.1 Установка dev-зависимостей (исправляет `No module named pytest`)

Если получаете ошибку `No module named pytest`, установите dev extras в активное venv:

```bash
python -m pip install -e .[dev]
```

### 4.2 Запуск сервера

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
source .venv/bin/activate
python3 -m core.api.asgi_app
```

Альтернатива через `uvicorn` напрямую:

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
source .venv/bin/activate
uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000
```

### 4.3 Как задается порт запуска

Порт задается переменной окружения `PORT`:

```bash
export PORT=8010
python3 -m core.api.asgi_app
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
2. **Неверный bind после запуска** — `python3 -m core.api.asgi_app` по умолчанию берёт `HOST=127.0.0.1` из кода; в контейнере нужен **`0.0.0.0`**, иначе health снаружи не достижим даже при успешном старте.

**Что сделать:**

- **В репозитории (рекомендуется):** в корне проекта есть [`railpack.json`](../../railpack.json) с полем `deploy.startCommand` (см. [Railpack: configuration file](https://railpack.com/config/file)).
- **В UI Railway (Settings):** задайте **Custom Start Command** (аналогично):

```bash
PYTHONPATH=src python -m uvicorn core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

- **Переменные в Railway (Variables):** как минимум `API_BASE_URL`, при необходимости `APP_PROFILE`, `SERVICE_API_TOKEN`, `REQUEST_TIMEOUT_S` (см. раздел 3 выше). Порт **`PORT`** Railway задаёт сам — не подменяйте вручную, если только не отлаживаете локально.

**Альтернатива без `uvicorn` в команде:** выставить `HOST=0.0.0.0` и оставить `PYTHONPATH=src python3 -m core.api.asgi_app` — тогда слушает адрес из `HOST` (см. `run_asgi_server` в `src/core/api/asgi_app.py`).

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
PYTHONPATH=src python -m uvicorn core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}
```

Это устраняет зависимость от наличия CLI-бинарника `uvicorn` в PATH и одновременно фиксирует импорт `core.*` из `src`.

**Если после этого останется ошибка:**

- `No module named uvicorn` → подтверждается H3 (проверить install-step/зависимости в build logs);
- `No module named core` → подтверждается H2 (проверить Root Directory сервиса в Railway, должен указывать на `doge-complaints-gateway`).

## 5) Частые проблемы

1. `Missing required environment variable: API_BASE_URL`
   - выставить `API_BASE_URL`.
2. `SERVICE_API_TOKEN is required for APP_PROFILE='pilot' strict auth mode`
   - выставить `SERVICE_API_TOKEN` или вернуться к `APP_PROFILE=demo`.
3. Импорт `core.*` не резолвится
   - запускать команды из корня `doge-complaints-gateway`;
   - убедиться, что установлено `pip install -e .[dev]`.
