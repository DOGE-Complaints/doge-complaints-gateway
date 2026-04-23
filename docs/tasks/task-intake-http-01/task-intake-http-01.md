## Task: implement — POST /intake/stories runtime endpoint

### Цель
Экспонировать в runtime API уже существующий intake-контракт (`StoryIntakeRequest`) через HTTP endpoint `POST /intake/stories`.

### Почему это важно (риск)
Без HTTP exposure intake-контракт существует только на уровне доменных функций, что блокирует demo-ready сценарий реальной отправки истории через API boundary.

### Scope
Входит:
- роут `POST /intake/stories` в ASGI;
- HTTP handler orchestration `parse_story_intake_request -> StoryIntakeService.create_story -> build_story_intake_response`;
- error envelope для validation/domain ошибок.

Не входит:
- создание issue endpoint;
- построение SPA projection.

### Факты из кода (Code Facts / SSOT)
1) `src/core/api/asgi_app.py`
- в runtime присутствуют только `@app.get(...)` роуты.

2) `src/core/intake/contracts.py`
- есть parser `parse_story_intake_request` и response builder `build_story_intake_response`.

3) `docs/runtime-docs/api-reference/openapi.yaml`
- `/intake/stories` помечен как `planned-http-binding-existing-contract`.

### Gap / Проблема
`GAP-IP-001`: intake контракт есть, но не доступен через HTTP runtime.

### Decision Points
- **PM decision:** обеспечить demo-ready intake API сейчас с минимальным внешним контрактом.
- **CTO decision:** подключить endpoint через существующие сервисы и envelope, без дублирования валидации.
- **Options:**
  - A: быстрый endpoint с минимальной оркестрацией только happy-path.
  - B: endpoint с полной error taxonomy + trace propagation + строгими контрактными тестами.
- **Recommendation:** вариант B (чуть дольше, но без костылей и с фундаментом для issue/create flow).

### AC/DoD
- [ ] (P0) В `asgi_app` добавлен `POST /intake/stories`.
- [ ] (P0) Endpoint использует `parse_story_intake_request` и `StoryIntakeService`.
- [ ] (P0) Успешный ответ возвращает envelope от `build_story_intake_response`.
- [ ] (P0) Validation ошибки возвращаются через `ErrorEnvelope` с корректным `trace_id`.
- [ ] (P1) Добавлены HTTP tests для 200 и 400 сценариев.
- [ ] (P1) OpenAPI runtime-state для `/intake/stories` синхронизирован.

### Где менять код
- `src/core/api/asgi_app.py`
- `src/core/api/handlers.py` (если выносится orchestration)
- `src/core/api/dependencies.py`
- `tests/` (новый HTTP intake test module)
- `docs/runtime-docs/api-reference/openapi.yaml`

### План выполнения (Execution Plan)
1) Добавить endpoint и wiring зависимостей.
2) Подключить parser/service/response builder.
3) Добавить обработку ошибок в envelope.
4) Добавить HTTP contract tests.
5) Синхронизировать OpenAPI и runtime docs.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_http_transport_smoke.py -q
python3 -m pytest tests/test_http_intake_endpoint.py -q
python3 -m pytest tests/test_e2e_intake_create_spa_contract.py -q
```
