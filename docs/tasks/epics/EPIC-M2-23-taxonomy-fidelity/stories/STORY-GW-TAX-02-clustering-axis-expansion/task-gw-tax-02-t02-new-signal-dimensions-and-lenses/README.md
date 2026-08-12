# task-gw-tax-02-t02-new-signal-dimensions-and-lenses

## Meta
- **Story:** [STORY-GW-TAX-02](../STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000055
- **Skill declared:** python-pro
- **Depends on:** T01 (composite primary may reference new dimensions)

## Purpose
Новые `SignalDimension` `service_object`/`ecosystem_signal` + `ClusterLens` + `lens_dimension`-маппинг; `deep_need`→ существующий `NEED` (D-CLUST-3).

## Code Facts
- `ClusterLens` — 6 values only — [`cluster/types.py:10-18`](../../../../../../../../src/core/cluster/types.py#L10)
- `SignalDimension` — no `service_object`/`ecosystem_signal` — [`domain/contracts.py:172-191`](../../../../../../../../src/core/domain/contracts.py#L172)
- `lens_dimension` maps 6 lenses to civic axes — [`cluster/engine.py:58-67`](../../../../../../../../src/core/cluster/engine.py#L58)
- `CIVIC_LENSES` tuple — [`cluster/engine.py:20`](../../../../../../../../src/core/cluster/engine.py#L20)

## Acceptance / DoD
- [x] Traces parent AC-2: `service_object`, `deep_need`, `ecosystem_signal` as lenses/facets
- [x] Scope trace: backlog T02 / D-CLUST-3 new axes
- [x] `service_object`, `ecosystem_signal` added to `SignalDimension` + `ClusterLens` + `lens_dimension`
- [x] `deep_need` mapped to existing `NEED` dimension
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-02-t02.md`](./acceptance-verification-gw-tax-02-t02.md) signed (Date post live-run only)

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../../src/core/domain/contracts.py) (`SignalDimension`)
- [`src/core/cluster/types.py`](../../../../../../../../src/core/cluster/types.py) (`ClusterLens`)
- [`src/core/cluster/engine.py`](../../../../../../../../src/core/cluster/engine.py) (`CIVIC_LENSES`, `lens_dimension`)

## Out of scope
- Composite primary key implementation details (T01)
- story_labels wiring (T03)
- Per-lens min_size (T04)
- GW-TAX-01; GPT-TAX-01; parallel board lenses; global `CLUSTER_MIN_SIZE` downgrade

## Verification commands (post live-run only)
```bash
rg -n "service_object|ecosystem_signal|deep_need" doge-complaints-gateway/src/core/domain/ doge-complaints-gateway/src/core/cluster/
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration" -k dimension
```
