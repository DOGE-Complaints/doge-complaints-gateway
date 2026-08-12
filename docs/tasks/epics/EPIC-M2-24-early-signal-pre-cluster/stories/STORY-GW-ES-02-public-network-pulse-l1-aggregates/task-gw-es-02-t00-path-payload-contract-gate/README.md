# task-gw-es-02-t00-path-payload-contract-gate

## Meta
- **Story:** [STORY-GW-ES-02](../STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- **Type:** gate / docs
- **Status:** 🟢 Done
- **Package:** pkg-000059
- **Skill declared:** python-pro
- **Depends on:** —
- **decision_ref:** backlog ES-02 AC T00; REQ-48 AC-GW-ES-02 (no route from Draft-48 alone)

## Purpose
Зафиксировать **path + payload** contract в follow-on gateway REQ (new NN) **или** ADR. Без Done этого таска — **stop before T03** (не invent path в story body).

## Code Facts
- No Pulse route today — [`asgi_app.py:57-64`](../../../../../../../../src/core/api/asgi_app.py) `PUBLIC_ROUTES`
- REQ-48 forbids inventing route from Draft-48 alone — [`48-early-signal-pre-cluster-data-readiness.md`](../../../../../../../requirements/48-early-signal-pre-cluster-data-readiness.md)
- Gap G-ES-PUB-01 — [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](../../../../../../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md)
- spa-15 sibling path TBD — [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md)

## Acceptance / DoD
- [x] Traces parent AC: T00 follow-on REQ/ADR names path + payload
- [x] Artifact exists under `docs/requirements/` (new NN) **or** `docs/analysis/` ADR with explicit path string + payload schema keys
- [x] Pipeline/backlog story body does **not** invent a path literal as SSOT
- [x] T03/T06 blocked until this Done (noted in Depends)
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-es-02-t00.md` signed (Date post P3 verify only)

## Where to change
- New REQ under `doge-complaints-gateway/docs/requirements/` **or** ADR under `doge-complaints-gateway/docs/analysis/`
- Pointers in this task acceptance artifact; optional soft link from TASK-GW-ES-04

## Out of scope
- Implementing handler/route (T03); inventing path only in this story file; ES-03; spa layout

## Verification commands
```bash
# After artifact exists — cite path+payload from REQ/ADR (example once named):
rg -n 'path|Network Pulse|payload' doge-complaints-gateway/docs/requirements/ doge-complaints-gateway/docs/analysis/ | head -40
rg -n 'PUBLIC_ROUTES' doge-complaints-gateway/src/core/api/asgi_app.py
```
