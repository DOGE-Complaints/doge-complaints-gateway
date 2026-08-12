# Story acceptance gate — STORY-M2-04-05

- Story: `STORY-M2-04-05`
- Gate status: **PASS**
- Requirement: REQ-34 (`34-civic-clustering-canonical-signal-pipeline.md`)
- Package: `pkg-000013-20260515-req34-civic-canonical-signal.yaml`

## Evidence

- Legacy `ClusterLens` values removed; `CIVIC_LENSES` / `CANONICAL_LENSES` (6) in `cluster/engine.py` and `cluster/types.py`.
- `infer_signals_from_narrative` absent from `src/` (verified via `rg`).
- `get_signals_for_story(story)` → `infer_signals_from_canonical` only; `canonical_type` in signal dict.
- `CLUSTER_SIGNAL_SOURCE` accepts only `canonical`; civic six lenses in `example.env` and config defaults.
- `projection/extraction_policy.py`: `select_dominant_story`, `canonical_issue_type_from_story`, `spa_labels_from_canonical` (SPA label mapping).
- `promotion/gates.py`: `no_actionable_canonical_type` when cluster lacks `complaint` / `system_bug`.
- `cluster_orchestrator.py`: policy `v2.canonical`, wired dominant/cluster stories into issue create path.
- Tests: `test_signal_extraction_canonical.py` (ET/RU), `test_promotion_canonical_type_gate.py`, `test_projection_canonical_derivation.py`; suite **261 passed**, 9 skipped.
- Audit follow-up T08: operator `.env` civic-only (no legacy duplicate CLUSTER_* block).
- Audit follow-up T09: `KEYWORD_EXTRACTION_POLICY` removed from cluster public API.

## Verification commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
rg -n infer_signals_from_narrative src/
```
