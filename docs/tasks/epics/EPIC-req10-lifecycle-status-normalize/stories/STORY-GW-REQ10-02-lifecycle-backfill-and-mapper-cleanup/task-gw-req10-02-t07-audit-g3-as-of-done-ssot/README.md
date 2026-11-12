# task-gw-req10-02-t07-audit-g3-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G3)

## Meta
- **Story:** [STORY-GW-REQ10-02](../STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000099 (parent product AC Done); wave `run_mode=gw_req10_02_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ10-02
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req10-02-lifecycle-backfill-2026-09-28.md`](../../../../../../analysis/audit-gw-req10-02-lifecycle-backfill-2026-09-28.md) **G3**
- **Scaffolded:** 2026-09-28T17:50:25Z
- **Completed:** 2026-09-28T17:52:28Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req10_02_gap_20260928T174919Z.plan.md` G3 TASKED follow_up=none

## Purpose
Закрыть G3 (LOW): T01/T03/T04 README Code Facts/Gap + pipeline Code touchpoints still present-tense pre-slim. Docs-only As-of-Done vs Historical. No product reopen. G1/G2 WAIVED operator (no §Актуальная точка rewrite; no hosted ops this task).

## Code Facts
1. Audit G3 — T01 Gap «still has RECEIVED»; T03 legacy dict `:185–188`; T04 debug `:190–221`; pipeline hydrate `:265` / parse `:179-224`.
2. Live product — `_parse_lifecycle_status` slim `db_supabase.py:179–185`; hydrate call `:226`; `rg src` clean of `debug-ba94c7` / `"RECEIVED"` map keys.
3. Gate PASS 2026-09-28T17:44:10Z; evidence AC-01 operator blocker documented.
4. **As-of-Done (P6 2026-09-28T17:52:28Z):** G3 CLOSED — T01/T03/T04 + pipeline touchpoints split As-of-Done vs Historical.
5. Pointer stays pkg-000099; product Story Done (AC-01…04 under gate framing).

## Gap
**G3 CLOSED:** present-tense pre-slim only in Historical rows.

## Acceptance / DoD
- [x] T01 README Code Facts/Gap: Historical vs As-of-Done (blocker path; no present-tense «still has RECEIVED until P3»)
- [x] T03 README Code Facts/Gap: Historical legacy dict vs As-of-Done slim `:179–185`
- [x] T04 README Code Facts/Gap: Historical debug block vs As-of-Done removed / `rg` clean
- [x] Pipeline Code touchpoints / Scope line numbers: parse `:179–185`, hydrate `:226`
- [x] T06 product gate **не** reopen
- [x] Product code/tests not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] G1 hosted residual **не** in scope (WAIVED operator)
- [x] `current.yaml` stays pkg-000099
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req10-02-t07.md` signed

## Where to change
- `task-gw-req10-02-t01-hosted-lifecycle-backfill/README.md`
- `task-gw-req10-02-t03-slim-lifecycle-mapper/README.md`
- `task-gw-req10-02-t04-remove-debug-io/README.md`
- Pipeline `STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md` Code touchpoints / Scope refs
- Bullrun T07 row + P6 registry (on close)

## Out of scope
Product reopen; hosted PATCH/ops (G1 WAIVED); invent new APIs; H8; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000099 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|RECEIVED|debug-ba94c7|:185|:190|:265' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t01-hosted-lifecycle-backfill/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t03-slim-lifecycle-mapper/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t04-remove-debug-io/README.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md
rg -n 'def _parse_lifecycle_status|_parse_lifecycle_status\(' doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
