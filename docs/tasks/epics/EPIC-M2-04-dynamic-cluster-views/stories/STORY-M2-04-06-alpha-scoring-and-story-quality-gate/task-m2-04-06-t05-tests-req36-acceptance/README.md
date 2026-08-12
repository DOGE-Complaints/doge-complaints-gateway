## Task workspace — `task-m2-04-06-t05-tests-req36-acceptance`

- Story: [`../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md`](../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md)
- Decision Ref: REQ-36 §5 (all AC)

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000015`  
---

## Task: tests — REQ-36 acceptance matrix

### Цель
Закрыть все acceptance criteria REQ-36 §5 автотестами: unit `alpha_score`, dominant selection, geo-agnostic score, promotion regression.

### Факты из кода
1. REQ-36 §5 — 7 чекбоксов AC (score range, rich vs poor story, geo=None, dominant, promotion, tie_breaker config).
2. Нет [`tests/test_alpha_score.py`](../../../../../../../tests/test_alpha_score.py) — файл отсутствует.
3. [`tests/test_promotion_canonical_type_gate.py`](../../../../../../../tests/test_promotion_canonical_type_gate.py) — partial promotion AC.

### Gap / Проблема
Нет регрессионного пакета, привязанного к REQ-36 §5 end-to-end.

### AC/DoD
- [ ] (P0) `tests/test_alpha_score.py`: rich story score > 60; sparse story < 20; geo=None → geo component 0.
- [ ] (P0) `select_dominant_story` picks higher alpha_score story (fixture).
- [ ] (P0) Promotion: cluster only `observation` → `no_actionable_canonical_type` (reuse/extend existing test).
- [ ] (P1) `python3 -m pytest tests/test_alpha_score.py tests/test_promotion_canonical_type_gate.py -q`
- [ ] (P1) `python3 -m pytest -q` — no regressions.

### Где менять код
- **Создать:** [`tests/test_alpha_score.py`](../../../../../../../tests/test_alpha_score.py)
- **Опционально:** extend [`tests/test_promotion_canonical_type_gate.py`](../../../../../../../tests/test_promotion_canonical_type_gate.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_alpha_score.py -q --tb=short
cd doge-complaints-gateway && python3 -m pytest -q
```
