# acceptance-verification — GW-SSR-05 t03

- **Result:** PASS
- **Date:** 2026-08-28T15:00:08Z
- **Package:** pkg-000065

## Evidence

`_process_pack_bound_story` saves membership then `_promote_pack_membership`. Pack `create_issue` with `gate_policy=` override; score from pack `min_size` vs `min_readiness_score` (not `readiness_score_for_cluster`). `CLUSTERED` only after successful promote. Two legal_process members stay READY; three promote. Cron still `process_all_pending`. Does not call civic `_create_issue_for_cluster`.

## Commands

```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_pack_promote_clustered.py tests/test_gw_ssr_04_schema_driven_cluster_lens.py
```
