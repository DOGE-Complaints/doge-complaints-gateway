# Story acceptance gate — STORY-GW-SSR-13

- **Story:** Abstract public API (`/node/*`, hard cut `/tallinn/*`)
- **Package:** `pkg-000069-20260829-gw-ssr-13-abstract-node-public-api.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T18:55:15Z

## G13 (runbook §6.4)

Hard cut. No alias. Gate = rg invariants, **not** full URL suite (→ G15). Red gateway pytest on old `/tallinn/` **allowed** until G15 — do not HALT for `test_req24_*` / `test_gw_ssr_05_*` `@app.get("/tallinn/issues")`.

| G13 check | Result | Evidence |
|-----------|--------|----------|
| `rg /tallinn/` empty in `doge-complaints-gateway/src/core/api` | PASS | live rg exit 1 (no matches) |
| five `/node/…` families in `asgi_app.py` + `PUBLIC_ROUTES` | PASS | `:65–67` PUBLIC_ROUTES; GET/POST issues `:462`/`:518`; get by id `:504`; Pulse `:436`; Emerging `:450` |
| three SPA repositories without `/tallinn/` in URL | PASS | `GatewayIssueRepository.js`, `GatewayNetworkPulseRepository.js`, `GatewayEmergingSignalsRepository.js` — live rg empty |
| spa-16 names `GET /node/issues`, not «keep `/tallinn/issues`» | PASS | `16-semantic-schema-spa-compatibility.md:5`, `:24`, `:43` |
| no alias (no second prefix in asgi) | PASS | `rg "/tallinn/` in `asgi_app.py` empty |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Канон: `GET/POST /node/issues`, `GET /node/issues/{issue_id}`, `GET /node/network-pulse`, `GET /node/emerging-signals`. | PASS | `asgi_app.py:421–518` |
| `/tallinn/` отсутствует в `src/core/api`. | PASS | live `rg /tallinn/` empty |
| SPA три репозитория бьют в `/node/…`. | PASS | three Gateway*Repository.js |
| spa-16 и REQ-51 sibling называют `/node/issues`, не город. | PASS | spa-16 `:24`; `51-semantic-schema-runtime.md:5`, `:59` |
| Нет alias. | PASS | no `/tallinn/` registrations in asgi |

## Commands (live verification 2026-08-29T18:55:15Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
rg -n "/tallinn/" doge-complaints-gateway/src/core/api
rg -n "/node/issues|/node/network-pulse|/node/emerging-signals" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "/tallinn/" spa-app/src/repositories/GatewayIssueRepository.js spa-app/src/repositories/GatewayNetworkPulseRepository.js spa-app/src/repositories/GatewayEmergingSignalsRepository.js
rg -n "GET /node/issues|/tallinn/issues" spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md
# Do not HALT G13 if test_req24_* / test_gw_ssr_05_* still assert @app.get("/tallinn/issues")
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

SSR-06/07/11/12/14/15 not started. SSR-01…05 / 08–10 not reopened. Pie T-wave unchanged. bullrun §«Актуальная точка» unchanged. `gateway-mvp-dashboard.md` unchanged. pkg-000069 immutable. spa-app nested git not committed. ClusterLens still 10. `settlement:tallinn` + pack id `tallinn_civic` stay. Gateway pytest URL suite → G15.
