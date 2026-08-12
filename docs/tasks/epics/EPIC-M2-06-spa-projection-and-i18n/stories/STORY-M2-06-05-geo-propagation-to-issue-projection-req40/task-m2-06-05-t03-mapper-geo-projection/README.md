## Task workspace — `task-m2-06-05-t03-mapper-geo-projection`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §4.3; GAP-40-03

---
**Приоритет:** P2  
**Сложность:** M  
**Оценка времени:** ~45–60 min  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: implement — `project_distinct_issue()` geo mapping

### Цель
В `project_distinct_issue()` собрать geo dict из `ProjectionInput` geo_* полей и передать в `DOGEIssue(geo=…)`.

### Факты из кода
1. [`projection/mapper.py`](../../../../../../../src/core/projection/mapper.py) L20–40 — маппинг без geo.
2. REQ-40 §4.3 — geo dict только если `geo_lat` и `geo_lon` not None; optional string keys omitted when empty.
3. T01/T02 должны быть выполнены до этого таска.

### Gap / Проблема
**GAP-40-03:** mapper не связывает domain geo fields с DTO geo sub-object.

### AC/DoD
- [ ] (P0) При `data.geo_lat is not None and data.geo_lon is not None` — geo dict с `lat`, `lon`.
- [ ] (P0) Optional: `label`, `district`, `settlement`, `region`, `country` — только если соответствующие input fields truthy.
- [ ] (P0) Иначе `geo=None` на `DOGEIssue`.
- [ ] (P1) Существующие projection unit tests зелёные.

### Где менять код
- [`src/core/projection/mapper.py`](../../../../../../../src/core/projection/mapper.py)

### Out of scope
- Populating `ProjectionInput` geo fields (T04–T05)
- Acceptance e2e (T06)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/ -q -k "projection" --tb=short 2>/dev/null | tail -5
```
