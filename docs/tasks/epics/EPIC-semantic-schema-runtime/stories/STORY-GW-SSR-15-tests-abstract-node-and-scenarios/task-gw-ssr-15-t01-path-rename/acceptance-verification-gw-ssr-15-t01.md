# acceptance-verification — GW-SSR-15 t01

- **Result:** PASS
- **Date:** 2026-08-29T19:47:15Z
- **Package:** pkg-000072

## Evidence

HTTP asserts in gateway `tests/` now use `/node/…`. Renamed `test_req24_tallinn_issues_read_api.py` → `test_req24_issues_read_api.py`. SSR-05/09 `@app.get` asserts → `/node/issues`. SSR-11 hard-cut `assert "/tallinn/issues" not in` asgi kept. Geo `settlement:tallinn` / `admin_settlement` untouched.

## Commands

```bash
rg -n 'client\.(get|post)\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
# only T05 leftover after t05
rg -n '@app.get\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
# empty
ls doge-complaints-gateway/tests/test_req24_issues_read_api.py
```
