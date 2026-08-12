# task-gw-draft-06-t07-audit-r1-story-status-sync

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000050)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_06_audit_followup`)
- **Depends on:** T01–T06 (P3 Done)
- **Audit ref:** [`audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11`](../../../../../../analysis/audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11.md) **R1**

## Purpose
Синхронизировать `Status:` в pipeline story и backlog story с фактом **Done** (gate T06 PASS, bullrun index/dashboard уже 🟢). Устранить status-drift без переписывания gate T06.

## Code Facts
- Pipeline drift — [`STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md:7`](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) `Status: ⚪ Todo`
- Backlog drift — [`STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) `:6` `Status: ⚪ Todo`
- Gate truth — [`story-acceptance-gate-STORY-GW-DRAFT-06.md`](../task-gw-draft-06-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-06.md) PASS 2026-07-11T10:15:42Z
- Index cross-check — [`backlog-stories/story-draft-handoff/INDEX.md`](../../../../backlog-stories/story-draft-handoff/INDEX.md) (already Done — do not regress)

## Acceptance / DoD
- [x] Pipeline story `Status:` reflects Done (aligned with gate/index)
- [x] Backlog story `Status:` reflects Done (aligned with gate/index)
- [x] No regression on INDEX row for GW-DRAFT-06
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-06-t07.md`](./acceptance-verification-gw-draft-06-t07.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md` — Meta `:7`
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md` — Meta `:6`

## Out of scope
- Rewriting T06 gate artifact
- P8 commits
- Runtime code or pytest

## Verification commands
```bash
rg 'Status:.*Todo' doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md
rg 'Status:.*Todo' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md
# expect 0 Todo on story Status after P6
```
