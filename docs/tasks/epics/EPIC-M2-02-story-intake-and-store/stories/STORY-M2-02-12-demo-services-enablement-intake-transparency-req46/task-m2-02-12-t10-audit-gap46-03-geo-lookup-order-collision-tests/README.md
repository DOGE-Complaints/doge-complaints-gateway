## Task workspace — `task-m2-02-12-t10-audit-gap46-03-geo-lookup-order-collision-tests`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md`](../../../../../../analysis/audit-req46-demo-services-intake-transparency-2026-06-02.md) §3 G3; REQ-46 §2.1 (district vs city)

---
**Priority:** P2  
**Complexity:** S  
**Estimate:** ~20 min  
**Status:** ready  
**Wave:** audit override (`run_mode=story02_12_audit_req46_followup`)  
---

## Task: tests — geo lookup length-DESC collision (district vs city)

### Цель
Зафиксировать в CI, что `_GEO_LOOKUP_ORDER` (ключи по длине DESC) не регрессирует: `Põhja-Tallinn` → район, чистый `Tallinn` → город без `admin_district`.

### Почему это важно (риск)
Без теста рефактор ordering может снова сопоставить `põhja-tallinn` с ключом `tallinn` и вернуть city snapshot вместо district — пустые/неверные `geo_admin_district` в intake (audit G3).

### Факты из кода
1. [`providers.py`](../../../../../../../src/core/geo/providers.py) L305–320 — `_GEO_LOOKUP_ORDER` sorted by `len` DESC; resolver iterates order.
2. [`providers.py`](../../../../../../../src/core/geo/providers.py) L247–255 — district snapshot `põhja-tallinn` / `pohja-tallinn` / `пыхья-таллин`.
3. [`test_geo_providers_estonia.py`](../../../../../../../tests/test_geo_providers_estonia.py) — есть `Таллин`, `Kalamaja`, `Tartu`; **нет** collision cases.

### Gap / Проблема
**G3 (audit):** отсутствует assert `Põhja-Tallinn` → `admin_district=põhja-tallinn`, `Tallinn` → `admin_settlement=tallinn`, `admin_district is None`.

### AC / DoD
- [ ] (P0) `location_query="Põhja-Tallinn"` (или `põhja-tallinn`) → `geo.admin_district == "põhja-tallinn"`, `geo.admin_settlement == "tallinn"`.
- [ ] (P0) `location_query="Tallinn"` → `geo.admin_settlement == "tallinn"`, `geo.admin_district is None`.
- [ ] (P1) Опционально: RU alias `пыхья-таллин` → district snapshot.
- [ ] (P1) `python3 -m pytest -q tests/test_geo_providers_estonia.py` — green.

### Где менять
- [`tests/test_geo_providers_estonia.py`](../../../../../../../tests/test_geo_providers_estonia.py) (через `StoryIntakeService` + `default_provider_chain()` как существующие кейсы).

### Out of scope
- Изменения [`providers.py`](../../../../../../../src/core/geo/providers.py) unless test reveals bug.
- T08/T09; T01–T07; `pkg-*.yaml`.

### Команды проверки
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_geo_providers_estonia.py
```
