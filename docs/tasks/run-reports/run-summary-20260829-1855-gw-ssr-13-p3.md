# run-summary — GW-SSR-13 P3 Execute

- **Date:** 2026-08-29T18:55:15Z
- **Package:** pkg-000069-20260829-gw-ssr-13-abstract-node-public-api.yaml
- **Story:** STORY-GW-SSR-13 abstract `/node/*` public API
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000069-20260829-gw-ssr-13-abstract-node-public-api.yaml
- **Result:** PASS (T01–T06 Done; story gate PASS)

## G13 (runbook §6.4)

Hard cut `/node/*`. No `/tallinn/*` alias. Gate = rg invariants, not full URL pytest (→ G15).

## Queue executed

T01 node public routes → T02 rename tallinn handlers → T03 OpenAPI node paths → T04 SPA Gateway URL clients → T05 sibling REQ paths → T06 story acceptance gate.

## Live verification

```text
ok 6 paths (project=gateway, pkg …/pkg-000069-…)
utc_now: 2026-08-29T18:55:15Z
rg /tallinn/ src/core/api → empty
rg /node/issues|/node/network-pulse|/node/emerging-signals asgi_app.py → five families + PUBLIC_ROUTES
rg /tallinn/ three SPA repositories → empty
spa-16 GET /node/issues (not keep /tallinn/issues)
rg "/tallinn/ asgi_app.py → empty (no alias)
ok date-check (after this file)
```

## Product claims (code)

- Routes: `asgi_app.py` PUBLIC_ROUTES `:65–67`; OPTIONS/GET/POST `/node/…` `:421–518`
- Handlers: `handlers.py` `handle_issues_list` / `handle_issue_get` / `handle_issue_create`; Pulse/Emerging names unchanged
- Config: `schema.py:127` `POST /node/issues`; `:225` `settlement:tallinn` stay
- OpenAPI: `openapi.yaml` path keys `/node/…` (five families)
- SPA: three Gateway*Repository.js + `__tests__` + contract test
- Sibling: spa-16 + REQ-51 `GET /node/issues`
- Not touched: ClusterLens members; pack id `tallinn_civic`; overlay UI; form builder; identity; HTTP filter; SSR-06/07/11/12/14/15; SSR-01…05/08–10 product; T-wave G3 audits; bullrun §Актуальная точка; `gateway-mvp-dashboard.md`; pie T-wave; pkg-000069 YAML; spa-app nested git commit

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-06/07/11/12/14/15. Optional P8 commits when asked (spa git skip unless operator).
