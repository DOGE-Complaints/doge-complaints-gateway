# Story acceptance gate — STORY-GW-SSR-35

- **Story:** SCHEMA_ROOT_URL + SCHEMA_PACK_REFRESH (federation remote registry)
- **Package:** `pkg-000092-20260907-gw-ssr-35-schema-root-url-pack-refresh.yaml`
- **Result:** PASS
- **Date:** 2026-09-07T08:54:22Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-SSR35-01: URL + empty cache → resolve_pack SUCCESS (fixture) | PASS | `test_fetch_on_cache_miss_then_resolve_pack`; `test_boot_load_config_fetches_via_mock` |
| AC-GW-SSR35-02: Fresh cache → no unnecessary re-fetch | PASS | `test_fresh_cache_skips_refetch` |
| AC-GW-SSR35-03: Refresh overwrite; corrupt → ConfigError; not tallinn default | PASS | `test_refresh_overwrites_cached_pack`; `test_corrupt_manifest_fail_fast_no_tallinn` |
| AC-GW-SSR35-04: pytest mocked HTTP; no network in CI | PASS | `httpx.MockTransport` in `test_gw_ssr_35_schema_root_url_pack_refresh.py` |
| AC-GW-SSR35-05: Manuals URL = federation; Volume = SCHEMA_PACKS_ROOT only | PASS | server-env federation playbook; warehouse glossary; example.env |

## Commands (live verification — P3)

```text
--verify ok 7 (pkg-000092)
utc_now: 2026-09-07T08:54:22Z
.venv/bin/python -m pytest -q tests/test_gw_ssr_35_schema_root_url_pack_refresh.py
→ 12 passed
rg SCHEMA_ROOT_URL src/core/config/schema.py src/core/schema/remote_fetch.py → present
Volume path rejected; §Актуальная точка not rewritten
```
