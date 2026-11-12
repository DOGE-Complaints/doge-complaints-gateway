# Story acceptance gate — STORY-GW-SSR-19

- **Story:** Node clustering pack contract
- **Package:** `pkg-000076-20260830-gw-ssr-19-node-clustering-pack-contract.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T19:21:58Z

## G19 (runbook §6.1)

| G19 check | Result | Evidence |
|-----------|--------|----------|
| pytest 19 зелёный | PASS | `tests/test_gw_ssr_19_node_clustering_pack_contract.py` — 5 passed (`-m "not live_integration"`) |
| три pack с блоком | PASS | `schema-packs/{tallinn_civic,legal_process,mobility_observation}/v1/pack.json` `node_clustering` |
| README ключ | PASS | `schema-packs/README.md:30` + `:60` |
| ClusterLens=10 | PASS | `src/core/cluster/types.py:10–22` |
| factory ещё читает AppConfig CLUSTER_* | PASS | `src/core/infrastructure/service_factory.py:93–113` |
| не `live_integration` как proof | PASS | marker `not live_integration` |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `node_clustering.civic` парсится в SchemaContext. | PASS | `contracts.py` + `resolver.py` `_parse_civic_clustering`; load-ok test |
| Нет блока / битый primary → loader error. | PASS | `UnsupportedVersionError`; missing / invalid-primary tests |
| Три example pack на диске с заполненным блоком (tallinn: `geo_scope=settlement:tallinn`). | PASS | three packs; tallinn JSON `settlement:tallinn` |
| `schema-packs/README.md` документирует ключ. | PASS | README table + subsection |
| `ClusterLens` members ровно baseline (10). | PASS | `types.py:10–22`; `test_clusterlens_still_ten_members` |
| Factory/AppConfig **не** переведены на pack в этой стори. | PASS | factory still `self.config.cluster_*`; EnvSpec CLUSTER_* intact |

## Commands (live verification 2026-08-30T19:21:58Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
GATEWAY_URL= .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_19_node_clustering_pack_contract.py
rg -n "node_clustering" schema-packs/README.md src/core/schema/
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "node_clustering" schema-packs/tallinn_civic/v1/pack.json schema-packs/legal_process/v1/pack.json schema-packs/mobility_observation/v1/pack.json
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
