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
- Использование в защищенной операции: `handle_protected_status` (`src/core/api/handlers.py`).

Практический смысл: gateway защищает вызовы между сервисами/интеграторами, но не реализует full user auth flow.

### 2) Поведение auth при наличии/отсутствии секрета

- `SERVICE_API_TOKEN` читается через `build_service_auth_from_env`.
- Если переменная отсутствует или пустая, auth переходит в disabled mode (`require()` становится no-op).
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

### 5) Test evidence

- `tests/test_api_security_and_ops.py`
  - проверяет Bearer/X-Service-Token extraction;
  - проверяет reject без токена при enabled auth;
  - проверяет allow в disabled режиме;
  - проверяет metrics/alert contract для auth failures.
- `tests/test_error_envelope_contract.py`
  - проверяет маппинг `UnauthorizedError` -> `UNAUTHORIZED`.
- `tests/test_trace_propagation.py`
  - проверяет трассировку `trace_id` в error path.

## Архитектурные последствия и ограничения

- Security baseline минималистичен и прозрачен: легко аудировать, но он intentionally narrow (service token gate only).
- Основная операционная опасность — неявный запуск в auth-disabled mode при незаданном `SERVICE_API_TOKEN`.
- Внутри текущего scope это приемлемо для demo-режима, но требует явного контроля в production-like окружениях.

## Strict Bearer runbook (current runtime)

1. Установить `SERVICE_API_TOKEN` в runtime environment.
2. Проверить, что protected вызовы несут `Authorization: Bearer ...` (или `X-Service-Token`).
3. Выполнить контрольные тесты:
   - `python3 -m pytest tests/test_api_security_and_ops.py tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q`
4. Оценить `auth_failures` через `ApiMetrics.alert_contract()` для сигнализации инцидентов.

## Planned target

- Ввести формальную policy документацию по key lifecycle:
  - ротация, TTL, revoke, emergency replace.
- Добавить интеграцию с внешним secret manager (если выйдем за рамки single token модели).
- При необходимости расширить модель до keyset/multi-token с audit metadata.

## Gaps / risks

- Пустой/отсутствующий `SERVICE_API_TOKEN` выключает gate, что рискованно без явного deployment guard.
- Отсутствует отдельный формализованный документ по ротации и аудит-требованиям для сервисных ключей.
- Нет transport-level rate limiting/WAF логики в текущем `src/core` scope.

## Контрольные проверки

- Конфиг валидность: `python3 -m pytest tests/test_config_loading.py -q`
- Security baseline: `python3 -m pytest tests/test_api_security_and_ops.py -q`
