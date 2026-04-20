# STORY-M2-02-03: Intake Idempotency Key Handling

## Meta
- Key: `STORY-M2-02-03`
- Parent Epic: [`EPIC-M2-02-story-intake-and-store.md`](../../EPIC-M2-02-story-intake-and-store.md)
- Type: Technical Story
- Status: Implemented (Waiting Commits)
- Stream: M2 Intake
- Skill declared: `python-pro` (for runtime implementation phase)

## Story Goal
Обеспечить детерминированную обработку повторных intake-команд через `Idempotency-Key`.

## Scope
- idempotency key policy и storage strategy;
- command handler dedup logic;
- deterministic response для повторов;
- race-safe tests на repeated intake.

## AC / DoD
- [ ] `Idempotency-Key` поддерживается в intake boundary.
- [ ] Повтор с тем же ключом не создает дубликат story.
- [ ] Повтор возвращает предсказуемый result/identifier.
- [ ] Конфликтные сценарии обрабатываются детерминированно.
- [ ] Тесты покрывают повторные и конкурентные вызовы baseline.

## Task Artifacts
- Task workspace: [`../../../task-m2-02-03-intake-idempotency-key-handling/README.md`](../../../task-m2-02-03-intake-idempotency-key-handling/README.md)
- Task specification: [`../../../task-m2-02-03-intake-idempotency-key-handling/task-m2-02-03-intake-idempotency-key-handling.md`](../../../task-m2-02-03-intake-idempotency-key-handling/task-m2-02-03-intake-idempotency-key-handling.md)
- Phase log: [`../../../task-m2-02-03-intake-idempotency-key-handling/BULLRUN-PHASE-LOG.md`](../../../task-m2-02-03-intake-idempotency-key-handling/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-02-03-intake-idempotency-key-handling/acceptance-verification-STORY-M2-02-03.md`](../../../task-m2-02-03-intake-idempotency-key-handling/acceptance-verification-STORY-M2-02-03.md)
