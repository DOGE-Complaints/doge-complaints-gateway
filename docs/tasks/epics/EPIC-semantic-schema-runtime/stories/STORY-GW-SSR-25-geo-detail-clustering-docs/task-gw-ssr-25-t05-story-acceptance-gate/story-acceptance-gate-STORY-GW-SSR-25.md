# Story acceptance gate — STORY-GW-SSR-25

- **Story:** geo detail clustering + docs
- **Package:** `pkg-000082-20260830-gw-ssr-25-geo-detail-clustering-docs.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T21:27:05Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Civic clustering зелёный с новым snapshot. | PASS | `tests/test_gw_ssr_25_geo_detail_clustering.py` + `tests/test_clustering_engine.py` |
| Pack exact membership по настроенным `geo.*` lenses. | PASS | tallinn `geo.district` + fixture `geo.street` in `test_gw_ssr_25_*` |
| Мануал: modes, mirror, civic vs exact. | PASS | `docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md` §geo_detail |
| T-wave G3 / closed audits не в diff. | PASS | `orchestrator-t-wave-runbook.md:271` stays `` `GET /tallinn/issues` на месте `` |
| Offline suite / story tests зелёные. | PASS | **811 passed**, 18 skipped, 10 deselected; ClusterLens=10 |

## Commands (live verification — P3 only)

```text
--verify ok 5 (pkg-000082)
utc_now: 2026-08-30T21:27:05Z
pytest -q -m "not live_integration" tests/test_gw_ssr_25_*.py + test_clustering_engine.py → 26 passed
pytest -q -m "not live_integration" → 811 passed, 18 skipped, 10 deselected
rg geo_intake|geo_detail → manual §geo_detail
sed -n '271p' orchestrator-t-wave-runbook.md → GET /tallinn/issues на месте
rg class ClusterLens -A 14 → 10 members
```
