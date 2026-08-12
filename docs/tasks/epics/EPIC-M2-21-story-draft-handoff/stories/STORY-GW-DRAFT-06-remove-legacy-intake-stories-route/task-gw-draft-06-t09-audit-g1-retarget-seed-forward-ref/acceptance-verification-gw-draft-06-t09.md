# Acceptance verification — task-gw-draft-06-t09-audit-g1-retarget-seed-forward-ref

- **Task:** T09 audit G1 retarget SEED forward-ref (doc-only)
- **Status:** PASS
- **Date:** 2026-07-11

## Checklist

- [x] Pipeline Decision Ref points to GW-SEED-03 (not GW-SEED-01) for runner submit/cluster
- [x] Backlog GW-DRAFT-06 forward-refs retargeted (`:11`, «Открытые вопросы» `:62`)
- [x] [`STORY-GW-SEED-03.md`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) `:22` — no stale `/intake/stories`; runner stash-only noted
- [x] Audit G1 doc traceability ([`audit-gw-draft-06-...`](../../../../../../analysis/audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11.md) §G1)

## Live verification

```bash
rg 'GW-SEED-01' doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md || test $? -eq 1
rg 'GW-SEED-01' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md || test $? -eq 1
rg '/intake/stories' doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md || test $? -eq 1
```

→ GW-SEED-01 = 0 in GW-DRAFT-06 pipeline+backlog; SEED-03 no `/intake/stories`
