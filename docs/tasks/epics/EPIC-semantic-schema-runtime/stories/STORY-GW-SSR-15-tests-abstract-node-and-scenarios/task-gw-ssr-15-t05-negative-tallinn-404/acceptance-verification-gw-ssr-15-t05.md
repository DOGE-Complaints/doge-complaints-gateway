# acceptance-verification — GW-SSR-15 t05

- **Result:** PASS
- **Date:** 2026-08-29T19:47:15Z
- **Package:** pkg-000072

## Evidence

`test_ssr15_legacy_tallinn_issues_is_404` — `GET /tallinn/issues` → 404. No 200/301/302 alias. Sole leftover `client.get("/tallinn/issues")` in tests.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_15_scenarios.py::test_ssr15_legacy_tallinn_issues_is_404
rg -n 'client\.(get|post)\("/tallinn' doge-complaints-gateway/tests --glob '*.py'
```
