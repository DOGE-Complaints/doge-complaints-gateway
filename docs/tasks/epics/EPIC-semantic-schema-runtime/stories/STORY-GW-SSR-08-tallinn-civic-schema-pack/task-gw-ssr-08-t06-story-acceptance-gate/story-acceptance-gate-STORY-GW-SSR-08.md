# Story acceptance gate — STORY-GW-SSR-08

- **Story:** Tallinn civic model as schema pack
- **Package:** `pkg-000066-20260829-gw-ssr-08-tallinn-civic-schema-pack.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T17:52:54Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Pack `tallinn_civic/v1` резолвится loader’ом (`SCHEMA_PACKS_ROOT` / default). | PASS | `schema-packs/tallinn_civic/v1/pack.json`; `tests/test_gw_ssr_08_pack_load_membership.py::test_tallinn_civic_pack_resolves` |
| JSON Schema покрывает map SignalDimension/label keys → dotted paths (таблица выше). | PASS | `payload.schema.json` properties `signals.*` + `geo.district`; `test_json_schema_covers_map_dotted_paths` |
| Exact membership для bound stories с этим pack; `cluster_memberships.lens` = pack `lens_id`. | PASS | `test_two_stories_same_payload_share_cluster_id`; composite two `source_fields`; `lens` = `civic_domain_micro` |
| Civic stories без binding: тесты зелёные; `ClusterLens` по-прежнему 10 членов. | PASS | G8 civic slice + `test_clusterlens_still_ten_civic_members`; `types.py:10–22` 10 members |
| Pack promote использует knobs файла пака; factory civic default не изменён. | PASS | pack file 35/3/false; `test_readiness_knobs_come_from_pack_file_not_civic_defaults`; `gates.py:14` True; factory `service_factory.py:108` |
| Пример `schema_binding` envelope в репозитории gateway (не GPT UI). | PASS | fixture `tests/fixtures/gw_ssr_08_tallinn_civic_envelope.json`; manual `schema-packs-node-data-model-ru.md`; `test_gw_ssr_08_envelope_example.py` |
| Нет: migrate civic rows; новый HTTP; `story_dimensions`; IDX/processor delivery. | PASS | `asgi_app.py` no `story_dimensions`/`/schema-filter`; `runtime.py` `build_index`/`project` stubs; civic unbound tests green |

## Commands (live verification 2026-08-29T17:52:54Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_08_pack_load_membership.py \
  tests/test_gw_ssr_08_civic_unbound_regression.py \
  tests/test_gw_ssr_08_envelope_example.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py
# → 36 passed
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
# → 10 members
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
# → no matches
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
# → 14:    require_actionable_canonical_type: bool = True
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

SSR-09 hosted apply / packs in image not started. SSR-06/07/12 not started. Pie T-wave unchanged.
