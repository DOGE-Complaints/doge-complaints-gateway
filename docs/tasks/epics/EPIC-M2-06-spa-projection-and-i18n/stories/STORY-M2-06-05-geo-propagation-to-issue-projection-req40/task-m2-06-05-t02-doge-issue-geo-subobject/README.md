## Task workspace — `task-m2-06-05-t02-doge-issue-geo-subobject`

- Story: [`../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md`](../STORY-M2-06-05-geo-propagation-to-issue-projection-req40.md)
- Decision Ref: [`../../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../../requirements/40-geo-propagation-to-issue-projection.md) §4.2; GAP-40-02

---
**Приоритет:** P2  
**Сложность:** S  
**Оценка времени:** ~30–45 min  
**Статус:** ready  
**Wave:** `pkg-000018`  
---

## Task: implement — `DOGEIssue.geo` and `to_public_dict()`

### Цель
Добавить поле `geo: dict[str, object] | None` в `DOGEIssue` и сериализовать вложенный `"geo"` только когда geo не `None`.

### Факты из кода
1. [`projection/dto.py`](../../../../../../../src/core/projection/dto.py) L8–45 — `DOGEIssue` без `geo`; `to_public_dict()` не добавляет ключ `geo`.
2. REQ-40 §3.2 — shape: `lat`, `lon`, optional `label`, `district`, `settlement`, `region`, `country`.
3. REQ-40 AC-2 — при отсутствии geo ключ **не включается** (не `null`).

### Gap / Проблема
**GAP-40-02:** SPA payload из projection DTO не содержит geo sub-object для read API / REQ-24.

### AC/DoD
- [ ] (P0) `DOGEIssue` + поле `geo: dict[str, object] | None = None`.
- [ ] (P0) `to_public_dict()`: `if self.geo is not None: out["geo"] = self.geo`.
- [ ] (P0) При `geo is None` ключ `"geo"` отсутствует в `out`.
- [ ] (P1) Mapper wiring — T03.

### Где менять код
- [`src/core/projection/dto.py`](../../../../../../../src/core/projection/dto.py)

### Out of scope
- Building geo dict from `ProjectionInput` (T03)
- Bridge / dominant story (T05)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -c "
from core.projection.dto import DOGEIssue
d = DOGEIssue(id='i', status='PUBLISHED', type='INCIDENT', labels=(), title={'et':'t'}, summary={'et':'s'}, description={'et':'d'}, geo={'lat':1.0,'lon':2.0})
assert 'geo' in d.to_public_dict()
d2 = DOGEIssue(id='i', status='PUBLISHED', type='INCIDENT', labels=(), title={'et':'t'}, summary={'et':'s'}, description={'et':'d'})
assert 'geo' not in d2.to_public_dict()
"
```
