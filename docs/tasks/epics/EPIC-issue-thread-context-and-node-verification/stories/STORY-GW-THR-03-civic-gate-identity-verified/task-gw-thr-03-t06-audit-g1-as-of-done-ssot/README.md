# task-gw-thr-03-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for T01/T02 + pipeline SSOT (G1)

## Meta
- **Story:** [STORY-GW-THR-03](../STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000095 (parent product AC Done); wave `run_mode=gw_thr_03_audit_followup`
- **Skill declared:** code-documenter · fence loaded python-pro
- **Wave:** audit follow-up GW-THR-03
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-thr-03-civic-gate-identity-verified-2026-09-21.md`](../../../../../../analysis/audit-gw-thr-03-civic-gate-identity-verified-2026-09-21.md) **G1**
- **Scaffolded:** 2026-09-21T21:09:59Z
- **Completed:** 2026-09-21T21:11:23Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_thr_03_gap_20260921T210918Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01/T02 Code Facts + pipeline Code touchpoints / As-is gap present-tense pre-P3. Docs-only As-of-Done vs Historical. Backlog §Verified already OK. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — T01/T02 Code Facts + pipeline residual were present-tense pre-P3.
2. Live product — opaque-only gate + parse; gate PASS 2026-09-21T21:05:11Z; tests `test_gw_thr_03_*` + `test_gw_gauth_03_*`.
3. **As-of-Done (P6 2026-09-21T21:11:23Z):** G1 CLOSED — SSOT split As-of-Done vs Historical on T01/T02 + pipeline.
4. Pointer stays pkg-000095; product Story Done (AC-01…04). Backlog Verified already As-of-Done (no drift).

## Gap
**G1 CLOSED:** present-tense pre-P3 only in Historical rows.

## Acceptance / DoD
- [x] T01 Code Facts: As-of-Done vs Historical (remove «No identity_verified yet» / «Gate still consumes phone»)
- [x] T02 Code Facts: As-of-Done vs Historical (remove phone hard-code present-tense; reason = Identity verification…)
- [x] Pipeline Code touchpoints: known tests listed; As-of-Done
- [x] Pipeline As-is gap / residual: Historical only — product closed
- [x] T05 product gate **не** reopen
- [x] Product code/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000095
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-thr-03-t06.md` signed

## Where to change
- T01 + T02 README Code Facts
- Pipeline `STORY-GW-THR-03-….md` Code touchpoints / As-is gap
- Bullrun T06 row + P6 registry

## Out of scope
Product reopen; invent public auth route; phone dual-read; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000095 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|identity_verified|phone_verified' doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t01-me-parse-identity-verified/README.md doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t02-gate-opaque-only/README.md
rg -n 'Unknown|As-is gap|test_gw_thr_03' doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/STORY-GW-THR-03-civic-gate-identity-verified.md
```
