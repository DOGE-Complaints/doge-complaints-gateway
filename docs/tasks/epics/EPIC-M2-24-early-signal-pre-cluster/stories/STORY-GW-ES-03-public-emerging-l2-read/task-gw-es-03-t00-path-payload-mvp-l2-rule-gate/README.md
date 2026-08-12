# task-gw-es-03-t00-path-payload-mvp-l2-rule-gate

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** gate / docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-08-10T12:06:12Z
- **decision_ref:** backlog ES-03 AC T00; REQ-48 §4.6 / open Q2; gap G-ES-PUB-03

## Purpose
Зафиксировать **path + payload** (incl. `top_n` / axis defaults) в follow-on gateway REQ (new NN, e.g. 50) **или** ADR, и задокументировать MVP L2 rule (story §) as Q2 close. Без Done — **stop before T03/T06** (не invent path в story body).

## Code Facts
- No emerging route — [`asgi_app.py:58–66`](../../../../../../../../src/core/api/asgi_app.py) `PUBLIC_ROUTES` has pulse, not emerging
- Pulse path etalon — REQ-49 [`49-early-signal-network-pulse-l1-api.md`](../../../../../../../requirements/49-early-signal-network-pulse-l1-api.md)
- Gap L2 Public=N — [`gap-analysis…§3`](../../../../../../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md) G-ES-PUB-03
- MVP rule SSOT — pipeline/backlog §«MVP derivation rule»
- spa-15 Emerging block — [`15-early-signal-pre-cluster-public-dashboard.md`](../../../../../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md)

## Acceptance / DoD
- [ ] Traces story AC: T00 path+payload named outside story file alone
- [ ] Artifact under `docs/requirements/` (new NN) **or** `docs/analysis/` ADR with explicit path string + payload schema keys + MVP L2 rule / Q2 close
- [ ] Pipeline/backlog story body does **not** invent a path literal as SSOT
- [ ] T03/T06 blocked until this Done (noted in Depends)
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t00.md` signed (Date post P3 verify only)

## Where to change
- New REQ under `doge-complaints-gateway/docs/requirements/` **or** ADR under `docs/analysis/`
- Optional soft link from TASK-GW-ES-04 / README-index

## Out of scope
- Implementing handler/route (T03); inventing path only in this story file; Pulse L1; spa layout

## Verification commands
```bash
rg -n 'Emerging|emerging|path|top_n' doge-complaints-gateway/docs/requirements/ doge-complaints-gateway/docs/analysis/ | head -40
rg -n 'PUBLIC_ROUTES|emerging' doge-complaints-gateway/src/core/api/asgi_app.py
```
