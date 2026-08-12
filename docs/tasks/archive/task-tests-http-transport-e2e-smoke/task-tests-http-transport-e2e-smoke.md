## Task: tests — HTTP transport smoke and contract checks

### Цель
Добавить transport-level smoke/integration тесты для реального HTTP запуска, чтобы валидировать контракты endpoint-ов не только через прямые вызовы handler функций.

### Почему это важно (риск)
Только handler-level тесты не покрывают риски маршрутизации, заголовков, HTTP статусов, content-type и real request/response поведения.

### Scope
Входит:
- smoke tests для `/health`, `/ready`, `/protected/status`, `/metrics`;
- проверка auth поведения через реальные HTTP запросы;
- contract checks для статуса/формата envelope.

Не входит:
- browser E2E UI tests;
- нагрузочные тесты.

### Факты из кода (Code Facts / SSOT)
1) `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`
- зафиксировано отсутствие e2e с реальным HTTP transport/server process.

2) `tests/test_api_security_and_ops.py`
- текущий набор проверяет handler functions in-process, без transport stack.

3) `src/core/api/asgi_app.py`
- рабочий ASGI HTTP surface и endpoint dispatch.

### Gap / Проблема
- Нет regression safety net на уровне реального HTTP transport.
- Возможные ошибки маршрутов/headers/status-кодов могут не ловиться unit/in-process тестами.

### AC/DoD
- [x] (P0) Добавлены transport smoke tests для `/health` и `/ready`.
- [x] (P0) Добавлены auth transport checks для `/protected/status` и `/metrics` (401/200 сценарии).
- [x] (P0) Проверяется envelope-структура и content-type на HTTP уровне.
- [x] (P1) Обновлена тестовая матрица в runtime docs с новым coverage.

### Где менять код
- `tests/` (новый test module для HTTP smoke/integration)
- `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`
- при необходимости `src/core/api/asgi_app.py` (ASGI entrypoint module)

### План выполнения (Execution Plan)
1) Определить тестовый запуск transport процесса.
2) Реализовать HTTP requests для базовых endpoint-ов.
3) Добавить auth positive/negative сценарии.
4) Зафиксировать checks на envelope/content-type/status.
5) Обновить runtime test matrix.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_api_security_and_ops.py -q
# + новый HTTP smoke module после реализации
```
