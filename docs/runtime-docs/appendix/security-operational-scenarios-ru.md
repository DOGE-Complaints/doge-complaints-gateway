# Security Operational Scenarios (RU)

## 1. Security boundary в текущем runtime

Фактическая граница доступа задается `ServiceTokenAuth`:

- извлечение токена: `extract_service_token`
- проверка: `ServiceTokenAuth.require`
- использование в защищенном handler: `handle_protected_status`

Источники:

- `src/core/api/security.py`
- `src/core/api/handlers.py`
- `tests/test_api_security_and_ops.py`

## 2. Сценарий: token missing

### Наблюдаемое поведение

- При enabled auth и отсутствии токена возвращается `UNAUTHORIZED`.
- `auth_failures` увеличивается в `ApiMetrics`.

Источники:

- `tests/test_api_security_and_ops.py::test_protected_route_rejects_without_token_when_auth_enabled`
- `src/core/api/metrics.py`

### Операционное значение

- Это основной ранний индикатор неправильной интеграции upstream-сервиса.
- Должен быть частью smoke/checklist после деплоя.

## 3. Сценарий: token invalid

### Наблюдаемое поведение

- Проверка использует `secrets.compare_digest`.
- На mismatch возвращается `UNAUTHORIZED`.

Источник:

- `src/core/api/security.py`

### Операционное значение

- Рекомендуется быстрый rollback к последнему валидному секрету в CI/secret-store.

## 4. Сценарий: auth disabled by configuration

### Наблюдаемое поведение

- Если `SERVICE_API_TOKEN` не задан, `ServiceTokenAuth.disabled()` делает `require()` no-op.

Источники:

- `src/core/api/security.py::build_service_auth_from_env`
- `tests/test_api_security_and_ops.py::test_service_auth_disabled_allows_protected_without_header`

### Риск

- Возможен неявный запуск в слабом security режиме без явного инцидента.

### Контроль

- Явно фиксировать состояние auth в deployment checklist.
- Запретить production deployment без установленного `SERVICE_API_TOKEN`.

## 5. Сценарий: traceability и расследование ошибок

### Наблюдаемое поведение

- `trace_id` попадает в success/error envelopes.
- `trace_id` сохраняется в structured logging paths.

Источники:

- `src/core/api/envelope.py`
- `src/core/api/logging.py`
- `tests/test_trace_propagation.py`

### Операционное значение

- Минимизируется время корреляции запроса и лог-событий при инциденте.

## 6. Сценарий: metrics-based security monitoring

### Наблюдаемое поведение

- `ApiMetrics.alert_contract()` формирует минимальный alert критерий по `auth_failures`.

Источники:

- `src/core/api/metrics.py`
- `tests/test_api_security_and_ops.py::test_metrics_alert_contract_shape`

### Ограничение

- Это in-process baseline; нет внешней alerting интеграции в текущем scope.

## 7. Planned hardening

- formal key rotation/revocation standard,
- external secret manager integration,
- deployment policy: fail startup if strict auth expected but token missing.
