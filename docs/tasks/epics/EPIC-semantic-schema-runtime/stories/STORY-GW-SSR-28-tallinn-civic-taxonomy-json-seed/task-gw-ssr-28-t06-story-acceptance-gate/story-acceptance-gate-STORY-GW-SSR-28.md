# Story acceptance gate — STORY-GW-SSR-28

- **Story:** tallinn_civic/v1 taxonomy.json seed
- **Package:** `pkg-000085-20260901-gw-ssr-28-tallinn-civic-taxonomy-json-seed.yaml`
- **Result:** PASS
- **Date:** 2026-09-01T13:35:45Z

## AC checklist (verbatim from backlog)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR28-01: `taxonomy.json` under `tallinn_civic/v1/` | PASS | `schema-packs/tallinn_civic/v1/taxonomy.json` · 13 axes · 182 keys · trailing newline |
| AC-GW-SSR28-02: `pack.json` `"taxonomy_schema": "taxonomy.json"` | PASS | tallinn only; legal/mobility unchanged |
| AC-GW-SSR28-03: 13 axes lockstep `TAXONOMY_AXIS_VALUES` | PASS | `test_taxonomy_axes_lockstep_thirteen` |
| AC-GW-SSR28-04: `axis_to_signal_map` covers required `signals.*` | PASS | `test_required_signals_covered_by_axis_to_signal_map` |
| AC-GW-SSR28-05: keys match GPT §4/§5/§6 extract (no invent) | PASS | `tests/helpers/ssr28_gpt_taxonomy_extract.py` + `test_canonical_keys_inventory_matches_gpt_md_section_four` |
| AC-GW-SSR28-06: `resolve_pack(tallinn_civic/v1)` loads taxonomy | PASS | `test_tallinn_resolve_requires_taxonomy_pack` |

## Commands (live verification — P3 only)

```text
--verify ok 6 (pkg-000085) + ok date-check
utc_now: 2026-09-01T13:35:45Z
pytest -q tests/test_gw_ssr_28_*.py → 7 passed
pytest -q tests/test_gw_ssr_26_*.py → 7 passed
pytest -q tests/test_gw_ssr_28_*.py tests/test_gw_ssr_26_*.py tests/test_gw_ssr_01_*.py → 35 passed
ClusterLens → 10
legal/mobility taxonomy is None
§Актуальная точка not rewritten; no GPT UI edit; no push
```
