# STORY-GW-SSR-20 — Node clustering runtime from active pack

## Meta
- **Key:** `STORY-GW-SSR-20-node-clustering-runtime-wire`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — cluster-knobs wave (sequence **20**)
- **Тип:** implement (factory + AppConfig cleanup + tests)
- **Parent REQ:** 51 CL; INDEX **D-SSR-9**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [cluster-knobs Шаг 0](./orchestrator-cluster-knobs-runbook.md)
- **Зависит от:** SSR-19

## Зачем простыми словами

Контракт уже в pack (SSR-19). Civic engine и promote должны читать knobs из **активного** pack (`NODE_SCHEMA_*`), а не из `.env`. Cron остаётся процессом в env. Семантические `CLUSTER_*` убрать из required AppConfig — один источник правды.

## Scope / Out of scope

**In:** [`service_factory.py`](../../../../src/core/infrastructure/service_factory.py) `get_clustering_engine` (`:93–104`), civic `PromotionGatePolicy` (`:110–113`), orchestrator `cluster_min_size` / `cluster_min_size_by_lens` (`:158–159`) — из `resolve_pack` активного `(node_schema_id, node_schema_version)` → `node_clustering.civic`. [`handlers.py`](../../../../src/core/api/handlers.py) `geo_scope` (`:253`) — из того же pack, не `config.cluster_geo_scope`. Boot: missing/битый `node_clustering` на активном pack → **`ConfigError`** (fail-fast как SSR-16). AppConfig / `ENV_SCHEMA`: **убрать** семантические `CLUSTER_MIN_SIZE`, `CLUSTER_MIN_SIZE_BY_LENS`, `CLUSTER_READINESS_THRESHOLD`, `CLUSTER_ACTIVE_LENSES`, `CLUSTER_PRIMARY_LENS`, `CLUSTER_SIGNAL_SOURCE`, `CLUSTER_ID_ALGORITHM`, `CLUSTER_GEO_FILTER`, `CLUSTER_GEO_SCOPE`, `CLUSTER_TIE_BREAKER`, `CLUSTER_TYPE_RESOLUTION` (и соответствующие поля dataclass). **Оставить:** `CLUSTER_CRON_ENABLED`, `CLUSTER_CRON_INTERVAL_S` + `NODE_SCHEMA_*`. Lifespan лог: lenses/min_size/geo из pack, cron из env ([`asgi_app.py`](../../../../src/core/api/asgi_app.py)). Pytest: `conftest` без monkeypatch семантических CLUSTER_*; `test_config_loading` / `test_cluster_active_lenses_runtime_effect` / config env contracts переписать; civic `test_clustering_engine.py` зелёный; dual path; missing env `CLUSTER_MIN_SIZE` больше не ConfigError.

**Out:** GPT UI; IDX; смена семантики `exact_lenses`; invent env override поверх pack; удаление `ClusterLens`; глубокий мануал (→21, кроме точечных правок `.env.test.example` если нужны для boot).

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-20 pkg-000077):** civic engine / gate / orchestrator min from active pack `node_clustering.civic` | [`service_factory.py:95–121,157–168`](../../../../src/core/infrastructure/service_factory.py) `_active_civic` |
| **As-of-Done:** handlers `geo_scope` from pack civic | [`handlers.py:254–257`](../../../../src/core/api/handlers.py) |
| **As-of-Done:** semantic `CLUSTER_*` gone from AppConfig; `CLUSTER_CRON_*` + `NODE_SCHEMA_*` stay | [`schema.py:37–56`](../../../../src/core/config/schema.py) |
| **As-of-Done:** lifespan logs pack knobs + cron env; `min_size_guard=civic.min_size` | [`asgi_app.py:121–149,175–194`](../../../../src/core/api/asgi_app.py) |
| **As-of-Done:** `ClusterLens` = 10; missing civic → ConfigError | [`types.py:10–22`](../../../../src/core/cluster/types.py); `civic_clustering_from_active_node` |
| **Historical (pre-SSR-20):** Engine / civic gate / orchestrator min / geo из AppConfig `cluster_*`; handlers `dependencies.config.cluster_geo_scope` | same paths pre-P3 |

## Стыковка

Не silent coerce: если env всё ещё задаёт старые `CLUSTER_MIN_SIZE` — после удаления из ENV_SCHEMA они **игнорируются OS** (не в AppConfig). Не держать dual-source «env wins». Не менять default civic `require_actionable_canonical_type=True` на factory policy type — только числа `min_readiness_score` / `min_stories` из pack civic block.

Unbound legacy + dual используют **один** civic engine, собранный из активного pack (D-SSR-8/9: одна нода — одна модель).

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Factory | Engine + civic gate + orchestrator min из active pack | Env override |
| **T02** | Handlers | geo_scope из pack | Новый HTTP path |
| **T03** | Config | Убрать семантические CLUSTER_* из AppConfig/ENV_SCHEMA; cron stay | Удалить CLUSTER_CRON_* |
| **T04** | Lifespan | Лог pack knobs + cron env | Dump payload |
| **T05** | Tests | conftest; config; clustering; active lenses effect; suite green | live_integration proof |
| **T06** | Gate | no required CLUSTER_MIN_SIZE; civic unlabeled green; ClusterLens=10 | |

## Target / AC

- [x] Civic `ClusteringEngine` knobs = `node_clustering.civic` активного pack.
- [x] Civic `PromotionGatePolicy` min_readiness / min_stories из pack.
- [x] Orchestrator min_size / by_lens из pack.
- [x] Handlers geo_scope из pack.
- [x] Семантические `CLUSTER_*` не в AppConfig; cron + NODE_SCHEMA остаются.
- [x] Missing `node_clustering` на активном pack → ConfigError при boot/load.
- [x] `test_clustering_engine.py` + offline suite зелёные после адаптации фикстур.
- [x] `ClusterLens` = 10.

## Dependencies

- SSR-19. Docs inventory — SSR-21.
