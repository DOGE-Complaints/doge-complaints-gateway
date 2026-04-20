# STORY-M2-10-03: Feature-flag snapshot and adapter bundle registry

## Meta
- Key: `STORY-M2-10-03`
- Parent Epic: [`../../EPIC-M2-10-demo-to-pilot-adapters.md`](../../EPIC-M2-10-demo-to-pilot-adapters.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Adapters
- Skill declared: `python-pro`

## Story Goal
Единая точка сборки адаптеров из `AppConfig` и наблюдаемый снимок флагов/профиля для тестов и логирования без дублирования логики переключения.

## AC / DoD
- [x] `AdapterBundle` группирует три адаптера; `build_adapter_bundle(config)` использует текущий `DeploymentProfile`.
- [x] `adapter_runtime_flags(config)` возвращает `deployment_profile`, `wallet_adapter`, `blockchain_adapter`, `tokenization_pipeline` из `AppConfig`.
- [x] Pilot-профиль пока использует те же stub-классы; точка расширения — замена реализаций в `build_adapter_bundle` без смены протоколов.

## Task Artifacts
- Task workspace: [`../../../task-m2-10-03-feature-flag-registry-and-bundle/README.md`](../../../task-m2-10-03-feature-flag-registry-and-bundle/README.md)
- Task specification: [`../../../task-m2-10-03-feature-flag-registry-and-bundle/task-m2-10-03-feature-flag-registry-and-bundle.md`](../../../task-m2-10-03-feature-flag-registry-and-bundle/task-m2-10-03-feature-flag-registry-and-bundle.md)
- Phase log: [`../../../task-m2-10-03-feature-flag-registry-and-bundle/BULLRUN-PHASE-LOG.md`](../../../task-m2-10-03-feature-flag-registry-and-bundle/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-10-03-feature-flag-registry-and-bundle/acceptance-verification-STORY-M2-10-03.md`](../../../task-m2-10-03-feature-flag-registry-and-bundle/acceptance-verification-STORY-M2-10-03.md)
- Test qualification: [`../../../task-m2-10-03-feature-flag-registry-and-bundle/test-qualification-STORY-M2-10-03.md`](../../../task-m2-10-03-feature-flag-registry-and-bundle/test-qualification-STORY-M2-10-03.md)
