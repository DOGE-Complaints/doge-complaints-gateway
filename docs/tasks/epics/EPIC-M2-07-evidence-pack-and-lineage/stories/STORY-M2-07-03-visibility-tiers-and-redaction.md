# STORY-M2-07-03: Visibility tiers and redaction

## Meta
- Key: `STORY-M2-07-03`
- Parent Epic: [`EPIC-M2-07-evidence-pack-and-lineage.md`](../../EPIC-M2-07-evidence-pack-and-lineage.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Evidence
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Реализовать `VisibilityTier` и redaction: public / internal / export без утечки лишних полей в public.

## AC / DoD
- [x] Три уровня доступа.
- [x] Public summary без `supporting_artifact_refs`.
- [x] Тесты на форму public view.

## Task Artifacts
- Task workspace: [`../../../task-m2-07-03-visibility-tiers-and-redaction/README.md`](../../../task-m2-07-03-visibility-tiers-and-redaction/README.md)
- Task specification: [`../../../task-m2-07-03-visibility-tiers-and-redaction/task-m2-07-03-visibility-tiers-and-redaction.md`](../../../task-m2-07-03-visibility-tiers-and-redaction/task-m2-07-03-visibility-tiers-and-redaction.md)
- Phase log: [`../../../task-m2-07-03-visibility-tiers-and-redaction/BULLRUN-PHASE-LOG.md`](../../../task-m2-07-03-visibility-tiers-and-redaction/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-07-03-visibility-tiers-and-redaction/acceptance-verification-STORY-M2-07-03.md`](../../../task-m2-07-03-visibility-tiers-and-redaction/acceptance-verification-STORY-M2-07-03.md)
