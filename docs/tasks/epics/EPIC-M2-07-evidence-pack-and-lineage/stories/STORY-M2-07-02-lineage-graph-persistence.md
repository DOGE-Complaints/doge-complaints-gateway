# STORY-M2-07-02: Lineage graph persistence

## Meta
- Key: `STORY-M2-07-02`
- Parent Epic: [`EPIC-M2-07-evidence-pack-and-lineage.md`](../../EPIC-M2-07-evidence-pack-and-lineage.md)
- Type: Technical Story
- Status: Implemented (Waiting Commits)
- Stream: M2 Evidence
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Персистентность (in-memory baseline) lineage: issue → stories и обратный lookup по story.

## AC / DoD
- [x] Репозиторий evidence pack с save/get_by_issue.
- [x] Reverse index pack_ids по story_id.
- [x] Корректное обновление индекса при upsert.

## Task Artifacts
- Task workspace: [`../../../task-m2-07-02-lineage-graph-persistence/README.md`](../../../task-m2-07-02-lineage-graph-persistence/README.md)
- Task specification: [`../../../task-m2-07-02-lineage-graph-persistence/task-m2-07-02-lineage-graph-persistence.md`](../../../task-m2-07-02-lineage-graph-persistence/task-m2-07-02-lineage-graph-persistence.md)
- Phase log: [`../../../task-m2-07-02-lineage-graph-persistence/BULLRUN-PHASE-LOG.md`](../../../task-m2-07-02-lineage-graph-persistence/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-07-02-lineage-graph-persistence/acceptance-verification-STORY-M2-07-02.md`](../../../task-m2-07-02-lineage-graph-persistence/acceptance-verification-STORY-M2-07-02.md)
