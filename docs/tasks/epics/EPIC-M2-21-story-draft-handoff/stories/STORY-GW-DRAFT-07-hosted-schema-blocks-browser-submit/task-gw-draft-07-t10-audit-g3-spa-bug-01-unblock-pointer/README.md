# task-gw-draft-07-t10-audit-g3-spa-bug-01-unblock-pointer

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000057
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-DRAFT-07
- **Depends on:** T01–T06 Done (gateway blocker cleared)
- **Audit ref:** [`audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md`](../../../../../../analysis/audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md) **G3**

## Purpose
Зафиксировать на стороне SPA backlog, что gateway blocker DRAFT-07 **Done** — SPA-BUG-01 / FE-HANDOFF-03 могут закрыть regression (retest submit → 202). Не выполнять SPA P3 / не менять SPA UI.

## Code Facts
- SPA story — [`STORY-SPA-BUG-01-story-submission-unavailable.md`](../../../../../../../../spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md) Status Todo; Related gateway still reads as blocker waiting Done
- Gateway Done — DRAFT-07 gate PASS; [`evidence-STORY-GW-DRAFT-07-…`](../../../../../../analysis/evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md)
- Pin — [`pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md`](../../../../../../../../spa-app/docs/analysis/pin-STORY-SPA-BUG-01-root-cause-2026-08-06.md) T03 next = DRAFT-07 then SPA retest

## Acceptance / DoD
- [x] SPA-BUG-01 Meta/Related: gateway blocker marked **Done** (pkg-000056); SPA T03+ unblocked for retest
- [x] No claim that schema readiness still blocks submit
- [x] Gateway DRAFT-07 **not** reopened; no SPA src changes in this task
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t10.md`](./acceptance-verification-gw-draft-07-t10.md) signed (Date post P6 verify only)

## Where to change
- `spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md` (Related / notes)
- Optional: spa pin «T03 next» one-liner that DRAFT-07 Done

## Out of scope
- SPA P3 execute / UI hotfix / pkg-000053 task implementation
- Changing gateway `src/`

## Verification commands
```bash
rg 'GW-DRAFT-07|DRAFT-07' spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md
rg 'Done|pkg-000056|unblocked|retest' spa-app/docs/tasks/backlog-stories/bugs/STORY-SPA-BUG-01-story-submission-unavailable.md
```
