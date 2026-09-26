# task-gw-thr-02-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for backlog/T01/T02 SSOT (G1)

## Meta
- **Story:** [STORY-GW-THR-02](../STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000094 (parent product AC Done); wave `run_mode=gw_thr_02_audit_followup`
- **Skill declared:** code-documenter · fence loaded python-pro
- **Wave:** audit follow-up GW-THR-02
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-thr-02-service-auth-pack-shell-settings-pull-2026-09-21.md`](../../../../../../analysis/audit-gw-thr-02-service-auth-pack-shell-settings-pull-2026-09-21.md) **G1**
- **Scaffolded:** 2026-09-21T20:53:24Z
- **Completed:** 2026-09-21T20:54:56Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_thr_02_gap_20260921T205228Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified + Code touchpoints + T01/T02 Code Facts still present-tense pre-P3 («Unknown / absent» / «No settings DTO» / «route absent»). Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen product/`GET /node/shell-settings` unless drift.

## Code Facts
1. Audit G1 — backlog §Verified / Code touchpoints + T01/T02 Code Facts were present-tense pre-P3.
2. Live product — `shell_settings.py` + `asgi_app.py` `GET /node/shell-settings` + `require_public_content_service_auth`; gate PASS 2026-09-21T20:48:13Z; Issue get still `{"issue": projection}` (~510–514).
3. **As-of-Done (P6 2026-09-21T20:54:56Z):** G1 CLOSED — SSOT split As-of-Done vs Historical on backlog + T01/T02.
4. Pointer stays pkg-000094; product Story Done (AC-01…05).

## Gap
**G1 CLOSED:** present-tense pre-P3 only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Code touchpoints): As-of-Done vs Historical; Issue get cite → get handler; path fact `GET /node/shell-settings`
- [x] T01 Code Facts As-of-Done vs Historical (remove contradictory «No settings DTO»)
- [x] T02 Code Facts As-of-Done vs Historical (remove contradictory «route absent»)
- [x] T05 product gate **не** reopen
- [x] Product code/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000094
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-thr-02-t06.md` signed

## Where to change
- Backlog `STORY-GW-THR-02-….md` §Verified / Code touchpoints
- T01 + T02 README Code Facts
- Bullrun T06 row + P6 registry

## Out of scope
Product reopen; invent public ThreadContext route; invent path into REQ; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000094 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|shell-settings|Unknown' doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md
rg -n 'As-of-Done|Historical|shell_settings' doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t01-settings-payload-from-active-pack/README.md doge-complaints-gateway/docs/tasks/epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t02-service-auth-read-wire/README.md
```
