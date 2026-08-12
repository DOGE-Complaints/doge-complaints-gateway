## Task workspace — `task-m2-18-02-t11-zone-f-logging-setup-contract`

- Story: [`../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md`](../STORY-M2-18-02-cross-layer-contract-zones-a-i-req39.md)
- Decision Ref: [`../../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../../requirements/39-cross-layer-contract-testing.md) — Zone **F**

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000020`  
---

## Task: tests — configure_logging ↔ pytest/uvicorn context

### Цель
configure_logging ↔ pytest/uvicorn context (Zone **F**). Offline contract tests per REQ-39.

### Факты из кода
1. `configure_logging` — `logging_setup.py`.
2. REQ-39 §F — pytest vs lifespan behavior (GAP-10 related).

### Gap / Проблема
Logging double-init or missing handlers under TestClient.

### AC/DoD
- [x] (P0) F-01..F-04 per REQ-39 §F.
- [x] (P1) `conftest.py` fixture if required by REQ-39 §«Системный инвариант».

### Где менять код
- `tests/test_logging_setup.py` (new)
- `tests/conftest.py` (optional fixture)

### Out of scope
REQ-37 StoryDebugLogger scope.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_logging_setup.py
```
