# STORY-M2-09-01: Centralized config and env validation

## Meta
- Key: `STORY-M2-09-01`
- Parent Epic: [`../../EPIC-M2-09-security-config-observability.md`](../../EPIC-M2-09-security-config-observability.md)
- Type: Technical Story
- Status: Todo
- Stream: M2 Security/Ops
- Skill declared: `python-pro`

## Story Goal
Единая схема конфигурации и строгая валидация env при старте (fail-fast на критичных переменных).

## AC / DoD
- [ ] Расширение или укрепление `core.config` / `ENV_SCHEMA` под ops baseline эпика.
- [ ] Явная валидация при загрузке; понятные `ConfigError` сообщения.
- [ ] Тесты на валидный / невалидный env.

## Task Artifacts
- Task workspace: [`../../../task-m2-09-01-centralized-config-and-env-validation/README.md`](../../../task-m2-09-01-centralized-config-and-env-validation/README.md)
- Task specification: [`../../../task-m2-09-01-centralized-config-and-env-validation/task-m2-09-01-centralized-config-and-env-validation.md`](../../../task-m2-09-01-centralized-config-and-env-validation/task-m2-09-01-centralized-config-and-env-validation.md)
- Phase log: [`../../../task-m2-09-01-centralized-config-and-env-validation/BULLRUN-PHASE-LOG.md`](../../../task-m2-09-01-centralized-config-and-env-validation/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-09-01-centralized-config-and-env-validation/acceptance-verification-STORY-M2-09-01.md`](../../../task-m2-09-01-centralized-config-and-env-validation/acceptance-verification-STORY-M2-09-01.md)
