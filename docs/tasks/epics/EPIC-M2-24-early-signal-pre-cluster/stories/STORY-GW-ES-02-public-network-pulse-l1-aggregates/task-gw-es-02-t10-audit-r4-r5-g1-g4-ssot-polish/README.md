# task-gw-es-02-t10-audit-r4-r5-g1-g4-ssot-polish

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000059 (parent Done); wave `run_mode=gw_es_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-ES-02
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-es-02-…`](../../../../../../analysis/audit-gw-es-02-public-network-pulse-l1-aggregates-2026-08-10.md) **R4**, **R5**, **G1**, **G4**
- **Scaffolded:** 2026-08-10T11:32:43Z
- **Closed:** 2026-08-10T11:48:57Z

## Purpose
Satellite SSOT polish post-ES-02: epic Problem Statement; dashboard REQ-48 Notes; REQ-49 disposition wording; OpenAPI root `tags` declare `EarlySignal`. Docs only — no runtime.

## Code Facts
- R4 stale epic — [`EPIC-M2-24` Problem Statement](../../../../EPIC-M2-24-early-signal-pre-cluster.md) «публичного Pulse aggregate нет»
- R5 dashboard — [`gateway-mvp-dashboard.md`](../../../../gateway-mvp-dashboard.md) REQ-48 Notes «ES-02 In Progress»
- G1 REQ-49 §3 «exclude internal» vs code `is_public_label_disposition` — [`disposition.py`](../../../../../../../../src/core/taxonomy/disposition.py); [`49-…md`](../../../../../../requirements/49-early-signal-network-pulse-l1-api.md)
- G4 OpenAPI — path uses `tags: [EarlySignal]` but root `tags:` only Ops/Intake — [`openapi.yaml:16-20`](../../../../../../runtime-docs/api-reference/openapi.yaml)

## Acceptance / DoD
- [x] R4: EPIC-M2-24 Problem Statement / Meta reflect post-ES-02 Pulse exists; ES-03 remains open
- [x] R5: dashboard REQ-48 Notes → Done pkg-000059 / gate PASS (not In Progress)
- [x] G1: REQ-49 §3 one phrase — public topics = `is_public_label_disposition` / canonical-only (TAX §24), not «всё кроме internal»
- [x] G4: root openapi `tags` includes `name: EarlySignal` with short description
- [x] No `src/` / handler changes (G2 WAIVED → ES-05 backlog)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t10.md` signed (Date post P6 verify only)

## Where to change
- [`EPIC-M2-24-early-signal-pre-cluster.md`](../../../../EPIC-M2-24-early-signal-pre-cluster.md)
- [`gateway-mvp-dashboard.md`](../../../../gateway-mvp-dashboard.md)
- [`49-early-signal-network-pulse-l1-api.md`](../../../../../../requirements/49-early-signal-network-pulse-l1-api.md)
- [`openapi.yaml`](../../../../../../runtime-docs/api-reference/openapi.yaml) root `tags:`

## Out of scope
- R1/R2 (T08/T09); G2 handler try/except (ES-05); G3 SQL count (ES-06); pytest

## Verification commands
```bash
rg -n 'публичного.*Pulse|Pulse aggregate нет' doge-complaints-gateway/docs/tasks/epics/EPIC-M2-24-early-signal-pre-cluster.md
rg -n 'ES-02 In Progress' doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md
rg -n 'exclude.*internal|is_public_label_disposition|canonical' doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md
rg -n 'name: EarlySignal' doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml
```
