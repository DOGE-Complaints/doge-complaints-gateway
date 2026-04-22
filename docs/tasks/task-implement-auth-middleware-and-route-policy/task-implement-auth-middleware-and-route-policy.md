## Task: implement — auth middleware and protected route policy

### Цель
Ввести framework-level policy для auth (public/protected route map + middleware/dependency enforcement), чтобы безопасность API определялась декларативно на уровне transport boundary, а не точечными вызовами в отдельных обработчиках.

### Почему это важно (риск)
Даже при корректной реализации `ServiceTokenAuth` локальные route-решения могут разъезжаться между endpoint-ами. Нужен единый policy-контур, который невозможно «забыть» применить при добавлении нового маршрута.

### Scope
Входит:
- декларативный список public/protected endpoints;
- централизованная auth проверка для protected routes;
- единый mapping unauthorized/error envelopes в transport layer.

Не входит:
- user-level OAuth/OIDC;
- rate limiting / WAF.

### Факты из кода (Code Facts / SSOT)
1) `src/core/api/security.py`
- `ServiceTokenAuth.require` валидирует Bearer/X-Service-Token и выбрасывает `UnauthorizedError`.

2) `src/core/api/handlers.py`
- Auth применяется через helper `_require_service_auth` внутри конкретных handlers.
- Это снижает повтор, но не задает декларативную transport policy-карту.

3) `docs/runtime-docs/api-reference/openapi.yaml`
- security схемы описаны, но policy enforcement зависит от runtime реализации маршрутов.

4) `docs/runtime-docs/security-env-api-access.md`
- Указан protected/public split как документарный контракт.

### Gap / Проблема
- Нет middleware/dependency-слоя, который автоматически защищает весь protected scope.
- Нет единого guardrail для новых endpoint-ов на уровне route definition.

### AC/DoD
- [x] (P0) Protected/public map зафиксирован в transport layer декларативно.
- [x] (P0) Для protected endpoints auth применен через middleware/dependency policy, а не ad-hoc ручной вызов.
- [x] (P0) Unauthorized responses унифицированы с текущим envelope contract.
- [x] (P0) Добавлены тесты на policy enforcement для каждого protected endpoint.
- [x] (P1) Runtime docs и OpenAPI синхронизированы с новой policy-моделью.

### Где менять код
- `src/core/api/` (route layer/middleware/dependency module)
- `src/core/api/security.py` (если потребуется адаптация интерфейсов)
- `tests/test_api_security_and_ops.py`
- `docs/runtime-docs/security-env-api-access.md`
- `docs/runtime-docs/api-reference/openapi.yaml`
- `docs/runtime-docs/api-reference/API_REFERENCE.md`

### План выполнения (Execution Plan)
1) Описать policy-карту маршрутов (public/protected).
2) Внедрить middleware/dependency auth enforcement.
3) Выравнять error/envelope поведение.
4) Расширить тесты на route-policy coverage.
5) Обновить runtime docs/openapi.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_api_security_and_ops.py tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q
```
