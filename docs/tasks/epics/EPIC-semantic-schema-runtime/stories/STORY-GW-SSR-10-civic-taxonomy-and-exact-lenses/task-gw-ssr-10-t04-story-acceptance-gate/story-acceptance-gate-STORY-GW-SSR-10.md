# Story acceptance gate — STORY-GW-SSR-10

- **Story:** Taxonomy + exact lenses on one bound story (pack-declared)
- **Package:** `pkg-000068-20260829-gw-ssr-10-civic-taxonomy-and-exact-lenses.yaml`
- **Result:** PASS
- **Date:** 2026-08-29T18:31:19Z

## G10 (runbook §6.3)

Dual **opt-in** in pack.json; default = exact-only (`legal_process`). Do not expand `ClusterLens`.

| G10 check | Result | Evidence |
|-----------|--------|----------|
| dual fixture civic lens value **and** pack `lens_id` on same `story_id` | PASS | `tests/test_gw_ssr_10_orchestrator_dual.py` `test_dual_fixture_civic_and_pack_lens_on_same_story` |
| pack without dual key = T-wave exact-only (`legal_process` green) | PASS | `legal_process/v1/pack.json` has no `dual_civic_lenses`; `test_legal_process_absent_dual_key_is_exact_only`; `test_pack_without_dual_key_stays_exact_only` |
| civic unbound green | PASS | `test_civic_unbound_unchanged_when_dual_bound_present`; `tests/test_clustering_engine.py` + `tests/test_gw_ssr_04_*` |
| `ClusterLens` = 10; no pack lens in enum | PASS | `types.py:10–22`; `len(ClusterLens)==10`; no `police_station` member |
| no `POLICE_STATION` in `types.py`/`engine.py` | PASS | `rg` empty |
| no new HTTP | PASS | `rg story_dimensions\|/schema-filter` in `asgi_app.py` empty |

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Pack MAY объявить dual; absent/false = T-wave поведение. | PASS | `resolver.py` `_parse_dual_civic_lenses`; `schema-packs/README.md`; `tests/test_gw_ssr_10_dual_pack_flag.py` |
| Dual: membership и civic-линз (enum value) и pack `lens_id` на одном `story_id`. | PASS | `_process_bound_story` + `_process_dual_civic_membership`; `test_dual_fixture_civic_and_pack_lens_on_same_story` |
| `ClusterLens` по-прежнему 10. | PASS | `types.py:10–22`; G10 rg |
| Civic без binding зелёный. | PASS | `_civic_ready` excludes bound; civic/04 slice green |
| Нет нового HTTP. | PASS | `asgi_app.py` no `story_dimensions` / `/schema-filter` |

## Commands (live verification 2026-08-29T18:31:19Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_10_dual_pack_flag.py tests/test_gw_ssr_10_orchestrator_dual.py \
  tests/test_gw_ssr_10_promote_separate.py
.venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_clustering_engine.py tests/test_gw_ssr_04_schema_driven_cluster_lens.py \
  tests/test_gw_ssr_05_pack_promote_clustered.py tests/test_gw_ssr_05_public_card_no_payload.py \
  tests/test_gw_ssr_05_negative_ac_018_no_qry.py tests/test_gw_ssr_05_optional_gate_policy.py \
  tests/test_gw_ssr_05_pack_policy_mapper.py
# → 55 passed
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

SSR-06/07/11/12/13 not started. SSR-01…05 / 08 / 09 not reopened. Pie T-wave unchanged. bullrun §«Актуальная точка» unchanged. `gateway-mvp-dashboard.md` unchanged. pkg-000068 immutable.
