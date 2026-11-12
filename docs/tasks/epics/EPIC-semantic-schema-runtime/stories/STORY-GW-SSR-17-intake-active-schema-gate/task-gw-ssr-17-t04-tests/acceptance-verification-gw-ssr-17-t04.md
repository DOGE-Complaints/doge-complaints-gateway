# acceptance-verification — GW-SSR-17 t04

- **Result:** PASS
- **Date:** 2026-08-30T14:45:34Z
- **Package:** pkg-000074

## Evidence

`tests/test_gw_ssr_17_intake_active_schema.py`: absent/`{}`/null parse 4xx; mismatch id/version 4xx; match persist; HTTP absent 400, mismatch 400, match 202. `tests/test_gw_ssr_03_*.py` civic-absent now reject. Fixtures: `valid_v2_intake_payload` default `active_node_schema_binding()`; `_scenario_to_payload`; req24 posts 3 matching intakes (pack `min_size=3`). G17 live: 22 passed (`test_gw_ssr_17_*` + `test_gw_ssr_03_*`). req24+G17: 45 passed. GPT UI files not in diff.
