# acceptance-verification — GW-SSR-09 t03

- **Result:** PASS
- **Date:** 2026-08-29T18:14:04Z
- **Package:** pkg-000067

## Evidence

`schema-packs/` present; `default_packs_root` (`resolver.py:19–30`) resolves `legal_process/v1` and `tallinn_civic/v1`. `SCHEMA_PACKS_ROOT` env override works; **not** in `AppConfig` (`src/core/config` Grep empty). **Dockerfile invented: no** (gateway Glob 0). Live image = operator, not overnight proof. `asgi_app.py` no `story_dimensions` / `/schema-filter`; `GET /tallinn/issues` stays. Tests: `tests/test_gw_ssr_09_packs_visible.py`.

## Commands

```bash
test -d doge-complaints-gateway/schema-packs
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_09_packs_visible.py
```
