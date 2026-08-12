## Task workspace — `task-m2-18-02-t10-zone-e-api-service-contract`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **E**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — API handler ↔ StoryIntakeService facade

### Цель
API handler ↔ StoryIntakeService facade (Zone **E**). Offline contract tests per REQ-39.

### Факты из кода
1. `handle_story_intake` — `handlers.py`.
2. `parse_story_intake_request` — `intake/contracts.py`.
3. `test_integration_cross_layer_api_app_infra.py` — avoid duplicate assertions.

### Gap / Проблема
HTTP boundary + parse + service call not tested as single contract.

### AC/DoD
- [x] (P0) E-01..E-08 per REQ-39 §E.
- [x] (P1) AC: no duplicate of existing integration test cases.

### Где менять код
- `tests/test_api_service_contract.py` (new)

### Out of scope
OpenAPI-only changes.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_api_service_contract.py
```
