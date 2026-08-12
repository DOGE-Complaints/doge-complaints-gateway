# acceptance-verification — GW-ES-03 T03

- **Result:** PASS
- **Date:** 2026-08-10T12:17:38Z
- **Package:** pkg-000060

## Evidence

| Check | Evidence |
|-------|----------|
| Path from REQ-50 | `GET /tallinn/emerging-signals` in `asgi_app.py` |
| PUBLIC_ROUTES | `/tallinn/emerging-signals` listed |
| OPTIONS CORS | `@app.options("/tallinn/emerging-signals")` |
| HTTP smoke | `test_gw_es_03_public_get_without_auth_returns_200` |

## Commands

```bash
rg -n 'emerging-signals' doge-complaints-gateway/src/core/api/asgi_app.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_es_03_emerging_signals.py::test_gw_es_03_public_get_without_auth_returns_200
```
