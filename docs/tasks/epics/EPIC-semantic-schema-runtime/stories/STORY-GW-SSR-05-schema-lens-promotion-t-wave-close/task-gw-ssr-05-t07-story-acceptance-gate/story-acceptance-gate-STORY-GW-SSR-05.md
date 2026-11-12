# Story acceptance gate — STORY-GW-SSR-05

- **Story:** Pack promotion policy + T-wave close without QRY HTTP
- **Package:** `pkg-000065-20260828-gw-ssr-05-schema-lens-promotion-t-wave-close.yaml`
- **Result:** PASS
- **Date:** 2026-08-28T15:00:08Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ3-14 / AC-014: schema-pack exact-lens cluster promotes under pack readiness policy **without** civic type tokens; civic-lens tests still pass. | PASS | `cluster_orchestrator.py` `_promote_pack_membership` + `gate_policy` override; `tests/test_gw_ssr_05_pack_promote_clustered.py::test_three_pack_stories_promote_without_civic_types`; civic G5 slice 52 passed |
| Civic built-in remains; not the only platform rule (CL-006). | PASS | `gates.py:14` `require_actionable_canonical_type: bool = True`; factory `service_factory.py` civic `PromotionGatePolicy(` unchanged; pack mapper `pack_policy.py` copies pack-file knobs (legal_process 40/3/False) |
| AC-GW-REQ3-18 / AC-018: T-wave accepted without generic analytical filter HTTP (AC-005) and without processor delivery. | PASS | `asgi_app.py` no `story_dimensions`/`/schema-filter`; `runtime.py` `build_index`/`project` `NotImplementedError`; `tests/test_gw_ssr_05_negative_ac_018_no_qry.py` |
| Public read path unchanged: `GET /tallinn/issues`; payload not automatic on Issue (SPA-003) — no invented field names. | PASS | `asgi_app.py:462` `@app.get("/tallinn/issues")`; `dto.py` `to_public_dict` without `structured_payload`; `tests/test_gw_ssr_05_public_card_no_payload.py` |
| §29 Compatibility: pack-lens promote without civic types; civic promotion tests green. | PASS | pack tests omit `complaint`/`system_bug`; `test_promotion_canonical_type_gate.py` + `test_issue_promotion_service.py` + `test_clustering_engine.py` + `test_gw_tax_02_cluster_axis_expansion.py` green in G5 52 passed |

## Commands (live verification 2026-08-28T15:00:08Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_pack_policy_mapper.py \
  tests/test_gw_ssr_05_optional_gate_policy.py \
  tests/test_gw_ssr_05_pack_promote_clustered.py \
  tests/test_gw_ssr_05_public_card_no_payload.py \
  tests/test_gw_ssr_05_negative_ac_018_no_qry.py \
  tests/test_promotion_canonical_type_gate.py \
  tests/test_issue_promotion_service.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py
# → 52 passed
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration"
# → 690 passed, 12 skipped, 10 deselected; 1 failed tests/test_gw_draft_02_get_auth_contract.py::test_missing_identity_config_returns_503
#    (order-dependent; file 6/6 and isolated 1 passed; not SSR-05 src; identity not in this story)
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
# → 14:    require_actionable_canonical_type: bool = True
rg -n "structured_payload" src/core/projection/dto.py
# → no matches
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
# → no matches
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)

## Residual (not story AC)

Full-offline suite: 1 fail `test_missing_identity_config_returns_503` (draft GET identity config). Isolated pass. Not in G5 bundle. SSR-05 did not change identity handlers (`D-SSR-3`).
