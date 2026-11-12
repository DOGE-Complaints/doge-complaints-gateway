# Story acceptance gate — STORY-GW-SSR-24

- **Story:** persist normalized geo (address depth)
- **Package:** `pkg-000081-20260830-gw-ssr-24-geo-detail-persist.yaml`
- **Result:** PASS
- **Date:** 2026-08-30T21:00:56Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Street / house_range / houses / coords persist на story. | PASS | `db_sqlite.py` + `test_sqlite_roundtrip_*` |
| Lifecycle advance не стирает новые geo fields. | PASS | `test_advance_preserves_geo_depth` |
| Binding/geo новые cols не в `required_columns_ready`. | PASS | `test_required_columns_ready_omits_geo_detail` |
| Mirror в payload когда `mirror_to_payload`. | PASS | `mirror_geo_to_payload`; `test_mirror_payload_from_snapshot_depth` |
| Migration SQL на диске. | PASS | `supabase/migrations/20260830_2100_gw_ssr_24_stories_geo_detail.sql` |

## G24 (runbook §6.3)

| G24 check | Result | Evidence |
|-----------|--------|----------|
| round-trip street/range/houses/coords | PASS | `test_gw_ssr_24_geo_detail_persist.py` |
| new cols не в required_columns_ready | PASS | omit-probe + inspect source |
| migration на диске | PASS | `20260830_2100_gw_ssr_24_stories_geo_detail.sql` |
| полный offline pytest зелёный | PASS | **801 passed**, 18 skipped, 10 deselected |
| ClusterLens=10 | PASS | `test_clusterlens_still_ten_members`; `types.py:10–22` |

## Commands (live verification — P3)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway
.venv/bin/python3.11 -m pytest -q -m "not live_integration" tests/test_gw_ssr_24_*.py
.venv/bin/python3.11 -m pytest -q -m "not live_integration" tests/test_stories_schema_cross_layer_invariant.py
.venv/bin/python3.11 -m pytest -q -m "not live_integration"
# 801 passed, 18 skipped, 10 deselected 2026-08-30T21:00:56Z
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
