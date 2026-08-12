## Task workspace — `task-m2-04-06-t03-cluster-tie-breaker-config-engine`

- Story: [`../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md`](../STORY-M2-04-06-alpha-scoring-and-story-quality-gate.md)
- Decision Ref: REQ-36 §2.4; G-03

---
**Приоритет:** P1  
**Сложность:** S  
**Оценка времени:** ~30 min  
**Статус:** ready  
**Wave:** `pkg-000015`  
---

## Task: implement — `CLUSTER_TIE_BREAKER=alpha` contract and engine field

### Цель
Зафиксировать контракт REQ-36 §2.4: единственное значение `CLUSTER_TIE_BREAKER=alpha` (default `alpha`); документировать связь с `ClusteringEngine.tie_breaker`; добавить negative config test если отсутствует.

### Факты из кода
1. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) L339–343 — `_parse_cluster_tie_breaker` уже отклоняет не-`alpha`.
2. [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py) L175 — поле `tie_breaker: str = "alpha"`; **не читается** в методах engine (GAP-36-03).
3. [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) L84 — передаёт `tie_breaker=self.config.cluster_tie_breaker`.
4. [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py) L56 — assert default `alpha`; **нет** теста на invalid value.

### Gap / Проблема
**GAP-36-03:** `tie_breaker` в engine объявлен, но не участвует в логике (dominant StoryRecord выбирается в projection, не в engine).  
**GAP-36-07:** negative test для `CLUSTER_TIE_BREAKER=lexical` (или иное) → `ConfigError`.

### AC/DoD
- [ ] (P0) `example.env` документирует `CLUSTER_TIE_BREAKER=alpha` и roadmap-only для других значений.
- [ ] (P1) Тест: `CLUSTER_TIE_BREAKER=lexical` → `ConfigError` при load (если ещё нет).
- [ ] (P1) Комментарий в `engine.py` или STORY: product dominant = `select_dominant_story`; `tie_breaker` reserved / future cluster-member pick.
- [ ] (P1) Не ломать существующий `test_config_loading` default alpha.

### Где менять код
- [`example.env`](../../../../../../../example.env)
- [`tests/test_config_loading.py`](../../../../../../../tests/test_config_loading.py) (negative case)
- Опционально docstring: [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py)

### Out of scope
- Полная интеграция `alpha_score` внутрь `ClusteringEngine._dominant_for_profiles` (signal dimensions ≠ StoryRecord)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q -k tie_breaker
```
