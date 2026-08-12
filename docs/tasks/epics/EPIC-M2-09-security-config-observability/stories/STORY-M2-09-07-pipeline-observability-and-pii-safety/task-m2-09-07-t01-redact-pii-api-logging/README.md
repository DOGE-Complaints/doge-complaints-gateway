## Task workspace — `task-m2-09-07-t01-redact-pii-api-logging`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: [`../../../../../../requirements/37-pipeline-observability-and-pii-safety.md`](../../../../../../requirements/37-pipeline-observability-and-pii-safety.md) §2.2; G-06

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~30 min  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: implement — `redact_pii()` in `api/logging.py`

### Цель
Добавить единую функцию редакции PII для narrative полей перед любым логированием (REQ-37 §2.2, G-06).

### Факты из кода
1. [`src/core/api/logging.py`](../../../../../../../src/core/api/logging.py) L1–33 — `log_error`, `log_api_event` only; **нет** `redact_pii`.
2. `rg redact_pii` по `src/` — 0 совпадений.
3. [`StoryRecord`](../../../../../../../src/core/domain/contracts.py) L65–66 — `privacy_contains_pii: bool`.

### Gap / Проблема
**GAP-37-03:** нет централизованной PII-редакции; защита неявная.

### AC/DoD
- [ ] (P0) `def redact_pii(text: str, contains_pii: bool) -> str` — `True` → `"[REDACTED]"`, else full text.
- [ ] (P1) Unit tests in T06 or local `test_redact_pii` subset.

### Где менять код
- [`src/core/api/logging.py`](../../../../../../../src/core/api/logging.py)

### Out of scope
- `StoryDebugLogger` (T02)
- Pipeline wiring (T03+)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.api.logging import redact_pii; assert redact_pii('x', True)=='[REDACTED]'"
```
