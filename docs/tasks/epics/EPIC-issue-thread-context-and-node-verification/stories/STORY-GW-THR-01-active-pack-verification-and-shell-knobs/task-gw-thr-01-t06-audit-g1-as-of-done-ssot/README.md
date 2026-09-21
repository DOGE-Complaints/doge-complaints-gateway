# task-gw-thr-01-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for backlog/T01 SSOT (G1)

## Meta
- **Story:** [STORY-GW-THR-01](../STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000093 (parent product AC Done); wave `run_mode=gw_thr_01_audit_followup`
- **Skill declared:** code-documenter · fence loaded python-pro
- **Wave:** audit follow-up GW-THR-01
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-thr-01-active-pack-verification-and-shell-knobs-2026-09-21.md`](../../../../../../analysis/audit-gw-thr-01-active-pack-verification-and-shell-knobs-2026-09-21.md) **G1**
- **Scaffolded:** 2026-09-21T20:34:29Z
- **Completed:** 2026-09-21T20:35:45Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_thr_01_gap_20260921T203326Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified + Code touchpoints + T01 Code Facts still present-tense pre-P3 («Not found» / Unknown hooks). Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen product/sidecar unless drift.

## Code Facts
1. Audit G1 — backlog §Verified / Code touchpoints + T01 Code Facts were present-tense pre-P3.
2. Live product — `shell_capabilities.py` + `resolver.load_pack` → `load_shell_capabilities`; warehouse `shell_capabilities.json` 5/5; uus `phone`/`uus_phone_sms`; gate PASS 2026-09-21T20:29:51Z.
3. **As-of-Done (P6 2026-09-21T20:35:45Z):** G1 CLOSED — SSOT split As-of-Done vs Historical.
4. Pointer stays pkg-000093; product Story Done (AC-01…05).

## Gap
**G1 CLOSED:** present-tense pre-P3 only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Code touchpoints): As-of-Done vs Historical
- [x] T01 Code Facts As-of-Done (sidecar + resolver hooks)
- [x] T05 product gate **не** reopen
- [x] Product code/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000093
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-thr-01-t06.md` signed

## Where to change
- Backlog `STORY-GW-THR-01-….md` §Verified / Code touchpoints
- T01 README Code Facts
- Bullrun T06 row + P6 registry

## Out of scope
Product reopen; invent pack.json key strings / ThreadContext route; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000093 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|shell_capabilities' doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md
rg -n 'As-of-Done|shell_capabilities' doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/task-gw-thr-01-t01-shell-capability-contract/README.md
```
