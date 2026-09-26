# task-gw-thr-03-t04-cutover-evidence

## Task: docs — Cutover evidence (T04)

## Meta
- **Story:** [STORY-GW-THR-03](../STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000095
- **Skill declared:** python-pro
- **Depends on:** T01–T03 (evidence after gate cutover code lands)
- **Scaffolded:** 2026-09-21T21:00:02Z
- **Completed:** 2026-09-21T21:05:11Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md`

## Purpose
Ordered-deploy / evidence note: identity VB-01/02 (+ backfill) before gateway gate cutover; no dual-read feature flag. Scope #5 · AC-GW-THR03-04.

## Code Facts
1. Operator FACT: Identity VB-01 Done pkg-000050; VB-02 Done pkg-000051.
2. Identity migrations on disk (sibling repo): `doge-identity-service/supabase/migrations/20260921000001_profiles_identity_verified.sql`, `…00002_…_backfill.sql`.
3. Gateway must ignore legacy method flags for allow after cutover (T02).
4. No phone dual-read feature flag in scope (operator lock).

## Gap
**Closed (P3 2026-09-21T21:05:11Z):** gap addressed in implement-wave.

## Acceptance / DoD
- [x] Evidence note records VB-01/02 Done + backfill path / apply status (AC-GW-THR03-04)
- [x] States gateway allow ignores legacy method flags (no dual-read)
- [x] Ordered launch: identity expose+migration before gate cutover
- [x] No invent public auth route / no §Актуальная точка rewrite
- [x] BULLRUN phases complete when closed

## Where to change
- This task folder evidence artifact (P3) — e.g. `cutover-evidence.md` or acceptance-verification body
- Optional cross-link to identity migration paths (do not edit identity package in this task)

## Out of scope
Running identity migrations from gateway; VB-03 live verify set; invent public auth route; phone dual-read flag; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **identity_verified only** — no `phone_verified` dual-read / fallback.
  - Fail-closed if opaque missing/invalid when gate runs.
  - Do **not invent** public gateway auth route.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093/094; pointer is pkg-000095.

## Verification commands
```bash
ls doge-identity-service/supabase/migrations/*identity_verified*
rg -n 'phone_verified|identity_verified' doge-complaints-gateway/src/core/identity/verification_gate.py
```
