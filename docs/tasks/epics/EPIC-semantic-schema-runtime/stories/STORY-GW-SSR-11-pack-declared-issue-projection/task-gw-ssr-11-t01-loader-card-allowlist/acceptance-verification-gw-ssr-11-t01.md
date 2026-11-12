# acceptance-verification — GW-SSR-11 t01

- **Result:** PASS
- **Date:** 2026-08-29T19:13:51Z
- **Package:** pkg-000070

## Evidence

`resolver.py` `_parse_card_fields` reads `pack.json` `card_fields`. Absent/`null`/`[]` → `SchemaContext.card_fields == ()`. `legal_process/v1` and `tallinn_civic/v1` have no key. Tests: `tests/test_gw_ssr_11_card_fields_loader.py`.

## Commands

```bash
rg -n "card_fields|_parse_card_fields" doge-complaints-gateway/src/core/schema/resolver.py
test -f doge-complaints-gateway/schema-packs/legal_process/v1/pack.json
test -f doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_11_card_fields_loader.py
```
