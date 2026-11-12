# acceptance-verification — GW-SSR-10 t00

- **Result:** PASS
- **Date:** 2026-08-29T18:31:19Z
- **Package:** pkg-000068

## Evidence

Loader key `dual_civic_lenses` (boolean, optional) on `SchemaContext` (`contracts.py`) parsed in `resolver.py` `_parse_dual_civic_lenses`. Absent/`false` = exact-only. `legal_process/v1/pack.json` and `tallinn_civic/v1/pack.json` have no key. Documented in `schema-packs/README.md`. Tests: `tests/test_gw_ssr_10_dual_pack_flag.py`.

## Commands

```bash
rg -n "exact_lenses|dual" doge-complaints-gateway/src/core/schema/resolver.py \
  doge-complaints-gateway/src/core/schema/contracts.py
rg -n "dual|civic-lens" doge-complaints-gateway/schema-packs/README.md
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_10_dual_pack_flag.py
```
