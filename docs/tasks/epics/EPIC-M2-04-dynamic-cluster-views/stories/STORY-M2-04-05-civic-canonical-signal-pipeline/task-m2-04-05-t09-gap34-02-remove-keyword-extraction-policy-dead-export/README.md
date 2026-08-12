## Task workspace — `task-m2-04-05-t09-gap34-02-remove-keyword-extraction-policy-dead-export`

- Story: [`../STORY-M2-04-05-civic-canonical-signal-pipeline.md`](../STORY-M2-04-05-civic-canonical-signal-pipeline.md)
- Decision Ref: [`../../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md`](../../../../../../analysis/audit-req34-civic-clustering-canonical-pipeline-2026-05-15.md) GAP-34-02

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** < 10 мин  
**Статус:** ready  
---

## Task: refactor — remove dead `KEYWORD_EXTRACTION_POLICY` export

### Цель
Убрать последний публичный след keyword extraction policy после REQ-34; не путать с `_CANONICAL_SIGNAL_POLICY = "v2.canonical"` в orchestrator (другой namespace).

### Почему это важно (риск)
Низкий для runtime; средний для onboarding — константа предполагает, что keyword mode ещё поддерживается.

### Факты из кода
1. [`src/core/cluster/vocabulary.py`](../../../../../../../src/core/cluster/vocabulary.py) L88:
   ```python
   KEYWORD_EXTRACTION_POLICY = "v1.keyword"
   ```
2. [`src/core/cluster/__init__.py`](../../../../../../../src/core/cluster/__init__.py) L17, L37 — import и `__all__`.
3. `rg KEYWORD_EXTRACTION_POLICY` — использований в production/tests вне cluster package **нет** (аудит 2026-05-15).

### Gap / Проблема
**GAP-34-02 (LOW):** dead export противоречит «full removal of legacy» из REQ-34.

### AC/DoD
- [x] (P0) Константа удалена из `vocabulary.py`.
- [x] (P0) Убрана из `cluster/__init__.py` imports и `__all__`.
- [x] (P0) `rg -n KEYWORD_EXTRACTION_POLICY src/ tests/` → no matches (или только docs — допустимо обновить при необходимости).
- [x] (P1) `python3 -m pytest -q` — без регрессий.

### Где менять код
- [`src/core/cluster/vocabulary.py`](../../../../../../../src/core/cluster/vocabulary.py)
- [`src/core/cluster/__init__.py`](../../../../../../../src/core/cluster/__init__.py)

### План выполнения
1. Delete `KEYWORD_EXTRACTION_POLICY` line.
2. Remove from `__init__.py`.
3. Run targeted import smoke: `python3 -c "from core.cluster import CIVIC_LENSES; print(len(CIVIC_LENSES))"`.

### Команды проверки
```bash
cd doge-complaints-gateway
rg -n KEYWORD_EXTRACTION_POLICY src/ tests/
python3 -m pytest tests/test_clustering_engine.py tests/test_signal_extraction_canonical.py -q --tb=short
```
