## Task workspace — `task-m2-06-05-t05-issue-create-bridge-dominant-geo`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §4.5; GAP-40-05

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~30–45 min  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: implement — dominant story geo in projection bridge

### Цель
В `StoryPromotionProjectionBridge.build_projection_input()` извлечь `dominant_story.geo` и передать в `build_projection_input_from_draft(geo_snapshot=…)`.

### Факты из кода
1. [`issue_create.py`](../../../../../../../src/core/application/issue_create.py) L108–121 — `select_dominant_story(cluster_stories)`; return `build_projection_input_from_draft(issue_id=…, draft=draft)` **без** geo.
2. REQ-40 §2 — MVP: geo доминантной истории (та же, что для title/type/labels).
3. [`select_dominant_story`](../../../../../../../src/core/projection/extraction_policy.py) L26 — уже используется.

### Gap / Проблема
**GAP-40-05:** promotion→projection bridge — точка разрыва geo propagation pipeline.

### AC/DoD
- [ ] (P0) `geo_snapshot = dominant_story.geo` после `select_dominant_story`.
- [ ] (P0) `build_projection_input_from_draft(..., geo_snapshot=geo_snapshot)`.
- [ ] (P0) Create и extend paths через bridge получают geo (grep other `build_projection_input` call sites — same method).
- [ ] (P1) T04 Done (signature exists).

### Где менять код
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py)

### Out of scope
- GeoService / intake (EPIC-M2-08)
- REQ-24 read filters (T06 only asserts payload shape)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/ -q -k "issue_create or projection" --tb=short 2>/dev/null | tail -5
```
