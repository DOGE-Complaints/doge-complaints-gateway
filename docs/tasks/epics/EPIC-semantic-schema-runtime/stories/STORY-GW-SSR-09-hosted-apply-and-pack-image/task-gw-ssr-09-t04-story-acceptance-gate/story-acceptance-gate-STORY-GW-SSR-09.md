# Story acceptance gate — STORY-GW-SSR-09

- **Story:** Hosted apply binding migration + packs in deploy image
- **Package:** `pkg-000067-20260829-gw-ssr-09-hosted-apply-and-pack-image.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T18:14:04Z

## Hosted apply is not overnight proof (G9)

Live hosted apply / process restart / live image = **operator/deploy**, not this pkg’s overnight proof (same class as T-wave `live_integration`). G9 = artifacts on disk + omit-probe / `/ready` invariants.

| G9 check | Result | Evidence |
|----------|--------|----------|
| `test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql` | PASS | six nullable `ADD COLUMN IF NOT EXISTS` = `_STORIES_BINDING_COLUMNS` |
| `required_columns_ready` does **not** contain binding columns | PASS | `db_supabase.py:392–403` stories set: civic/geo only |
| `test -d schema-packs/` | PASS | `legal_process/v1`, `mobility_observation/v1`, `tallinn_civic/v1` |
| no new HTTP (`rg story_dimensions\|/schema-filter` in `asgi_app.py`) | PASS | empty; `GET /tallinn/issues` stays `:462` |
| civic `/ready` not requiring binding cols | PASS | `required_columns_ready` source omits six names; `REQUIRED_READINESS_TABLES` unchanged |
| Dockerfile invented | **no** | gateway Glob 0 |
| binding in `required_columns_ready` | **no** | `:392–403` |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Hosted `stories` имеет шесть nullable binding-колонок. | PASS | SQL artifact on disk (not live Railway apply). `20260828_1400_gw_ssr_02_stories_schema_binding.sql:4–10`; `tests/test_gw_ssr_09_hosted_sql_binding.py`. Live apply = operator/deploy. |
| После рестарта persist `schema_binding` на supabase не вырезается omit-probe. | PASS | Invariant: omit only when `stories_binding_columns_ready` is false (`db_supabase.py:470–476`); when true, SELECT keeps six names. Cache `:381–386` — live restart = operator, not overnight DoD. `tests/test_gw_ssr_09_omit_probe_ready.py`. |
| `/ready` не требует binding-колонки. | PASS | `required_columns_ready` stories set `:392–403` without the six names. |
| Resolver находит example pack в деплое. | PASS | `schema-packs/` + `default_packs_root` (`resolver.py:19–30`); `legal_process/v1` and `tallinn_civic/v1`. CWD ≠ root → `SCHEMA_PACKS_ROOT` (no `AppConfig` field). Live image = operator. `tests/test_gw_ssr_09_packs_visible.py`. |
| Нет нового HTTP. | PASS | `asgi_app.py` no `story_dimensions` / `/schema-filter`; `GET /tallinn/issues` stays. |

## Commands (live verification 2026-08-29T18:14:04Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway
test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
rg -n "required_columns_ready" -A 40 src/core/infrastructure/db_supabase.py
rg -n "schema_id|bound_schema_version|structured_payload" src/core/infrastructure/db_supabase.py
test -d schema-packs
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
# → no matches
./.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_09_hosted_sql_binding.py \
  tests/test_gw_ssr_09_omit_probe_ready.py \
  tests/test_gw_ssr_09_packs_visible.py
# → 12 passed
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

Live Railway SQL apply / process restart / image bake = operator. SSR-10 not started. SSR-06/07/12 not started. Pie T-wave unchanged.
