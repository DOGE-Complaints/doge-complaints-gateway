# task-gw-es-02-t06-runtime-docs-openapi

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** **T00 Done** (path named); T03
- **decision_ref:** backlog ES-02 Runtime-docs дельта

## Purpose
Обновить OpenAPI + API_REFERENCE для Network Pulse L1 после path named; Topic≠Issue note; optional pointer toward TASK-GW-ES-04 / spa-15 seam.

## Code Facts
- [`openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- Soft seam — [`TASK-GW-ES-04`](../../../../../../backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md)

## Acceptance / DoD
- [x] Traces parent Runtime-docs дельта: path from T00 REQ in openapi + API_REFERENCE Network Pulse L1
- [x] Topic≠Issue note present
- [x] No invent path beyond T00
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t06.md` signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md`

## Out of scope
- spa-15 UI wiring; inventing path; ES-03 docs

## Verification commands
```bash
# After T00 path known:
rg -n 'Network Pulse|network.pulse|Topic' doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md | head
rg -n 'PATH_FROM_T00_or_literal' doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml | head
```
