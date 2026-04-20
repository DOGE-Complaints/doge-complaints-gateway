# STORY-M2-10-02: Demo stub adapters

## Meta
- Key: `STORY-M2-10-02`
- Parent Epic: [`../../EPIC-M2-10-demo-to-pilot-adapters.md`](../../EPIC-M2-10-demo-to-pilot-adapters.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Adapters
- Skill declared: `python-pro`

## Story Goal
In-memory реализации интерфейсов с детерминированными идентификаторами (SHA-256 digest, усечённый hex) для demo и pilot профилей без реальной сети.

## AC / DoD
- [x] `DemoWalletPushAdapter`, `DemoSignRequestAdapter`, `DemoTxBroadcastAdapter` реализуют соответствующие протоколы.
- [x] Идентификаторы зависят от `DeploymentProfile` (различаются demo vs pilot при одинаковых входах).
- [x] `TxReceipt.chain_profile` совпадает со значением профиля конфигурации.

## Task Artifacts
- Task workspace: [`../../../task-m2-10-02-demo-stub-adapters/README.md`](../../../task-m2-10-02-demo-stub-adapters/README.md)
- Task specification: [`../../../task-m2-10-02-demo-stub-adapters/task-m2-10-02-demo-stub-adapters.md`](../../../task-m2-10-02-demo-stub-adapters/task-m2-10-02-demo-stub-adapters.md)
- Phase log: [`../../../task-m2-10-02-demo-stub-adapters/BULLRUN-PHASE-LOG.md`](../../../task-m2-10-02-demo-stub-adapters/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-10-02-demo-stub-adapters/acceptance-verification-STORY-M2-10-02.md`](../../../task-m2-10-02-demo-stub-adapters/acceptance-verification-STORY-M2-10-02.md)
- Test qualification: [`../../../task-m2-10-02-demo-stub-adapters/test-qualification-STORY-M2-10-02.md`](../../../task-m2-10-02-demo-stub-adapters/test-qualification-STORY-M2-10-02.md)
