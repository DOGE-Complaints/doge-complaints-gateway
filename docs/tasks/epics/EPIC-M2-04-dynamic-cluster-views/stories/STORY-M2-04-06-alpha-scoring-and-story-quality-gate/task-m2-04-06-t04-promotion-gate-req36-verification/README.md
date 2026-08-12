## Task workspace — `task-m2-04-06-t04-promotion-gate-req36-verification`

- Story: [`../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md`](../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md)
- Decision Ref: REQ-36 §2.5; STORY-M2-04-05 T05

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~20 min  
**Статус:** ready  
**Wave:** `pkg-000015`  
---

## Task: verify — REQ-36 canonical_type promotion gate (no duplicate impl)

### Цель
Подтвердить, что REQ-36 §2.5 AC «кластер без complaint/system_bug → не промотируется» уже закрыт в [`promotion/gates.py`](../../../../../../../src/core/promotion/gates.py) (REQ-34 T05); расширить тесты только при пробеле в покрытии REQ-36 wording.

### Факты из кода
1. [`src/core/promotion/gates.py`](../../../../../../../src/core/promotion/gates.py) L7–35 — `ACTIONABLE_CANONICAL_TYPES = frozenset({"complaint", "system_bug"})`; reason `no_actionable_canonical_type`.
2. [`tests/test_promotion_canonical_type_gate.py`](../../../../../../../tests/test_promotion_canonical_type_gate.py) — observation-only cluster rejected.
3. STORY-M2-04-05 T05 — gate уже реализован; **не reopen** implementation.

### Gap / Проблема
**GAP-36-05 (verify):** REQ-36 дублирует требование REQ-34 T05 — нужна явная traceability в тестах/acceptance, не новая логика gates.

### AC/DoD
- [ ] (P0) Существующий gate + test покрывают REQ-36 §2.5 — зафиксировать в `acceptance-verification` (PASS без code change) или добавить 1 тест с комментарием REQ-36.
- [ ] (P0) **Не** дублировать `evaluate_promotion_gates` logic.
- [ ] (P1) `pytest tests/test_promotion_canonical_type_gate.py -q` green.

### Где менять код
- **По умолчанию:** только [`tests/test_promotion_canonical_type_gate.py`](../../../../../../../tests/test_promotion_canonical_type_gate.py) (REQ-36 label in docstring/test name)
- **Не менять:** [`src/core/promotion/gates.py`](../../../../../../../src/core/promotion/gates.py) unless test proves gap

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_promotion_canonical_type_gate.py -q
```
