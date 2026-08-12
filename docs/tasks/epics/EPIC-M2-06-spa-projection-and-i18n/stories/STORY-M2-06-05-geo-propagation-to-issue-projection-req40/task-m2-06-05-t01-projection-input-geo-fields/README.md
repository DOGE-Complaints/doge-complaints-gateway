## Task workspace — `task-m2-06-05-t01-projection-input-geo-fields`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §4.1; GAP-40-01

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~30–45 min  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: implement — `ProjectionInput` geo fields

### Цель
Добавить 7 опциональных geo-полей в `ProjectionInput` для передачи snapshot доминантной истории в projection engine.

### Факты из кода
1. [`projection/input.py`](../../../../../../../src/core/projection/input.py) L9–23 — `ProjectionInput` без `geo_lat` / `geo_lon` / admin fields.
2. REQ-40 §4.1 — поля: `geo_lat`, `geo_lon`, `geo_normalized_label`, `geo_admin_district`, `geo_admin_settlement`, `geo_admin_region`, `geo_admin_country` (все `| None = None`).
3. [`StoryGeoSnapshot`](../../../../../../../src/core/domain/contracts.py) L28–40 — источник значений на story-уровне.

### Gap / Проблема
**GAP-40-01:** projection input layer не несёт geo; downstream mapper/DTO не могут сериализовать geo в payload.

### AC/DoD
- [ ] (P0) Все 7 полей добавлены в `ProjectionInput` с defaults `None`.
- [ ] (P0) Frozen dataclass остаётся валидным; существующие call sites компилируются (kwargs optional).
- [ ] (P1) Нет изменений в mapper/dto в этом таске (T02–T03).

### Где менять код
- [`src/core/projection/input.py`](../../../../../../../src/core/projection/input.py)

### Out of scope
- `DOGEIssue`, mapper, bridge (T02–T05)
- Tests (T06)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "from core.projection.input import ProjectionInput; import inspect; f=[x.name for x in ProjectionInput.__dataclass_fields__.values()]; assert 'geo_lat' in f"
```
