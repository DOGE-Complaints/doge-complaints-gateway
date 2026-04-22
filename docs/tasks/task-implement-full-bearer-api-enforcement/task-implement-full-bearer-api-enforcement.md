## Task: implement — full bearer auth enforcement across API boundary

### Цель
Ввести полноценный server-side Bearer enforcement для всех защищаемых API операций в `doge-complaints-gateway`, чтобы service auth применялся не точечно, а системно.

### Почему это важно (риск)
Сейчас токеновая защита реализована технически корректно, но используется ограниченно. В результате можно получить ложное ощущение «сервер целиком под Bearer», хотя в коде это не так.

### Scope
Входит в задачу:
- унифицированное применение auth-check в API boundary;
- policy fail-fast для production-like профиля без `SERVICE_API_TOKEN`;
- тесты на позитивные/негативные сценарии auth enforcement.

Не входит:
- полноценный end-user OAuth/OIDC flow;
- WAF/rate-limiting на транспортном уровне;
- внешние secret managers (Vault/KMS) как обязательная часть внедрения.

### Факты из кода (Code Facts / SSOT)
1) `src/core/api/security.py`
- `extract_service_token` принимает токен из `Authorization: Bearer ...` и `X-Service-Token`.
- `ServiceTokenAuth.require` использует `secrets.compare_digest`.
- `build_service_auth_from_env` отключает auth, если `SERVICE_API_TOKEN` отсутствует.

2) `src/core/api/handlers.py`
- `ServiceTokenAuth.require` вызывается в `handle_protected_status`.
- Остальные handlers (`handle_health`, `handle_readiness`, `handle_metrics`) не содержат auth enforcement.

3) `tests/test_api_security_and_ops.py`
- Подтверждает: reject без токена при enabled auth.
- Подтверждает: allow при valid Bearer.
- Подтверждает: disabled mode разрешает вызов без заголовка.

4) `docs/analysis/analysis-02-bearer-server-auth-readiness.md`
- Зафиксирован gap: нет универсального применения Bearer ко всем бизнес-операциям API.

### Gap / Проблема
- Auth реализация есть, но enforcement не описан и не закреплен как единый policy на уровне всех защищаемых операций.
- Нет явного production guardrail для обязательного `SERVICE_API_TOKEN`.
- Нет единой матрицы тестов «какие endpoints публичные, какие обязаны требовать токен».

### AC/DoD
- [x] (P0) Определён и задокументирован публичный/защищённый список API операций в runtime docs.
- [x] (P0) Для каждой защищённой операции в API boundary применяется единый auth gate (`ServiceTokenAuth.require` или эквивалентный централизованный слой).
- [x] (P0) Для production-like профиля без `SERVICE_API_TOKEN` реализован fail-fast startup policy.
- [x] (P0) Добавлены/обновлены тесты, которые доказывают:
  - [x] reject без токена для защищённых операций;
  - [x] accept с валидным Bearer;
  - [x] reject с невалидным токеном;
  - [x] корректный trace/error envelope для auth failures.
- [x] (P1) Runtime docs (`security-env-api-access.md`, `api-reference/API_REFERENCE.md`) синхронизированы с итоговым enforcement policy.

### Где менять код
Runtime:
- `src/core/api/security.py`
- `src/core/api/handlers.py`
- `src/core/api/dependencies.py`
- `src/core/config/schema.py` (если policy привязывается к profile rules)

Tests:
- `tests/test_api_security_and_ops.py`
- Дополнительные API contract/ops tests в `tests/` по фактическому списку защищённых операций.

Docs:
- `docs/runtime-docs/security-env-api-access.md`
- `docs/runtime-docs/api-reference/API_REFERENCE.md`
- `docs/runtime-docs/api-reference/openapi.yaml` (если меняется declared auth requirement)

### План выполнения (Execution Plan)
1) Зафиксировать матрицу операций API (public vs protected) и целевой enforcement policy.
2) Внедрить единый механизм применения auth-check на защищённые операции.
3) Ввести fail-fast policy для production-like запуска без `SERVICE_API_TOKEN`.
4) Расширить тесты на все целевые protected операции и негативные сценарии.
5) Обновить runtime docs и API reference в соответствии с фактическим поведением.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_api_security_and_ops.py -q
python3 -m pytest tests/test_error_envelope_contract.py tests/test_trace_propagation.py -q
python3 -m pytest tests/test_config_loading.py -q
```
