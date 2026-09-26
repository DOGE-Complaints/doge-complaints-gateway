# task-gw-req9-01-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000096 (parent product AC Done); wave `run_mode=gw_req9_01_audit_followup`
- **Skill declared:** code-documenter · fence loaded python-pro
- **Wave:** audit follow-up GW-REQ9-01
- **Depends on:** T01–T05 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req9-01-example-env-and-spa-base-url-2026-09-26.md`](../../../../../../analysis/audit-gw-req9-01-example-env-and-spa-base-url-2026-09-26.md) **G1**
- **Scaffolded:** 2026-09-26T12:11:17Z
- **Completed:** 2026-09-26T12:12:27Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req9_01_gap_20260926T121033Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog/pipeline §Verified + T01–T03 Code Facts/Gap present-tense pre-P3. Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — backlog/pipeline §Verified + T01–T03 Code Facts were present-tense pre-P3 (`SPA_VERIFY_*` / «lacks keys»).
2. Live product — `SPA_BASE_URL` / `spa_base_url` / `resolve_spa_base_url`; `example.env` keys; gate PASS 2026-09-26T12:06:30Z.
3. **As-of-Done (P6 2026-09-26T12:12:27Z):** G1 CLOSED — SSOT split As-of-Done vs Historical on backlog/pipeline §Verified + T01–T03.
4. Pointer stays pkg-000096; product Story Done (AC-01…05).

## Gap
**G1 CLOSED:** present-tense pre-P3 only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (keys present; `SPA_BASE_URL` / `spa_base_url`; tests set `SPA_BASE_URL`)
- [x] Pipeline §Verified: same As-of-Done vs Historical split
- [x] T01 Code Facts/Gap: Historical vs As-of-Done — remove present-tense «No IDENTITY/SPA keys» / «Template missing»
- [x] T02 Code Facts/Gap: Historical vs As-of-Done — live `spa_base_url` / `SPA_BASE_URL` only
- [x] T03 Code Facts/Gap: Historical vs As-of-Done — `resolve_spa_base_url` shipped
- [x] T05 product gate **не** reopen
- [x] Product code/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000096
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req9-01-t06.md` signed

## Where to change
- Backlog `STORY-GW-REQ9-01-….md` §Verified
- Pipeline `STORY-GW-REQ9-01-….md` §Verified
- T01–T03 README Code Facts / Gap
- Bullrun T06 row + P6 registry

## Out of scope
Product reopen; invent Railway service ids; dual-read; REQ9-02 make test; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000096 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|SPA_VERIFY|spa_verify|SPA_BASE_URL' doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/STORY-GW-REQ9-01-example-env-and-spa-base-url.md
rg -n 'As-of-Done|Historical|SPA_VERIFY|spa_verify' doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/task-gw-req9-01-t01-example-env-keys/README.md doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/task-gw-req9-01-t02-schema-spa-base-hard-cut/README.md doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-01-example-env-and-spa-base-url/task-gw-req9-01-t03-verify-url-helpers/README.md
```
