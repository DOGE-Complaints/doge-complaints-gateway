# task-gw-draft-06-t09-audit-g1-retarget-seed-forward-ref

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** audit override (not in pkg-000050)
- **Skill declared:** python-pro
- **Wave:** audit override (`run_mode=gw_draft_06_audit_followup`)
- **Depends on:** T01–T06 (P3 Done)
- **Audit ref:** [`audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11`](../../../../../../analysis/audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11.md) **G1 doc**

## Purpose
Убрать dangling forward-ref на **Done** [GW-SEED-01](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-01-loader-and-hosted-readiness.md) для runner submit/cluster path; указать [GW-SEED-03](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) как владельца runner E2E materialization. Обновить stale строку SEED-03 `:22` (runner уже на `/story-drafts` stash-only).

## Code Facts
- Pipeline Decision Ref — [`STORY-GW-DRAFT-06...pipeline.md:10`](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) → GW-SEED-01
- Backlog refs — [`STORY-GW-DRAFT-06...backlog.md`](../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) `:11`, «Швы» `:62`
- SEED-03 stale — [`STORY-GW-SEED-03.md:22`](../../../../backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md) still says `/intake/stories`
- Runner as-is — [`simulation_runner.py:203`](../../../../../../../tests/simulation_runner.py) stash-only by design (G1 impl → `activation: none`)

## Acceptance / DoD
- [x] No forward-ref to GW-SEED-01 for runner submit/cluster in pipeline + backlog GW-DRAFT-06
- [x] GW-SEED-03 referenced as owner of runner E2E materialization (doc-only)
- [x] SEED-03 `:22` updated (runner on `/story-drafts`, stash-only; submit → SEED-03 scope)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-06-t09.md`](./acceptance-verification-gw-draft-06-t09.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/.../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md` — Decision Ref `:10`, «Открытые вопросы» / «Швы» if needed
- `doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md` — `:11`, «Швы» `:62`
- `doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md` — `:22`

## Out of scope
- Changing `simulation_runner.py` (submit flow — GW-SEED-03 G1 impl, `activation: none`)
- Hosted smoke

## Verification commands
```bash
rg 'GW-SEED-01' doge-complaints-gateway/docs/tasks/epics/EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md
rg 'GW-SEED-01' doge-complaints-gateway/docs/tasks/backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md
# expect 0 dangling submit/cluster refs to SEED-01; historical depends OK if scoped
rg '/intake/stories' doge-complaints-gateway/docs/tasks/backlog-stories/demo-data-seeding/STORY-GW-SEED-03-end-to-end-seed-runbook.md || test $? -eq 1
```
