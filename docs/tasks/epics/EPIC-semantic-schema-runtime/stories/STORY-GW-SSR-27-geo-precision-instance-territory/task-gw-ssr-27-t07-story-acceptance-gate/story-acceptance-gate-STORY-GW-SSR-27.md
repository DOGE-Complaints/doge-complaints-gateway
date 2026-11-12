# Story acceptance gate — STORY-GW-SSR-27

- **Story:** geo precision + instance territory
- **Package:** `pkg-000084-20260901-gw-ssr-27-geo-precision-instance-territory.yaml`
- **Result:** PASS
- **Date:** 2026-09-01T13:21:04Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR27-01: README documents `geo_model` + `gpt_instance_territory` + node vs instance | PASS | `schema-packs/README.md` keys + three-level section |
| AC-GW-SSR27-02: Loader exposes parsed blocks; absent = optional | PASS | `_parse_geo_model` / `_parse_gpt_instance_territory`; legal/mobility None |
| AC-GW-SSR27-03: `detail_level` wire → snapshot → Issue.geo | PASS | intake + merge + sqlite + mapper UC-G03; tests T03/T04 |
| AC-GW-SSR27-04: `gpt_instance_territory` supports admin_id / admin_token / bbox | PASS | loader rule parse; `GPT_INSTANCE_RULE_TYPES`; tallinn admin_token seed |
| AC-GW-SSR27-05: SSR-22 regression green | PASS | `tests/test_gw_ssr_22_*` **3 passed** |
| AC-GW-SSR27-06: GPT-SSR-08 pack blocks on disk for copy | PASS | tallinn `geo_model` + `gpt_instance_territory`; README examples |

## Commands (live verification — P3 only)

```text
--verify ok 8 (pkg-000084) + ok date-check
utc_now: 2026-09-01T13:21:04Z
pytest -q tests/test_gw_ssr_27_*.py → 10 passed
pytest -q tests/test_gw_ssr_22_*.py → 3 passed
pytest -q tests/test_gw_ssr_23_*.py tests/test_gw_ssr_24_*.py tests/test_gw_ssr_26_*.py (+27+22) → 41 passed combined earlier
ClusterLens → 10
Tallinn Option B: settlement admin_token (no invent district/bbox)
§Актуальная точка not rewritten
```
