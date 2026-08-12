## Task workspace — `task-m2-08-05-t07-tests-req35-acceptance`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §5 (all AC)

## Task: tests — REQ-35 acceptance coverage

### Цель
Закрыть все acceptance criteria REQ-35 §5 автоматическими тестами (unit + HTTP + clustering).

### Факты из кода
1. REQ-35 §5 — шесть чекбоксов AC (snapshot fields, scope 422, scope without geo, filter settlement split, filter country together, stubs).
2. Существующие buckets: `tests/test_http_intake_endpoint.py`, `tests/test_clustering_engine.py`, `tests/test_config_loading.py`.
3. STORY-M2-04-05 T07 pattern — dedicated test module per REQ wave.

### Gap / Проблема
Нет регрессии на geo scope/filter policy — риск повторного drift (как `CLUSTER_GEO_FILTER` declared-but-unused).

### AC/DoD
- [x] (P0) Test: snapshot from stub has `admin_settlement` and `admin_country`.
- [x] (P0) Test: `CLUSTER_GEO_SCOPE=settlement:tallinn` + Narva location → 422 `GEO_SCOPE_MISMATCH`.
- [x] (P0) Test: same scope, no `location_query` → success.
- [x] (P0) Test: `CLUSTER_GEO_FILTER=settlement` → Tallinn vs Narva different cluster ids/keys.
- [x] (P0) Test: `CLUSTER_GEO_FILTER=country` (default) → same-country stories cluster together.
- [x] (P1) `pytest -q` full suite green (no regressions).

### Где менять код
- Новый: `tests/test_req35_geo_scope_and_filter.py` (или split по layer)
- Обновить: `tests/conftest.py` fixtures for geo env if needed

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q --tb=short
cd doge-complaints-gateway && python3 -m pytest -q
```
