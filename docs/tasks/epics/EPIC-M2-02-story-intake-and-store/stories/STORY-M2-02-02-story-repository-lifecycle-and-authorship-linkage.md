# STORY-M2-02-02: Story Repository Lifecycle and Authorship Linkage

## Meta
- Key: `STORY-M2-02-02`
- Parent Epic: [`EPIC-M2-02-story-intake-and-store.md`](../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Intake
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Реализовать persistence-модель intake: immutable story narrative, lifecycle fields и авторство через `submitter` linkage.

## Scope
- story repository interface + in-memory/persistence baseline;
- lifecycle fields (`accepted`, readiness-related baseline);
- authorship linkage (`submitter.external_user_id`, optional issuer);
- tests на сохранение immutable narrative и linkage.

## AC / DoD
- [ ] Реализован story repository baseline.
- [ ] Original narrative сохраняется неизменно.
- [ ] Lifecycle поля сохранены и читаются предсказуемо.
- [ ] Авторство (`external_user_id`) сохраняется и доступно в чтении.
- [ ] Добавлены unit/integration tests для repository и linkage.

## Task Artifacts
- Task workspace: [`../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/README.md`](../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/README.md)
- Task specification: [`../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/task-m2-02-02-story-repository-lifecycle-and-authorship-linkage.md`](../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/task-m2-02-02-story-repository-lifecycle-and-authorship-linkage.md)
- Phase log: [`../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/BULLRUN-PHASE-LOG.md`](../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/acceptance-verification-STORY-M2-02-02.md`](../../../task-m2-02-02-story-repository-lifecycle-and-authorship-linkage/acceptance-verification-STORY-M2-02-02.md)
