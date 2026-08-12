## Task workspace — `task-m2-08-05-t04-config-cluster-geo-scope-and-filter`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §3.2–3.3; G-02; D-03 (example.env)

## Task: implement — CLUSTER_GEO_SCOPE env and filter validation

### Цель
Добавить `CLUSTER_GEO_SCOPE` (`<level>:<value>`) в `ENV_SCHEMA` / `AppConfig`; валидировать `CLUSTER_GEO_FILTER` ∈ `{district,settlement,region,country}` с дефолтом `country`; документировать обе переменные в `example.env`.

### Факты из кода
1. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) L184–188 — `CLUSTER_GEO_FILTER` default `"any"`, description без enum.
2. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) L505, L540 — значение читается в `AppConfig.cluster_geo_filter` без parse helper.
3. `rg CLUSTER_GEO_SCOPE` по `src/` — 0 совпадений (GAP-35-03).
4. REQ-35 §3.2 — дефолт filter = `country`; G-02 L187 согласован.

### Gap / Проблема
GAP-35-03, GAP-35-04: нет scope env; filter default не соответствует продуктовому решению.

### AC/DoD
- [x] (P0) `CLUSTER_GEO_SCOPE` optional; parse `level:value`; invalid format → `ConfigError`.
- [x] (P0) `CLUSTER_GEO_FILTER` parse: `district|settlement|region|country`; default `country` (убрать или alias `any` → `country` с явной документацией).
- [x] (P0) `AppConfig` exposes `cluster_geo_scope: tuple[str, str] | None` (или typed struct).
- [x] (P1) [`example.env`](../../../../../../../example.env) документирует обе переменные с комментариями REQ-35.
- [x] (P1) `tests/test_config_loading.py` покрывает valid/invalid combinations.

### Где менять код
- [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py)
- [`example.env`](../../../../../../../example.env)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q --tb=short -k geo
```
