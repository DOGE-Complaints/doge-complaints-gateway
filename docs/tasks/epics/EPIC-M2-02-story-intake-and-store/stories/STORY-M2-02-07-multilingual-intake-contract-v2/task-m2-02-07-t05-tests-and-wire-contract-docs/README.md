## Task workspace — `task-m2-02-07-t05-tests-and-wire-contract-docs`

- Story: [`../STORY-M2-02-07-multilingual-intake-contract-v2.md`](../STORY-M2-02-07-multilingual-intake-contract-v2.md)
- Decision Ref: REQ-33 §5 Acceptance Criteria

## Task: tests — full v2 intake contract coverage and wire docs checklist

### Цель
Закрыть REQ-33 §5 в автотестах; обновить fixtures/runner под v2; зафиксировать внешний wire-doc checklist для GPT UI (без блокировки gateway, если PR отдельный).

### Факты из кода
1. [`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py), [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py) — v1 payloads.
2. [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py) — `_scenario_to_payload` (сверить с T07 M2-02-06).
3. REQ-33 §5 — AC на 202, 400, idempotency, `StoryRecord` fields, reject v1.

### Gap / Проблема
Без обновления тестов breaking v2 не защищён регрессией.

### AC/DoD
- [ ] (P0) Все пункты REQ-33 §5 покрыты unit/HTTP тестами.
- [ ] (P0) `simulation_runner` и `test_e2e_simulation_canvas_intake.py` шлют v2-shaped payload (после T01–T04).
- [ ] (P1) OpenAPI/runtime compliance tests обновлены при расхождении с v2.
- [ ] (P2) Checklist: `GPT UI/instructions/api-orchestrator.md` — отдельный трек (вне repo).

### Где менять код
- [`tests/test_story_intake_contract.py`](../../../../../../../tests/test_story_intake_contract.py)
- [`tests/test_story_intake_idempotency.py`](../../../../../../../tests/test_story_intake_idempotency.py)
- [`tests/test_http_intake_endpoint.py`](../../../../../../../tests/test_http_intake_endpoint.py)
- [`tests/test_e2e_simulation_canvas_intake.py`](../../../../../../../tests/test_e2e_simulation_canvas_intake.py)
- [`tests/simulation_runner.py`](../../../../../../../tests/simulation_runner.py)
- при необходимости [`tests/test_openapi_runtime_compliance.py`](../../../../../../../tests/test_openapi_runtime_compliance.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_story_intake_contract.py tests/test_story_intake_idempotency.py tests/test_http_intake_endpoint.py tests/test_e2e_simulation_canvas_intake.py -q --tb=short
```
