## Task workspace — `task-m2-04-06-t02-select-dominant-story-alpha`

- Story: [`../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md`](../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md)
- Decision Ref: REQ-36 §2.3; G-03

---
**Приоритет:** P0  
**Сложность:** S  
**Оценка времени:** ~30 мин  
**Статус:** ready  
**Wave:** `pkg-000015`  
---

## Task: implement — wire `select_dominant_story` to `alpha_score`

### Цель
Заменить interim эвристику в `select_dominant_story` на выбор истории с максимальным `alpha_score`; при равенстве — tie-break по `created_at` ascending (старейшая побеждает), REQ-36 §2.3.

### Факты из кода
1. [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py) L25–35 — docstring «Interim … until REQ-36»; key: canonical flag, `len(labels)`, `story_id`.
2. [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) L108 — `dominant_story = select_dominant_story(cluster_stories)`.
3. REQ-36 §5 — dominant story = max `alpha_score`.

### Gap / Проблема
**GAP-36-02:** product path для Issue projection не использует alpha scoring.

### AC/DoD
- [ ] (P0) `select_dominant_story` вызывает `alpha_score` из `cluster/alpha.py` (после T01).
- [ ] (P0) Tie-break: при равном score — `min(..., key=lambda s: s.created_at)`.
- [ ] (P0) Удалить/обновить interim docstring; пустой tuple → `ValueError` сохранён.
- [ ] (P1) Unit test: две stories с разным score → победитель с большим alpha.

### Где менять код
- [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_alpha_score.py -q -k dominant 2>/dev/null || true
```
