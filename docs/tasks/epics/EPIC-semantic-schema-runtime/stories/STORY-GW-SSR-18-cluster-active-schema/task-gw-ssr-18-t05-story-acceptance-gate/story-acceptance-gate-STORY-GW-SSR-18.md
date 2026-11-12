# Story acceptance gate — STORY-GW-SSR-18

- **Story:** Кластеризация от активной схемы ноды
- **Package:** `pkg-000075-20260830-gw-ssr-18-cluster-active-schema.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T15:06:33Z

## G18 (runbook §6.3)

| G18 check | Result | Evidence |
|-----------|--------|----------|
| mismatch bound → skip (нет pack membership чужим pack.json) | PASS | `test_gw_ssr_18_cluster_active_schema.py` `test_mismatch_bound_skips_without_pack_membership`; `cluster_orchestrator.py:303–307` |
| civic unlabeled engine зелёный | PASS | `tests/test_clustering_engine.py` |
| полный offline pytest зелёный | PASS | 767 passed, 18 skipped, 10 deselected (`-m "not live_integration"`) |
| мануал **не** учит «клиент выбирает любой pack» / «решает тело intake» | PASS | `rg` empty; учит склад vs `NODE_SCHEMA_*` и 4xx |
| `ClusterLens` members **ровно** baseline (10) | PASS | `src/core/cluster/types.py:10–22` |
| нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions` | PASS | `rg` `src/core/api/asgi_app.py` empty |
| не `live_integration` как proof | PASS | marker `not live_integration` |
| GPT UI files не в diff | PASS | `git diff --name-only` — no GPT UI paths |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Bound ≠ активная пара → нет pack membership / не чужой pack.json. | PASS | skip + log; G18 mismatch tests |
| Bound == активная → exact-lenses **этого** pack (dual если pack.json true). | PASS | match test; dual via `dual_civic_lenses_for_ref` |
| Unbound legacy → civic path; `ClusterLens` 10. | PASS | `_civic_ready`; types.py 10 members |
| Мануал: склад vs `NODE_SCHEMA_*`; intake 4xx; кластеризация с сервера. | PASS | `schema-packs-node-data-model-ru.md` |
| Smoke docs: binding в payload = env процесса. | PASS | `test-matrix-by-type-layer-mocks.md` |

## Commands (live verification 2026-08-30T15:06:33Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
GATEWAY_URL= .venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_18_*.py
GATEWAY_URL= .venv/bin/python -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
GATEWAY_URL= .venv/bin/python -m pytest -q -m "not live_integration"
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "клиент выбирает любой pack|решает тело intake" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
