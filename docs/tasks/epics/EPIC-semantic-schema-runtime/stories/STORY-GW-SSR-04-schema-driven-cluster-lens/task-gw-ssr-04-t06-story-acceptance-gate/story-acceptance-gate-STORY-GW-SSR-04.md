# Story acceptance gate — STORY-GW-SSR-04

- **Story:** Schema-pack exact lens membership (civic ClusterLens preserved)
- **Package:** `pkg-000064-20260828-gw-ssr-04-schema-driven-cluster-lens.yaml`
- **Result:** PASS
- **Date:** 2026-08-28T14:36:12Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ3-07 / AC-007: exact lens over structured fields → memberships without new hard-coded `ClusterLens` member. | PASS | `src/core/schema/pack_engine.py` `SchemaPackClusterEngine` / `pack_cluster_id`; `tests/test_gw_ssr_04_schema_driven_cluster_lens.py::test_two_payloads_same_office_id_share_cluster_id`; `test_clusterlens_still_ten_civic_members`; `types.py` still 10 members |
| AC-008: existing Tallinn civic clustering + issue projection tests still pass. | PASS | G4: `test_clustering_engine.py` + `test_gw_tax_02_cluster_axis_expansion.py` + `test_story_cluster_orchestrator.py` + `test_cluster_cron_job.py` + `test_e2e_story_cluster_issue_pipeline.py` green in 57 passed |
| CL-004: Story MAY have multiple memberships; no exclusive collapse. | PASS | engine yields one `PackMembership` per matching `exact_lenses` entry (`memberships_for_context`); pack-bound excluded from civic buckets (`test_schema_bound_does_not_enter_civic_buckets`) so civic lenses are not collapsed onto pack stories |
| SEC-004: no automatic sensitive payload in cluster narratives. | PASS | pack does not call `build_cluster_narrative`; `_leaf_token` skips Mapping/list; `test_cluster_id_does_not_embed_secret_note` |

## Commands (live verification 2026-08-28T14:36:12Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_04_schema_driven_cluster_lens.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py \
  tests/test_story_cluster_orchestrator.py \
  tests/test_cluster_cron_job.py \
  tests/test_e2e_story_cluster_issue_pipeline.py
# → 57 passed
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
# → 10 members; no POLICE_STATION
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
# → no matches
rg -n "process_all_pending" src/core/scheduler/cluster_cron.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
