## Task workspace — `task-m2-08-05-t06-intake-geo-scope-rejection`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §3.4; G-02 L189

## Task: implement — intake GEO_SCOPE_MISMATCH rejection

### Цель
При заданном `CLUSTER_GEO_SCOPE`: resolve `location_query` через GeoService, сравнить admin-уровень с scope value; mismatch → HTTP 422 с `code: GEO_SCOPE_MISMATCH`. Без `location_query` — intake разрешён.

### Факты из кода
1. [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py) L123+ — `handle_story_intake` вызывает `story_intake_service.create_story`; `has_location_query` логируется L145.
2. [`src/core/geo/service.py`](../../../../../../../src/core/geo/service.py) — `resolve_for_story(location_query)` возвращает `StoryGeoSnapshot | None`.
3. REQ-35 §3.4 — rejection на intake, не на cluster cron.
4. `rg GEO_SCOPE_MISMATCH` — только requirements (GAP-35-05).

### Gap / Проблема
GAP-35-05: нода не может ограничить зону ответственности на intake boundary.

### AC/DoD
- [x] (P0) `CLUSTER_GEO_SCOPE=settlement:tallinn` + Narva `location_query` → HTTP 422, envelope `code=GEO_SCOPE_MISMATCH`.
- [x] (P0) Тот же scope + пустой `location_query` → 200 accepted.
- [x] (P1) Scope не задан → поведение без изменений (accept all).
- [x] (P1) Использовать unified error envelope / trace propagation (EPIC-M2-01-04).

### Где менять код
- [`src/core/api/handlers.py`](../../../../../../../src/core/api/handlers.py)
- Возможно: small helper `core/geo/scope.py` for parse/compare (keep thin)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_http_intake_endpoint.py -q --tb=short -k scope
```
