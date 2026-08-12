## Task workspace — `task-m2-18-01-t07-audit-gap39-k-geo-fixtures-decouple`

- Story: [`../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md`](../STORY-M2-18-01-cross-layer-contract-zones-j-n-req39.md)
- Decision Ref: [`../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) §6 GAP-39-K-DEP; Zone K

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~1–2 ч  
**Статус:** ready  
**Wave:** audit override (`run_mode=story18_audit_req39_followup`)  
---

## Task: tests — decouple Zone K from private helpers in test_req40

### Цель
Убрать зависимость `test_geo_propagation_contract.py` от приватных символов `tests.test_req40_geo_propagation` (`_build_orchestrator`, `_geo_kalamaja`, `_issue_payload`, `_story`).

### Почему это важно (риск)
Рефактор или удаление REQ-40 test module сломает Zone K без изменений в seam K — нарушение изоляции contract-зон.

### Факты из кода
1. [`test_geo_propagation_contract.py`](../../../../../../../tests/test_geo_propagation_contract.py) L7–12 импортирует из `tests.test_req40_geo_propagation`.
2. Приватные helpers определены в [`test_req40_geo_propagation.py`](../../../../../../../tests/test_req40_geo_propagation.py) (~L26, L54, L75, L99).

### Gap / Проблема
**AUDIT-GAP-39-K-DEP:** test-to-test coupling через underscore-prefixed helpers.

### AC/DoD
- [ ] (P0) Новый модуль `tests/geo_propagation_fixtures.py` (или `tests/fixtures/geo_propagation.py`) с публичными factory-функциями.
- [ ] (P0) `test_geo_propagation_contract.py` и `test_req40_geo_propagation.py` импортируют из fixtures, не друг из друга.
- [ ] (P0) Все Zone K tests green; `test_req40_geo_propagation.py` green.

### Где менять код
- `tests/geo_propagation_fixtures.py` (new)
- [`tests/test_geo_propagation_contract.py`](../../../../../../../tests/test_geo_propagation_contract.py)
- [`tests/test_req40_geo_propagation.py`](../../../../../../../tests/test_req40_geo_propagation.py) (import path only)

### Out of scope
- Production geo logic changes.
- `pkg-000020` edits.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_geo_propagation_contract.py tests/test_req40_geo_propagation.py
```
