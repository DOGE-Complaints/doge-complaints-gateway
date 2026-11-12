# acceptance-verification — GW-SSR-13 t01

- **Result:** PASS
- **Date:** 2026-08-29T18:55:15Z
- **Package:** pkg-000069

## Evidence

`asgi_app.py` `PUBLIC_ROUTES` `:65–67` lists `/node/issues`, `/node/network-pulse`, `/node/emerging-signals`. OPTIONS/GET/POST wrappers `:421–518` use `/node/…` only. `config/schema.py:127` names `POST /node/issues`. Geo example `:225` `settlement:tallinn` unchanged. No `/tallinn/` route registrations (no alias).

## Commands

```bash
rg -n "/tallinn/|/node/" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "POST /tallinn/issues|POST /node/issues|settlement:tallinn" \
  doge-complaints-gateway/src/core/config/schema.py
```
