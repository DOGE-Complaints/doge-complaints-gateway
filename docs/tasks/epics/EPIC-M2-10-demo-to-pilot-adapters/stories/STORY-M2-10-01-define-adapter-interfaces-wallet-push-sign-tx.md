# STORY-M2-10-01: Define adapter interfaces (wallet push / sign / tx)

## Meta
- Key: `STORY-M2-10-01`
- Parent Epic: [`../../EPIC-M2-10-demo-to-pilot-adapters.md`](../../EPIC-M2-10-demo-to-pilot-adapters.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Adapters
- Skill declared: `python-pro`

## Story Goal
Зафиксировать контракты адаптеров для внешних поверхностей (push, подпись, broadcast) без привязки к конкретной сети или транспорту.

## AC / DoD
- [x] `Protocol` для `WalletPushAdapter`, `SignRequestAdapter`, `TxBroadcastAdapter`.
- [x] Тип результата broadcast — `TxReceipt` (`tx_id`, `status`, `chain_profile`).
- [x] Импорты не тянут доменные сущности story/issue — только `core.adapters`.

## Task Artifacts
- Task workspace: [`../../../task-m2-10-01-define-adapter-interfaces/README.md`](../../../task-m2-10-01-define-adapter-interfaces/README.md)
- Task specification: [`../../../task-m2-10-01-define-adapter-interfaces/task-m2-10-01-define-adapter-interfaces.md`](../../../task-m2-10-01-define-adapter-interfaces/task-m2-10-01-define-adapter-interfaces.md)
- Phase log: [`../../../task-m2-10-01-define-adapter-interfaces/BULLRUN-PHASE-LOG.md`](../../../task-m2-10-01-define-adapter-interfaces/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-10-01-define-adapter-interfaces/acceptance-verification-STORY-M2-10-01.md`](../../../task-m2-10-01-define-adapter-interfaces/acceptance-verification-STORY-M2-10-01.md)
