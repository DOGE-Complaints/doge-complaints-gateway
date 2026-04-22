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
- `GET /protected/status`
- `GET /metrics`
- demo auth page: `/demo/auth-page`

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

### 4.5 Базовая проверка boundary/config/auth

```bash
python3 -m pytest tests/test_bootstrap_smoke.py tests/test_api_security_and_ops.py tests/test_http_transport_smoke.py tests/test_config_loading.py -q
```

### 4.6 Расширенная проверка envelope/trace

```bash
python3 -m pytest tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q
```

## 5) Частые проблемы

1. `Missing required environment variable: API_BASE_URL`
   - выставить `API_BASE_URL`.
2. `SERVICE_API_TOKEN is required for APP_PROFILE='pilot' strict auth mode`
   - выставить `SERVICE_API_TOKEN` или вернуться к `APP_PROFILE=demo`.
3. Импорт `core.*` не резолвится
   - запускать команды из корня `doge-complaints-gateway`;
   - убедиться, что установлено `pip install -e .[dev]`.
