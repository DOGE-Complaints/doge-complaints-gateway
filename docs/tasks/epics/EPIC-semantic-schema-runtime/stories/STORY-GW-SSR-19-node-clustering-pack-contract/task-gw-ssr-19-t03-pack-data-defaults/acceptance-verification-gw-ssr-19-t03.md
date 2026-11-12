# acceptance-verification — GW-SSR-19 t03

- **Result:** PASS
- **Date:** 2026-08-30T19:21:58Z
- **Package:** pkg-000076

## Evidence

Three packs have `node_clustering.civic` from EnvSpec defaults (`schema.py:166–240`): min_size 5; `composite_primary_micro=8` in `min_size_by_lens`; readiness 60; 10 lenses. tallinn `geo_scope=settlement:tallinn`; legal/mobility `null`. No cron keys in pack.json.
