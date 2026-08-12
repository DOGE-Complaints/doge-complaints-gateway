## Task workspace — `task-m2-04-06-t01-cluster-alpha-score-module`

- Story: [`../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md`](../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md)
- Decision Ref: [`../../../../../../requirements/36-alpha-scoring-and-story-quality-gate.md`](../../../../../../requirements/36-alpha-scoring-and-story-quality-gate.md) §2.2, §3; G-03

---
**Приоритет:** P0  
**Сложность:** M  
**Оценка времени:** 1–2 ч  
**Статус:** ready  
**Wave:** `pkg-000015`  
**Supersedes / Superseded by:** complements STORY-M2-04-05 T04 interim picker; does not change promotion gate code  
---

## Task: implement — `cluster/alpha.py` with `alpha_score()`

### Цель
Реализовать детерминированную функцию `alpha_score(story: StoryRecord) -> float` (0–100) по REQ-36 §2.2 в отдельном модуле `cluster/alpha.py` (single responsibility, testability).

### Почему это важно (риск)
Без формулы качества доминантная история выбирается эвристикой (`len(labels)`, `story_id`) — SPA и Issue получают слабый narrative anchor.

### Out of scope
- Замена `select_dominant_story` (T02)
- Изменения `promotion/gates.py` (T04 verify only)
- `identity_issuer` intake (REQ-33, verify-only)

### Факты из кода
1. REQ-36 §2.2 — три измерения: classification 0–30, narrative richness 0–40, geo accuracy 0–30; max 100.
2. REQ-36 §2.2 псевдокод ссылается на `narrative_summary_json`; фактическая модель — [`StoryRecord.narrative_summary`](../../../../../../../src/core/domain/contracts.py) `dict[str, str] | None` (GAP-36-04: реализовать по dict + `narrative_consistency_notes`).
3. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) L49–58 — `narrative_canonical_type`, `narrative_canonical_labels`, `narrative_original_text`, `geo`, `created_at`.
4. `rg alpha_score` по `src/` — 0 совпадений; модуля `cluster/alpha.py` нет.

### Gap / Проблема
**GAP-36-01:** отсутствует `alpha_score()` и модуль `cluster/alpha.py`.  
**GAP-36-04:** REQ-формула должна использовать `narrative_summary` (dict), не несуществующее поле `narrative_summary_json`.

### AC/DoD
- [ ] (P0) Новый [`src/core/cluster/alpha.py`](../../../../../../../src/core/cluster/alpha.py) с `alpha_score(story: StoryRecord) -> float`.
- [ ] (P0) Classification: +12 при `narrative_canonical_type`; +6 за label, cap 18 (3 labels).
- [ ] (P0) Narrative: `min(len(original_text.strip())/15, 20)`; +10 если `narrative_summary` truthy; +10 если `narrative_consistency_notes`.
- [ ] (P0) Geo: +10 if `story.geo`; +`confidence * 20`; geo=None → 0 за измерение 3.
- [ ] (P1) Экспорт из `core.cluster` при необходимости для T02.

### Где менять код
- **Создать:** [`src/core/cluster/alpha.py`](../../../../../../../src/core/cluster/alpha.py)
- **Опционально:** [`src/core/cluster/__init__.py`](../../../../../../../src/core/cluster/__init__.py) re-export

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.cluster.alpha import alpha_score; from core.domain import StoryRecord; print(alpha_score)"
```
