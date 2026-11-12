# run-summary — GW-SSR-15 P3 Execute

- **Date:** 2026-08-29T19:47:15Z
- **Package:** pkg-000072-20260829-gw-ssr-15-tests-abstract-node-and-scenarios.yaml
- **Story:** STORY-GW-SSR-15 tests `/node` + scenarios
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000072-20260829-gw-ssr-15-tests-abstract-node-and-scenarios.yaml
- **Result:** PASS (T01–T06 + T-dual Done; story gate PASS)

## G15 (runbook §6.7)

Public pytest URLs `/node/…`. Rename `test_req24_issues_read_api.py`. Scenarios civic / pack / Pulse≠issues / 404 `/tallinn/issues`. T-dual included (SSR-10 Done). Not `live_integration` proof. Geo `settlement:tallinn` stay. No alias 200.

## Queue executed

T01 path rename → T02 civic → T03 pack → T04 Pulse/Emerging → T05 404 → T-dual include → T06 story acceptance gate.

## Live verification

```text
ok 7 paths (project=gateway, pkg …/pkg-000072-…)
utc_now: 2026-08-29T19:47:15Z
G15 pytest -q -m "not live_integration"
  → 744 passed, 1 failed (known identity 503), 12 skipped (smoke), 10 deselected
rg '@app.get("/tallinn' tests → empty
rg 'client.(get|post)("/tallinn' tests → test_gw_ssr_15_scenarios.py:100 404 only
ClusterLens types.py:10–22 → still 10
rg story_dimensions|/schema-filter asgi_app.py → empty
ok date-check
```

## Product claims (code)

- Tests HTTP: `/node/issues`, `/node/network-pulse`, `/node/emerging-signals` after T01
- Rename: `tests/test_req24_issues_read_api.py` (no `tallinn` in filename)
- Scenarios: `tests/test_gw_ssr_15_scenarios.py` T02–T05 + T-dual
- Sole leftover `client.get("/tallinn/issues")`: T05 404 (`:100`)
- Hard-cut keep: `test_gw_ssr_11_public_dict_no_dump.py:105` `assert "/tallinn/issues" not in`
- Public routes unchanged: `asgi_app.py` `/node/*` (SSR-13)
- Not touched: ClusterLens members (10); geo `settlement:tallinn` / pack id `tallinn_civic`; identity-service (D-SSR-3); filter HTTP; `SchemaRuntime.project` stub; SSR-06/07/12; SSR-01…05/08–11/13/14 product; bullrun §Актуальная точка; `gateway-mvp-dashboard.md`; pie T-wave; pkg-000072 YAML; spa-app

## Residual (documented, not this story)

- `test_missing_identity_config_returns_503` FAIL in full-suite order (D-SSR-3; conftest autouse `IDENTITY_BASE_URL`). Identity-service not rewritten.
- 12 smoke skipped (`GATEWAY_URL` / server). Not hosted G15 proof.

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-06/07/12. Optional P8 commits when asked.
