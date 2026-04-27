# Security, Env, API Access

## Контекст и управленческий вопрос

Ключевой вопрос:  
**какова фактическая security posture текущего runtime, где проходит trust boundary, и как обеспечить предсказуемый режим доступа в production-like окружении?**

## Current state (implemented now)

### 1) Модель доступа к API

В коде реализован **service-to-service gate**, а не пользовательская аутентификация:

- Принимаются токены из:
  - `Authorization: Bearer <token>`
  - `X-Service-Token: <token>`
- Извлечение токена: `extract_service_token` (`src/core/api/security.py`).
- Проверка: `ServiceTokenAuth.require` (`src/core/api/security.py`).
- Transport policy enforcement: `require_service_auth` dependency (`src/core/api/asgi_app.py`).
- Handler-level guard (defense in depth): `handle_protected_status` и `handle_metrics` (`src/core/api/handlers.py`).

Практический смысл: gateway защищает вызовы между сервисами/интеграторами, но не реализует full user auth flow.

Protected/public operation split (as-is, route policy — источник: `asgi_app.py`):

- Protected routes (Bearer token или `X-Service-Token` обязательны):
  - `GET /protected/status`
  - `GET /metrics`
- Public routes (без авторизации):
  - `GET /health`
  - `GET /ready`
  - `GET /demo/auth-page`
  - `GET /demo/auth-page/`
  - `GET /demo/auth-page/styles.css`
  - `POST /intake/stories` ← бизнес-эндпоинт, без auth

**Примечание:** бизнес-эндпоинт intake (`/intake/stories`) намеренно публичен в текущей модели — service-to-service auth применяется только к ops-маршрутам. В pilot-профиле бизнес-эндпоинт может быть защищен при необходимости.

### 1.1) User identifier linkage для stories

User identity на уровне доменной истории передаётся не через Bearer-токен, а в payload intake-контракта:

- Входной контракт: `submitter.external_user_id` (required), `submitter.identity_issuer` (optional) — `src/core/intake/contracts.py`.
- Валидация: `parse_story_intake_request` требует непустой `submitter.external_user_id`.
- Привязка к доменной модели: `StoryIntakeService.create_story` записывает
  - `submitter_external_user_id=request.submitter.external_user_id`
  - `submitter_identity_issuer=request.submitter.identity_issuer`
  в `StoryRecord` (`src/core/application/services.py`).
- Поля persistence-контракта: `StoryRecord.submitter_external_user_id`, `StoryRecord.submitter_identity_issuer` (`src/core/domain/contracts.py`).

Это означает, что текущая runtime-модель уже хранит устойчивую связку story -> external submitter id.

### 2) Поведение auth при наличии/отсутствии секрета

- `SERVICE_API_TOKEN` читается через `build_service_auth_from_env`.
- Если переменная отсутствует или пустая, auth переходит в disabled mode (`require()` становится no-op).
- Для `APP_PROFILE=pilot` runtime config теперь работает в strict mode: `load_config_from_env` вызывает fail-fast при отсутствии `SERVICE_API_TOKEN`.
- Сравнение токена выполняется через `secrets.compare_digest`, что исключает простейшие timing comparison ошибки.

### 3) Error и trace контракт как часть security-операционки

- Ошибки доступа маппятся в `UNAUTHORIZED` envelope (`build_error_envelope`).
- `trace_id` сохраняется в ответах и structured logs:
  - `src/core/api/envelope.py`
  - `src/core/api/logging.py`
  - `tests/test_trace_propagation.py`

### 4) Runtime env contract (фактически используемый)

| Variable | Where used | Operational meaning |
|---|---|---|
| `SERVICE_API_TOKEN` | `src/core/api/security.py` | Включает/фиксирует service auth gate |
| `APP_PROFILE` | `src/core/config/schema.py` | Переключает demo/pilot defaults |
| `API_BASE_URL` | `src/core/config/schema.py` | Обязательный базовый URL runtime profile |
| `REQUEST_TIMEOUT_S` | `src/core/config/schema.py` | Таймаут исходящих запросов/политик |
| `FF_WALLET_ADAPTER` | `src/core/config/schema.py` | Override adapter behavior |
| `FF_BLOCKCHAIN_ADAPTER` | `src/core/config/schema.py` | Override adapter behavior |
| `FF_TOKENIZATION_PIPELINE` | `src/core/config/schema.py` | Override pipeline behavior |
| `LOG_LEVEL` | `src/core/config/schema.py` | Уровень логирования |

