# task-gw-tax-02-t03-story-labels-signal-source

## Meta
- **Story:** [STORY-GW-TAX-02](../STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000055
- **Skill declared:** python-pro
- **Depends on:** T02 (axis mapping for new dimensions)

## Purpose
Источник сигналов из `story_labels` per-axis (GW-TAX-01) вместо/поверх `infer_signals_from_canonical` (D-TAX-1).

## Code Facts
- Partial wiring: `get_signals_for_story(..., story_label_repository=)` — [`profile/enrichment.py:81+`](../../../../../../../../src/core/profile/enrichment.py#L81)
- `signals_from_story_labels` + incomplete `_AXIS_TO_SIGNAL_DIMENSION` — [`taxonomy/story_labels.py:136-174`](../../../../../../../../src/core/taxonomy/story_labels.py#L136)
- Orchestrator has `story_label_repository` field — [`cluster_orchestrator.py:35`](../../../../../../../../src/core/application/cluster_orchestrator.py#L35)
- DI assembly — [`infrastructure/service_factory.py:83`](../../../../../../../../src/core/infrastructure/service_factory.py#L83)

## Acceptance / DoD
- [x] Traces parent AC-2: axes from `story_labels` per-axis (not dictionary re-guess when labels present)
- [x] Scope trace: backlog T03 / D-TAX-1 signal source
- [x] `_AXIS_TO_SIGNAL_DIMENSION` covers new axes (`service_object`, `deep_need`, `ecosystem_signal`)
- [x] Clustering path prefers stored `story_labels` over `infer_signals_from_canonical` when repo populated
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-02-t03.md`](./acceptance-verification-gw-tax-02-t03.md) signed (Date post live-run only)

## Where to change
- [`src/core/taxonomy/story_labels.py`](../../../../../../../../src/core/taxonomy/story_labels.py) (`signals_from_story_labels`, `_AXIS_TO_SIGNAL_DIMENSION`)
- [`src/core/profile/enrichment.py`](../../../../../../../../src/core/profile/enrichment.py) (`get_signals_for_story`)
- [`src/core/application/cluster_orchestrator.py`](../../../../../../../../src/core/application/cluster_orchestrator.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py), [`providers.py`](../../../../../../../../src/core/infrastructure/providers.py)

## Out of scope
- GW-TAX-01 intake/persist (Done)
- GPT-TAX-01 producer contract
- Composite key engine (T01); per-lens min_size (T04)

## Verification commands (post live-run only)
```bash
rg -n "signals_from_story_labels|story_label_repository" doge-complaints-gateway/src/core/
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration" -k story_labels
```
