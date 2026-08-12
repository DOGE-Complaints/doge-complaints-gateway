## Task workspace — `task-m2-08-05-t05-cluster-engine-geo-filter`

- Story: [`../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md`](../STORY-M2-08-05-geo-scope-node-architecture-and-filtering.md)
- Decision Ref: REQ-35 §3.2; SA cluster-engine/03

## Task: implement — CLUSTER_GEO_FILTER in clustering engine

### Цель
Реализовать фильтрацию историй при формировании кластера по admin-полю, соответствующему `CLUSTER_GEO_FILTER`; истории с `geo=None` не фильтруются (geo-агностичные).

### Факты из кода
1. [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py) L165 — `ClusteringEngineParams.geo_filter: str = "any"` — поле есть, логики нет (`rg self.geo_filter` / `params.geo_filter` в `src/` — 0).
2. [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) L83 — `geo_filter=self.config.cluster_geo_filter` передаётся в engine params.
3. REQ-35 §3.2 — при `settlement` Tallinn и Narva не в одном кластере; при `country` — вместе (EE).

### Gap / Проблема
GAP-35-02: config wire exists, clustering ignores geo filter.

### AC/DoD
- [x] (P0) При `CLUSTER_GEO_FILTER=settlement` stories с разным `admin_settlement` не объединяются в один cluster bucket для geo-sensitive lens keys.
- [x] (P0) При `CLUSTER_GEO_FILTER=country` stories с `admin_country=EE` могут кластеризоваться вместе.
- [x] (P0) `geo=None` stories участвуют без geo partition (REQ §3.2).
- [x] (P1) Normalization: compare admin values case-insensitively / slug form (document in code).

### Где менять код
- [`src/core/cluster/engine.py`](../../../../../../../src/core/cluster/engine.py)
- При необходимости: helper в `cluster/types.py` or geo util

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_clustering_engine.py tests/test_story_cluster_orchestrator.py -q --tb=short
```
