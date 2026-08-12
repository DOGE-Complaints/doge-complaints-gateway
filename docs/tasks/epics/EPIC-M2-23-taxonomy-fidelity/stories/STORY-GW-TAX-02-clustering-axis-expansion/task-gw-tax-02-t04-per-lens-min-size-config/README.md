# task-gw-tax-02-t04-per-lens-min-size-config

## Meta
- **Story:** [STORY-GW-TAX-02](../STORY-GW-TAX-02-clustering-axis-expansion.md)
- **Type:** implement
- **Status:** ✅ Done
- **Package:** pkg-000055
- **Skill declared:** python-pro
- **Depends on:** T01 (composite primary lens id for per-lens threshold)

## Purpose
Per-lens `min_size`: конфиг `CLUSTER_MIN_SIZE_BY_LENS` (composite-primary=8, богатые оси ниже) + honor в `_resolve_min_size_guard`/promotion-gate; глобальный `CLUSTER_MIN_SIZE` не понижать (D-CLUST-4).

## Code Facts
- Global `CLUSTER_MIN_SIZE` only — [`config/schema.py:163-167`](../../../../../../../../src/core/config/schema.py#L163)
- `_resolve_min_size_guard` uses promotion `min_stories` — [`cluster_orchestrator.py:204-210`](../../../../../../../../src/core/application/cluster_orchestrator.py#L204)
- Prod target min_size=8; demo `.env`=2 — backlog «Что наблюдаю»

## Acceptance / DoD
- [x] Traces parent AC-3: per-lens `min_size`; composite-primary=8; rich axes lower
- [x] Scope trace: backlog T04 / D-CLUST-4
- [x] `CLUSTER_MIN_SIZE_BY_LENS` (or equivalent) in config schema + env parsing
- [x] `_resolve_min_size_guard` / promotion gate honors per-lens values
- [x] Global `CLUSTER_MIN_SIZE` default **not** lowered
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-tax-02-t04.md`](./acceptance-verification-gw-tax-02-t04.md) signed (Date post live-run only)

## Where to change
- [`src/core/config/schema.py`](../../../../../../../../src/core/config/schema.py)
- [`src/core/application/cluster_orchestrator.py`](../../../../../../../../src/core/application/cluster_orchestrator.py) (`_resolve_min_size_guard`)

## Out of scope
- Composite engine (T01); new dimensions (T02); signal source (T03)
- GW-TAX-01; GPT-TAX-01; lowering global threshold for board fill

## Verification commands (post live-run only)
```bash
rg -n "CLUSTER_MIN_SIZE_BY_LENS|min_size" doge-complaints-gateway/src/core/config/ doge-complaints-gateway/src/core/application/cluster_orchestrator.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_tax_02_* -m "not live_integration" -k min_size
```
