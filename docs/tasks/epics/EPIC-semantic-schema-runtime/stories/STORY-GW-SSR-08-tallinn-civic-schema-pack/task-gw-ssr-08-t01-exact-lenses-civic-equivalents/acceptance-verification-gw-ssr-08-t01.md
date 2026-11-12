# acceptance-verification — GW-SSR-08 t01

- **Result:** PASS
- **Date:** 2026-08-29T17:52:54Z
- **Package:** pkg-000066

## Evidence

`exact_lenses` include civic-equivalent `lens_id` strings and `composite_primary_micro` with two `source_fields` (`signals.civic_domain`, `signals.failure_pattern`). No `ClusterLens` / `lens_dimension` edit.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_08_pack_load_membership.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
