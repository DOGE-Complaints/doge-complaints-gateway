## Task workspace — `task-m2-09-07-t06-tests-req37-acceptance`

- Story: [`../STORY-M2-09-07-pipeline-observability-and-pii-safety.md`](../STORY-M2-09-07-pipeline-observability-and-pii-safety.md)
- Decision Ref: REQ-37 §5 (all AC)

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000016`  
---

## Task: tests — REQ-37 acceptance matrix

### Цель
Закрыть REQ-37 §5: JSONL file creation, 5 stages, no-op without dir, `redact_pii`, PII story log safety, `LOG_LEVEL=INFO` + `LOG_DEBUG_DIR`.

### Факты из кода
1. Нет [`tests/test_req37_pipeline_observability_pii.py`](../../../../../../../tests/test_req37_pipeline_observability_pii.py).
2. [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py) L193 — asserts `LOG_DEBUG_DIR` in env schema names only.

### Gap / Проблема
Нет регрессионного пакета для REQ-37 end-to-end acceptance.

### AC/DoD
- [ ] (P0) `redact_pii` unit tests.
- [ ] (P0) Temp `LOG_DEBUG_DIR` → `{story_id}.jsonl` with 5 stage lines after pipeline exercise (unit/integration as feasible).
- [ ] (P0) Unset `LOG_DEBUG_DIR` → no file, no error.
- [ ] (P0) `LOG_LEVEL=INFO` + `LOG_DEBUG_DIR` still creates jsonl.
- [ ] (P1) `python3 -m pytest -q` green.

### Где менять код
- **Создать:** [`tests/test_req37_pipeline_observability_pii.py`](../../../../../../../tests/test_req37_pipeline_observability_pii.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req37_pipeline_observability_pii.py -q --tb=short
cd doge-complaints-gateway && python3 -m pytest -q
```
