# Story acceptance gate — STORY-M2-04-06

- **Story:** Alpha scoring and story quality gate (REQ-36)
- **Package:** `pkg-000015-20260516-req36-alpha-scoring-story-quality-gate.yaml`
- **Result:** PASS
- **Date:** 2026-05-16

## AC checklist (REQ-36 §5)

| AC | Status | Evidence |
|----|--------|----------|
| `alpha_score` returns 0–100 | PASS | `test_alpha_score_rich_story_above_sixty` |
| Rich canonical + narrative → score > 60 | PASS | same |
| No canonical fields → score < 20 | PASS | `test_alpha_score_sparse_story_below_twenty` |
| geo=None → geo dimension 0 | PASS | `test_alpha_score_geo_none_skips_geo_dimension` |
| Dominant = max alpha_score | PASS | `test_select_dominant_story_picks_higher_alpha` |
| observation-only cluster not promoted | PASS | `test_req36_gate_rejects_observation_only_cluster` |
| CLUSTER_TIE_BREAKER=alpha only | PASS | `test_cluster_tie_breaker_non_alpha_raises` + default alpha |

## Runtime files

- `src/core/cluster/alpha.py`
- `src/core/projection/extraction_policy.py` (`select_dominant_story`)
- `src/core/cluster/engine.py` (scope docstring)
- `example.env`, `tests/test_alpha_score.py`, `tests/test_config_loading.py`

## Commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q
```
