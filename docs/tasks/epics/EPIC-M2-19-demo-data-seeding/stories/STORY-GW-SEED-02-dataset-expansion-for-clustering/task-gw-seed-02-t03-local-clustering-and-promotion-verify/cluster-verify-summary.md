# Cluster verify summary — STORY-GW-SEED-02 T03

- **Date:** 2026-06-22
- **Canvas:** `tests/sandbox/dogestonia_simulation_canvas_v0_2.json` (18 scenarios)
- **Env (verify):** `CLUSTER_MIN_SIZE=8`, `CLUSTER_READINESS_THRESHOLD=70`, `CLUSTER_GEO_FILTER=district` (in-memory + sqlite pytest)

## Pre-check (offline bucket sizes)

| cluster key (civic_domain \| geographic_district) | stories | ≥8 |
|---------------------------------------------------|---------|-----|
| `waste\|kalamaja` | 9 | yes |
| `roads\|lasnamäe` | 9 | yes |

Source: `infer_signals_from_canonical` on v0_2 `canonical_payload` labels + district from `test_metadata.seed_cluster_target` ([`enrichment.py`](../../../../../../../src/core/profile/enrichment.py)).

## Live run (in-memory orchestrator)

| Metric | Value |
|--------|-------|
| ready stories loaded | 18 |
| `process_all_pending()` issue_ids | 2 |
| projection count | 2 |
| sample issue_ids | `46fbb308-7c9c-4c74-957d-d9731567b237`, `ed277f0c-1966-4204-805d-f58ff243d297` |

Command: in-process `StoryClusterOrchestrator.process_all_pending()` with `PromotionGatePolicy(min_stories=8, min_readiness_score=70)` — same path as [`cluster_orchestrator.py`](../../../../../../../src/core/application/cluster_orchestrator.py).

## Automated tests

```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_gw_seed_02_cluster_density.py
# 4 passed (2026-06-22)
```

Covers: v0_2 file + v0_1 unchanged, offline buckets ≥8, in-memory promotion, sqlite intake + `process_all_pending`.
