# run-summary — GW-SSR-27 P3 Execute

- **Date:** 2026-09-01T13:21:04Z
- **Package:** pkg-000084-20260901-gw-ssr-27-geo-precision-instance-territory.yaml
- **Story:** STORY-GW-SSR-27 geo precision + instance territory
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000084-20260901-gw-ssr-27-geo-precision-instance-territory.yaml
- **Result:** PASS (T00–T07 Done; story gate G27 PASS)

## G27

README `geo_model` + `gpt_instance_territory` + three-level geo; types + loader; `detail_level` wire→snapshot→DB→Issue.geo (UC-G03 without inventing coords); tallinn Option B settlement `admin_token`; tests `test_gw_ssr_27_*` **10 passed**; SSR-22 **3 passed**; ClusterLens=10; manual §три уровня geo.

## Queue executed

T00 README → T01 types → T02 loader → T03 wire/persist → T04 projection → T05 tests → T06 manual → T07 story acceptance gate.

## Live verification

```text
ok 8 paths (project=gateway, pkg …/pkg-000084-…)
ok date-check
utc_now: 2026-09-01T13:21:04Z
pytest -q tests/test_gw_ssr_27_*.py → 10 passed
pytest -q tests/test_gw_ssr_22_*.py → 3 passed
combined SSR-22+23+24+26+27 → 41 passed
ClusterLens → 10
```

## Product claims (code)

- Types — `src/core/schema/contracts.py` `GEO_PRECISION_LEVELS` / `GeoModelBlock` / `GptInstanceTerritory*` / SchemaContext fields
- Loader — `src/core/schema/resolver.py` `_parse_geo_model` / `_parse_gpt_instance_territory`
- Wire — `intake/contracts.py` `detail_level`; `domain/contracts.py` `StoryGeoSnapshot.detail_level`; `geo/intake_merge.py`
- Persist — sqlite/supabase `geo_detail_level` + migration `20260901_1315_gw_ssr_27_stories_geo_detail_level.sql` (omit-probe; SSR-24 column set unchanged)
- Projection — `ProjectionInput.geo_detail_level`; mapper UC-G03 partial geo
- Tallinn seed — `geo_model` + Option B `gpt_instance_territory` admin_token settlement tallinn
- Docs — `schema-packs/README.md`; `schema-packs-node-data-model-ru.md` §три уровня
- Tests — `tests/test_gw_ssr_27_geo_precision.py`
- Not touched: ClusterLens still 10; no invent coords; no HTTP geo-filter; no street/house on Issue; §Актуальная точка not rewritten; pkg-000084 YAML immutable; push=no; do not start 28/29

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-28/29 in this pkg.
