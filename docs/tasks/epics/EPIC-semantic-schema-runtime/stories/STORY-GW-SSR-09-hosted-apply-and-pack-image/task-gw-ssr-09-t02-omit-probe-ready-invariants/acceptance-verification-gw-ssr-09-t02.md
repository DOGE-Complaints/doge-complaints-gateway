# acceptance-verification — GW-SSR-09 t02

- **Result:** PASS
- **Date:** 2026-08-29T18:14:04Z
- **Package:** pkg-000067

## Evidence

`_story_select_fields_for_db` (`db_supabase.py:470–476`) omits `_STORIES_BINDING_COLUMNS` only when `stories_binding_columns_ready` is false. `required_columns_ready` stories set (`:392–403`) has no binding names. `REQUIRED_READINESS_TABLES` (`:30–44`) unchanged (no `story_dimensions`). Probe cache `_stories_binding_columns_ready` (`:381–386`) documented — **live restart = operator, not overnight DoD**. Civic path not edited. Tests: `tests/test_gw_ssr_09_omit_probe_ready.py`.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_09_omit_probe_ready.py
```
