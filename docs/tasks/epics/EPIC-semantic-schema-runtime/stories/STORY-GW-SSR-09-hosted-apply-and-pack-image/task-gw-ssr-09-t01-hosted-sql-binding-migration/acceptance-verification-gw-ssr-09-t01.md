# acceptance-verification — GW-SSR-09 t01

- **Result:** PASS
- **Date:** 2026-08-29T18:14:04Z
- **Package:** pkg-000067

## Evidence

`supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql` on disk; six `ADD COLUMN IF NOT EXISTS` names match `_STORIES_BINDING_COLUMNS` (`db_supabase.py:333–341`). No DROP. Binding names absent from `required_columns_ready` (`db_supabase.py:388–403`). **Hosted apply + restart = operator/deploy, not overnight proof** (pipeline §G9; manual Hosted Supabase row). Tests: `tests/test_gw_ssr_09_hosted_sql_binding.py`.

## Commands

```bash
test -f doge-complaints-gateway/supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_09_hosted_sql_binding.py
```
