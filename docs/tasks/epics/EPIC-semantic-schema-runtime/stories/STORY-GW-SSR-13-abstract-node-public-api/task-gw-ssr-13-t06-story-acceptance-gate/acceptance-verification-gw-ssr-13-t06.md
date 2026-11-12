# acceptance-verification — GW-SSR-13 t06

- **Result:** PASS
- **Date:** 2026-08-29T18:55:15Z
- **Package:** pkg-000069

## Evidence

G13 rg invariants (runbook §6.4) — not full URL pytest suite. `rg /tallinn/` empty in `src/core/api`. Five `/node/…` families in `asgi_app.py` + `PUBLIC_ROUTES`. Three SPA repositories empty of `/tallinn/`. spa-16 names `GET /node/issues`. No alias (no second prefix in asgi). Red `test_req24_*` / `test_gw_ssr_05_*` `@app.get("/tallinn/issues")` not used as HALT (→ G15).

## Commands

```bash
rg -n "/tallinn/" doge-complaints-gateway/src/core/api
rg -n "/node/issues|/node/network-pulse|/node/emerging-signals" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "/tallinn/" spa-app/src/repositories/GatewayIssueRepository.js spa-app/src/repositories/GatewayNetworkPulseRepository.js spa-app/src/repositories/GatewayEmergingSignalsRepository.js
rg -n "GET /node/issues|/tallinn/issues" spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
