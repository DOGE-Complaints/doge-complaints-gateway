# task-gw-req11-03-t05-operator-docs-no-spa

## Task: docs — Pass path API+JSON; no SPA login (T05)

## Meta
- **Story:** [STORY-GW-REQ11-03](../STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000102
- **Skill declared:** python-pro
- **Depends on:** T01–T04 (prefer tooling paths named)
- **Scaffolded:** 2026-09-29T14:13:56Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-03-profiled-api-replay-multi-submitter.md`

## Purpose
Document Pass path = API+JSON + pool map; **no SPA resident login** (K1/K4). Makefile/`make simulate` handoff as fit. Scope #4 · AC-GW-REQ1103-04.

## Code Facts
1. Make `simulate`: `Makefile:31-32`.
2. Profile selection note exists (REQ11-02): `docs/analysis/note-gw-req11-02-profile-selection-2026-09-29.md`.
3. Single-user SPA phone_verified messaging still in `simulation_intake_http.py:106-109`.
4. Operator lock: no SPA login per run (INDEX).

## Gap
**As-of-Done (P3):** closed — see gate + run-summary.

**Historical:**
No REQ11-03 operator doc stating Pass = profiled API replay + pool; SPA not required.

## Acceptance / DoD
- [x] Documented Pass path without SPA resident login (AC-GW-REQ1103-04)
- [x] Primary path documented as API+JSON (K4)
- [x] Cross-links profiles + fixtures + pool/map
- [x] BULLRUN phases complete when closed

## Where to change
- Short note under `doge-complaints-gateway/docs/analysis/` and/or runtime testing docs (P3)
- Optional Makefile comment / simulate handoff

## Out of scope
Implement Identity SPA accounts; backdate; threads; invent APIs.
- Overlay bans:
  - Stay `dev`.
  - Pointer pkg-000102.
  - No secrets in git.

## Verification commands
```bash
rg -n 'SPA|pool|replay|Pass|DEMO_LIFE_SIM' doge-complaints-gateway/docs/analysis --glob '*req11*' | head -40
```
