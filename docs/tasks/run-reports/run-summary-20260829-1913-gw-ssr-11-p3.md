# run-summary — GW-SSR-11 P3 Execute

- **Date:** 2026-08-29T19:13:51Z
- **Package:** pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml
- **Story:** STORY-GW-SSR-11 pack-declared Issue projection
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000070-20260829-gw-ssr-11-pack-declared-issue-projection.yaml
- **Result:** PASS (T00–T04 Done; story gate PASS)

## G11 (runbook §6.5)

Named `schema_card` sidecar from pack `card_fields`. No payload dump. Civic form when key absent. Public read = `GET /node/issues`. Overlay UI spa — no.

## Queue executed

T00 pack card-fields contract → T01 loader allowlist → T02 named projection → T03 tests no dump → T04 story acceptance gate.

## Live verification

```text
ok 5 paths (project=gateway, pkg …/pkg-000070-…)
utc_now: 2026-08-29T19:13:51Z
G11 pytest (ssr-11 + ssr-05/10/dto) → 29 passed
rg structured_payload dto.py → empty
rg /node/issues asgi_app.py → present (@app.get("/node/issues") :462)
rg require_actionable_canonical_type: bool = True gates.py → :14
ok date-check
```

## Product claims (code)

- Key: `SchemaContext.card_fields` (`contracts.py`); parse `resolver.py` `_parse_card_fields`; doc `schema-packs/README.md`
- Extract: `project_card_fields` (`card_fields.py`) — filters `forbidden` / `node_private`
- Wire: `to_public_dict(schema_card=…)` (`dto.py`); `IssueCreateService._to_public_payload` (`issue_create.py`)
- Public read: `GET /node/issues` (`asgi_app.py:462`)
- Tests: `tests/test_gw_ssr_11_*.py`
- Not touched: ClusterLens members; legal_process/tallinn_civic pack.json (no `card_fields`); civic factory; `gates.py:14` default True; HTTP filter; identity; `SchemaRuntime.project` stub; SSR-06/07/12/14/15; SSR-01…05/08–10/13 product; bullrun §Актуальная точка; `gateway-mvp-dashboard.md`; pie T-wave; pkg-000070 YAML; spa-app overlay UI

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-06/07/12/14/15. Optional P8 commits when asked.
