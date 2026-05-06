# STORY-M2-17-01: Living issues create/extend orchestration

## Meta
- Key: `STORY-M2-17-01`
- Parent Epic: [`../../../EPIC-M2-17-living-issues-cluster-growth-model.md`](../../../EPIC-M2-17-living-issues-cluster-growth-model.md)
- Type: Technical Story
- Status: In Progress (Audit gap closure wave)
- Stream: M2 Living Issue Growth
- Requirement reference: [`29-living-issues-cluster-growth-model.md`](../../../../../requirements/29-living-issues-cluster-growth-model.md)
- Skill declared: `python-pro`

## Story Goal
Внедрить living model: при повторной обработке того же `cluster_id` issue расширяется (extend path), а не дублируется новым create path.

## AC / DoD
- [x] AC-29-1: два последовательных прогона с одним `cluster_id` создают один issue.
- [x] AC-29-2: issue содержит story_ids из обеих волн.
- [x] AC-29-3: `review_audit_log` фиксирует `cluster_growth_extend` на каждый extend.
- [x] AC-29-4: `DOGEIssue` проекция после extend перестроена на полном наборе story_ids.
- [x] AC-29-5: idempotent extend без новых stories не создаёт дублей и лишних изменений score.
- [x] AC-29-6: все stories обеих волн в статусе `CLUSTERED`.

## Nested tasks

| Order | Slug | Task folder |
|-------|------|-------------|
| 1 | primary | `task-m2-17-01-living-issues-primary` |
| 2 | T03 | `task-m2-17-01-t03-projection-embedding-upsert-invariants` |
| 3 | T04 | `task-m2-17-01-t04-issue-story-links-dedup-contract` |
| 4 | T01 | `task-m2-17-01-t01-promotion-extend-primitive` |
| 5 | T02 | `task-m2-17-01-t02-issue-create-create-extend-split` |
| 6 | T05 | `task-m2-17-01-t05-candidate-lookup-update-backend-parity` |
| 7 | T06 | `task-m2-17-01-t06-issue-create-service-tests` |
| 8 | T07 | `task-m2-17-01-t07-e2e-living-issue-two-batches` |
| 9 | T08 | `task-m2-17-01-t08-audit-trail-extend-events-test` |
| 10 | T09 | `task-m2-17-01-t09-embedding-upsert-atomicity` |
| 11 | T10 | `task-m2-17-01-t10-e2e-clustered-status-ac29-6` |
| 12 | T11 | `task-m2-17-01-t11-sqlite-extend-parity-test` |
| 13 | T12 | `task-m2-17-01-t12-projection-content-invariant` |

## Task Artifacts
- primary: [`./task-m2-17-01-living-issues-primary/README.md`](./task-m2-17-01-living-issues-primary/README.md)
- T03: [`./task-m2-17-01-t03-projection-embedding-upsert-invariants/README.md`](./task-m2-17-01-t03-projection-embedding-upsert-invariants/README.md)
- T04: [`./task-m2-17-01-t04-issue-story-links-dedup-contract/README.md`](./task-m2-17-01-t04-issue-story-links-dedup-contract/README.md)
- T01: [`./task-m2-17-01-t01-promotion-extend-primitive/README.md`](./task-m2-17-01-t01-promotion-extend-primitive/README.md)
- T02: [`./task-m2-17-01-t02-issue-create-create-extend-split/README.md`](./task-m2-17-01-t02-issue-create-create-extend-split/README.md)
- T05: [`./task-m2-17-01-t05-candidate-lookup-update-backend-parity/README.md`](./task-m2-17-01-t05-candidate-lookup-update-backend-parity/README.md)
- T06: [`./task-m2-17-01-t06-issue-create-service-tests/README.md`](./task-m2-17-01-t06-issue-create-service-tests/README.md)
- T07: [`./task-m2-17-01-t07-e2e-living-issue-two-batches/README.md`](./task-m2-17-01-t07-e2e-living-issue-two-batches/README.md)
- T08: [`./task-m2-17-01-t08-audit-trail-extend-events-test/README.md`](./task-m2-17-01-t08-audit-trail-extend-events-test/README.md)
- T09: [`./task-m2-17-01-t09-embedding-upsert-atomicity/README.md`](./task-m2-17-01-t09-embedding-upsert-atomicity/README.md)
- T10: [`./task-m2-17-01-t10-e2e-clustered-status-ac29-6/README.md`](./task-m2-17-01-t10-e2e-clustered-status-ac29-6/README.md)
- T11: [`./task-m2-17-01-t11-sqlite-extend-parity-test/README.md`](./task-m2-17-01-t11-sqlite-extend-parity-test/README.md)
- T12: [`./task-m2-17-01-t12-projection-content-invariant/README.md`](./task-m2-17-01-t12-projection-content-invariant/README.md)
- Acceptance (story): [`./task-m2-17-01-living-issues-primary/acceptance-verification-STORY-M2-17-01.md`](./task-m2-17-01-living-issues-primary/acceptance-verification-STORY-M2-17-01.md)
- Phase log (story): [`./task-m2-17-01-living-issues-primary/BULLRUN-PHASE-LOG.md`](./task-m2-17-01-living-issues-primary/BULLRUN-PHASE-LOG.md)
