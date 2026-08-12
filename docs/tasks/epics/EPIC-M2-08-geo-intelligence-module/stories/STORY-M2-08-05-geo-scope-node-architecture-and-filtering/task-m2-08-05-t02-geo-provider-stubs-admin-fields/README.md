## Task workspace — `task-m2-08-05-t02-geo-provider-stubs-admin-fields`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §3.1; G-02

## Task: implement — demo geo stubs with admin levels

### Цель
Обновить `_TallinnOpenCageStub` и `_NarvaNominatimStub` так, чтобы они возвращали захардкоженные `admin_*` значения для demo (post-demo: real provider mapping).

### Факты из кода
1. [`src/core/geo/providers.py`](../../../../../../../src/core/geo/providers.py) L24–32 — Tallinn stub: `cluster_tags=("place:tallinn", "country:ee")`, без admin-полей.
2. [`src/core/geo/providers.py`](../../../../../../../src/core/geo/providers.py) L43–51 — Narva stub: `cluster_tags=("place:narva", "country:ee")`.
3. REQ-35 §3.1 — для demo достаточно стабов с фиксированными admin-уровнями (пример: Tallinn / Narva / EE).

### Gap / Проблема
GAP-35-06: стабы не заполняют admin-поля → T04/T05/T06 не могут быть проверены end-to-end.

### AC/DoD
- [x] (P0) Tallinn resolve возвращает `admin_settlement` (напр. `tallinn` или `Tallinn`), `admin_country=EE`, опционально `admin_region`.
- [x] (P0) Narva resolve возвращает `admin_settlement` для Narva, `admin_country=EE`.
- [x] (P1) Существующие `cluster_tags` сохранены для backward compatibility.

### Где менять код
- [`src/core/geo/providers.py`](../../../../../../../src/core/geo/providers.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_geo_service.py -q --tb=short -k stub 2>/dev/null || python3 -m pytest tests/ -q --tb=short -k geo -x
```
