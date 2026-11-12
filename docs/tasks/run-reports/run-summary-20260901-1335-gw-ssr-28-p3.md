# run-summary — GW-SSR-28 P3 Execute

- **Date:** 2026-09-01T13:35:45Z
- **Package:** pkg-000085-20260901-gw-ssr-28-tallinn-civic-taxonomy-json-seed.yaml
- **Story:** STORY-GW-SSR-28 tallinn_civic taxonomy.json seed
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000085-20260901-gw-ssr-28-tallinn-civic-taxonomy-json-seed.yaml
- **Result:** PASS (T01–T06 Done; story gate G28 PASS)

## G28

Section-scoped GPT §4/§5/§6 extract → `tallinn_civic/v1/taxonomy.json` (13 axes, 182 keys, no invent); `taxonomy_schema` wired in tallinn `pack.json` only; tests `test_gw_ssr_28_*` **7 passed**; SSR-26 **7 passed** (orphan assert moved to tmp_path); ClusterLens=10; handoff note for SSR-29 / GPT-SSR-05 (no GPT UI edit).

## Queue executed

T01 extract helper → T02 compose taxonomy.json → T03 pack manifest → T04 tests → T05 handoff → T06 story acceptance gate.

## Live verification

```text
ok 6 paths (project=gateway, pkg …/pkg-000085-…)
ok date-check
utc_now: 2026-09-01T13:35:45Z
pytest -q tests/test_gw_ssr_28_*.py → 7 passed
pytest -q tests/test_gw_ssr_26_*.py → 7 passed
combined SSR-28+26+01 → 35 passed
ClusterLens → 10
```

## Product claims (code)

- Helper — `tests/helpers/ssr28_gpt_taxonomy_extract.py` (section-scoped; §7 not into canonical_keys)
- Seed — `schema-packs/tallinn_civic/v1/taxonomy.json` regenerated from GPT SSOT
- Manifest — tallinn `pack.json` `"taxonomy_schema": "taxonomy.json"`
- Tests — `tests/test_gw_ssr_28_taxonomy_seed.py` (six story asserts + ClusterLens=10)
- Docs — `schema-packs/README.md` SSR-28 seed / SSR-29 byte-copy handoff
- SSR-26 regress — orphan-without-manifest now tmp_path (tallinn loads taxonomy)
- Not touched: ClusterLens still 10; legal/mobility no taxonomy_schema; no invent vocab; no GPT UI; §Актуальная точка not rewritten; pkg-000085 YAML immutable; push=no; do not start SSR-29 product

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-29 in this pkg.
