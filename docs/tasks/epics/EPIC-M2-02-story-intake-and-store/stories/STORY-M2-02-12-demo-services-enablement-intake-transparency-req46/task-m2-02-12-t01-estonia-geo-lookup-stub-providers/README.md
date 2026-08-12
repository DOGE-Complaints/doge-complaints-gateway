## Task workspace — `task-m2-02-12-t01-estonia-geo-lookup-stub-providers`

- Story: [`../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md`](../STORY-M2-02-12-demo-services-enablement-intake-transparency-req46.md)
- Decision Ref: [`../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md`](../../../../../../requirements/46-demo-services-enablement-and-response-transparency.md) §2.1, §4 Geo expansion

---
**Priority:** P1  
**Complexity:** M  
**Estimate:** ~2 h  
**Status:** ready  
**Wave:** `pkg-000026`  
---

## Task: implement — Estonia geo lookup stub (EN/ET/RU + districts)

### Цель
Заменить узкий demo stub (2 города, только EN substring) на `_EstoniaGeoLookup` с dict alias → `StoryGeoSnapshot` для топ-10 городов EE + 9 районов Таллинна.

### Почему это важно (риск)
`"Таллин"` → `"таллин"` не матчит `"tallinn"` ([`providers.py`](../../../../../../../src/core/geo/providers.py) L23–24) → пустые `geo_*` при живом geo-сервисе (REQ §1.1).

### Факты из кода
1. [`src/core/geo/providers.py`](../../../../../../../src/core/geo/providers.py) L17–64 — `_TallinnOpenCageStub`, `_NarvaNominatimStub`; `default_provider_chain()` returns both.
2. REQ §2.1 — таблица alias (EN/ET/RU) и архитектура `_GEO_LOOKUP` + `_EstoniaGeoLookup`.

### Gap / Проблема
Demo intake не резолвит RU/ET написания и районы → GPT видит пустой geo без сигнала в API (до T03–T06).

### AC/DoD (source-of-truth: REQ-46 §4 Geo)
- [ ] (P0) `location_query = "Таллин"` → `geo_admin_settlement = "tallinn"`, `geo_admin_country = "EE"`.
- [ ] (P0) `location_query = "Kalamaja"` → `geo_admin_district = "kalamaja"`, `geo_admin_settlement = "tallinn"`.
- [ ] (P0) `location_query = "Tartu"` / `"Тарту"` → `geo_admin_settlement = "tartu"`.
- [ ] (P0) `location_query = "Нарва"` → `geo_admin_settlement = "narva"`.
- [ ] (P0) Пустой/отсутствующий `location_query` → `geo_*` null, без ошибок.
- [ ] (P1) Unit tests для alias matrix (минимум кейсы из REQ §4).

### Где менять код
- [`src/core/geo/providers.py`](../../../../../../../src/core/geo/providers.py)
- Новый/расширенный test module под geo providers (координация с T06).

### Out of scope
- Real OpenCage/Nominatim adapters (REQ §5 backlog).
- `intake_notes` / logging (T02–T04).
- REQ-47 GPT payload changes.

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/ -k geo -k estonia 2>/dev/null || python3 -m pytest -q tests/test_geo_providers.py
```
