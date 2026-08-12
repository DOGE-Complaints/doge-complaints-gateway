# task-gw-tax-02-t01-composite-primary-cluster-key

## Meta
- **Story:** [STORY-GW-TAX-02](../STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000055
- **Skill declared:** python-pro
- **Depends on:** —

## Purpose
Composite-primary (D-CLUST-1/2): движок строит ключ из **связки** осей (`civic_domain`+`failure_pattern`); расширить `cluster_key_for_lens` (сейчас `lens:dimension:value:scope`) на composite-key + primary-линза.

## Code Facts
- Ключ линзы = одно значение одной оси — [`cluster/engine.py:70-89`](../../../../../../../../src/core/cluster/engine.py#L70)
- Primary = `civic_domain_micro` via `resolved_primary_lens()` — [`engine.py:182`](../../../../../../../../src/core/cluster/engine.py#L182); config default — [`schema.py:181-184`](../../../../../../../../src/core/config/schema.py#L181)
- `domain+pattern` только debug-лейбл — [`cluster_orchestrator.py:139`](../../../../../../../../src/core/application/cluster_orchestrator.py#L139)
- Issue создаёт только primary-линза — [`cluster_orchestrator.py:244`](../../../../../../../../src/core/application/cluster_orchestrator.py#L244)

## Acceptance / DoD
- [x] Traces parent AC-1: primary issue-ключ = composite `civic_domain + failure_pattern`
- [x] Scope trace: backlog T01 / D-CLUST-1/2 composite-primary
- [x] `cluster_key_for_lens` (or successor) supports composite axis pair for primary lens
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-02-t01.md`](./acceptance-verification-gw-tax-02-t01.md) signed (Date post live-run only)

## Where to change
- [`src/core/cluster/engine.py`](../../../../../../../../src/core/cluster/engine.py) (`cluster_key_for_lens`, `resolved_primary_lens`)
- [`src/core/application/cluster_orchestrator.py`](../../../../../../../../src/core/application/cluster_orchestrator.py) (primary lens selection, debug label vs grouping)

## Out of scope
- New SignalDimension / ClusterLens (T02)
- story_labels signal source (T03)
- Per-lens min_size (T04)
- GW-TAX-01 persist/intake; GPT-TAX-01; parallel board lenses; global `CLUSTER_MIN_SIZE` downgrade

## Verification commands (post live-run only)
```bash
rg -n "cluster_key_for_lens|composite|civic_domain.*failure_pattern" doge-complaints-gateway/src/core/cluster/
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration" -k composite
```
