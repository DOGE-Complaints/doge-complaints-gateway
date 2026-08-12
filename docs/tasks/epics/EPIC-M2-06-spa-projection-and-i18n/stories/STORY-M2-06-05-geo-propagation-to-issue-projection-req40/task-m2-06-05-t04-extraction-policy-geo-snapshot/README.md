## Task workspace — `task-m2-06-05-t04-extraction-policy-geo-snapshot`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §4.4; GAP-40-04

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~30–45 min  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: implement — `build_projection_input_from_draft(geo_snapshot=…)`

### Цель
Расширить `build_projection_input_from_draft()` параметром `geo_snapshot: StoryGeoSnapshot | None` и заполнить geo_* поля `ProjectionInput`.

### Факты из кода
1. [`extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py) L146–159 — только `issue_id`, `draft`; geo не мапится.
2. REQ-40 §4.4 — маппинг `latitude`→`geo_lat`, `longitude`→`geo_lon`, admin_* → `geo_admin_*`, `normalized_label`→`geo_normalized_label`.
3. [`StoryGeoSnapshot`](../../../../../../../src/core/domain/contracts.py) L28–40.

### Gap / Проблема
**GAP-40-04:** draft→input path игнорирует geo snapshot.

### AC/DoD
- [ ] (P0) Новый optional kw-only `geo_snapshot: StoryGeoSnapshot | None = None`.
- [ ] (P0) При `geo_snapshot is None` все geo_* на input = `None`.
- [ ] (P0) При snapshot — поля заполнены per REQ-40 §4.4.
- [ ] (P1) Export в `projection/__init__.py` при необходимости (signature only).

### Где менять код
- [`src/core/projection/extraction_policy.py`](../../../../../../../src/core/projection/extraction_policy.py)

### Out of scope
- `StoryPromotionProjectionBridge` (T05)
- Mapper (T03) — должен быть Done или совместим

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "
from core.projection.extraction_policy import build_projection_input_from_draft
from core.domain.contracts import StoryGeoSnapshot
# minimal draft test requires StoryProjectionDraft — defer full test to T06
"
```
