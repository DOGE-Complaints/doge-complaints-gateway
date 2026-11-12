# run-summary — GW-SSR-09 P3 Execute

- **Date:** 2026-08-29T18:14:04Z
- **Package:** pkg-000067-20260829-gw-ssr-09-hosted-apply-and-pack-image.yaml
- **Story:** STORY-GW-SSR-09 hosted apply + packs in image
- **gateway_input_package:** doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000067-20260829-gw-ssr-09-hosted-apply-and-pack-image.yaml
- **Result:** PASS (T01–T04 Done; story gate PASS)

## Hosted apply is not overnight proof (G9)

Live hosted apply / restart / image = **operator/deploy**, not overnight proof (runbook §6.2). G9 = artifacts on disk + omit-probe / `/ready` invariants.

## Queue executed

T01 hosted SQL binding migration → T02 omit-probe + `/ready` invariants → T03 packs visible to resolver → T04 story acceptance gate.

## Live verification

```text
ok 4 paths (project=gateway, pkg …/pkg-000067-…)
utc_now: 2026-08-29T18:14:04Z
test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql → OK
required_columns_ready stories set :392–403 → no binding cols
test -d schema-packs → OK
rg story_dimensions|/schema-filter asgi_app.py → no matches
.venv/bin/python -m pytest -q -m "not live_integration" tests/test_gw_ssr_09_*.py
→ 12 passed
Dockerfile invented: no (Glob 0)
binding in required_columns_ready: no
ok date-check (after this file)
```

## Product claims (code)

- SQL: `supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql` six nullable cols = `_STORIES_BINDING_COLUMNS` (`db_supabase.py:333–341`)
- Omit-probe: `_story_select_fields_for_db` (`:470–476`); cache `:381–386`
- `/ready`: `required_columns_ready` `:388–403` without binding names
- Packs: `schema-packs/` + `resolver.py:19–30`; no `AppConfig.SCHEMA_PACKS_ROOT`
- Tests: `tests/test_gw_ssr_09_*.py`
- Not touched: ClusterLens; civic factory; `PromotionGatePolicy` default; `REQUIRED_READINESS_TABLES`; identity; SSR-06/07/10/12; SSR-08; bullrun §Актуальная точка; `gateway-mvp-dashboard.md`; pie T-wave; pkg-000067 YAML; no new Dockerfile; no new HTTP

## Next

P4 audit (operator). Do not start P4 in this step. Do not start SSR-06/07/10/12. Optional P8 commits when asked.