### 5) Readiness and auth boundary semantics

- `GET /ready` всегда публичный и не требует service token.
- `GET /protected/status` и `GET /metrics` — единственные маршруты с обязательным service token.
- В `demo` profile при пустом `SERVICE_API_TOKEN` protected checks de-facto становятся permissive; в `pilot` конфиг не стартует без токена.

### 6) Test evidence

- `tests/test_api_security_and_ops.py`
  - проверяет Bearer/X-Service-Token extraction;
  - проверяет reject без токена при enabled auth;
  - проверяет allow в disabled режиме;
  - проверяет metrics/alert contract для auth failures.
- `tests/test_http_transport_smoke.py`
  - проверяет policy map (public/protected);
  - проверяет 401/200 поведение на реальном HTTP transport.
- `tests/test_error_envelope_contract.py`
  - проверяет маппинг `UnauthorizedError` -> `UNAUTHORIZED`.
- `tests/test_trace_propagation.py`
  - проверяет трассировку `trace_id` в error path.
- `tests/test_story_intake_contract.py`
  - проверяет обязательность `submitter.external_user_id`.
- `tests/test_story_repository_lifecycle.py`
  - проверяет сохранение `submitter_external_user_id` и `submitter_identity_issuer`.

## Архитектурные последствия и ограничения

- Security baseline минималистичен и прозрачен: легко аудировать, но он intentionally narrow (service token gate only).
- Основная операционная опасность — неявный запуск в auth-disabled mode при незаданном `SERVICE_API_TOKEN`.
- Внутри текущего scope это приемлемо для demo-режима, но требует явного контроля в production-like окружениях.

## Strict Bearer runbook (current runtime)

1. Для `pilot` обязательно установить `SERVICE_API_TOKEN` (иначе startup config validation завершится ошибкой).
2. Для `demo` тоже установить `SERVICE_API_TOKEN`, если нужен строгий режим API gate.
3. Проверить, что protected вызовы несут `Authorization: Bearer ...` (или `X-Service-Token`):
   - `GET /protected/status`
   - `GET /metrics`
4. Выполнить контрольные тесты:
   - `python3 -m pytest tests/test_api_security_and_ops.py tests/test_http_transport_smoke.py tests/test_error_envelope_contract.py tests/test_trace_propagation.py tests/test_config_loading.py -q`
5. Оценить `auth_failures` через `ApiMetrics.alert_contract()` для сигнализации инцидентов.

## Planned target

- Полноценный server auth для business-operations API:
  - `ServiceTokenAuth.require()` применяется ко всем защищаемым handler/route операциям, а не только к `handle_protected_status`.
  - Policy по умолчанию для production-like профиля: fail-fast startup при пустом/отсутствующем `SERVICE_API_TOKEN`.
  - Единый список публичных vs защищённых операций фиксируется в runtime docs + tests.
- Ввести формальную policy документацию по key lifecycle:
  - ротация, TTL, revoke, emergency replace.
- Добавить интеграцию с внешним secret manager (если выйдем за рамки single token модели).
- При необходимости расширить модель до keyset/multi-token с audit metadata.

## Gaps / risks

- В `demo` профиль всё ещё может работать в auth-disabled режиме при пустом `SERVICE_API_TOKEN`; это допустимо для демо, но рискованно без операционного контроля.
- Бизнес-эндпоинт (`POST /intake/stories`) публичен — это осознанное решение для текущей фазы, но в production-like окружении может потребоваться auth gate.
- Отсутствует отдельный формализованный документ по ротации и аудит-требованиям для сервисных ключей.
- Нет transport-level rate limiting/WAF логики в текущем `src/core` scope.

## Контрольные проверки

- Конфиг валидность: `python3 -m pytest tests/test_config_loading.py -q`
- Security baseline: `python3 -m pytest tests/test_api_security_and_ops.py -q`
