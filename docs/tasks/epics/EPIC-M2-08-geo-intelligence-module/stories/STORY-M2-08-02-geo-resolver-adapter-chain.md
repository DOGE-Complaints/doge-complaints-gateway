# STORY-M2-08-02: GeoResolver adapter chain

## Meta
- Key: `STORY-M2-08-02`
- Parent Epic: [`../../EPIC-M2-08-geo-intelligence-module.md`](../../EPIC-M2-08-geo-intelligence-module.md)
- Type: Technical Story
- Status: Implemented (Waiting Commits)
- Stream: M2 Geo
- Skill declared: `python-pro`

## Story Goal
Цепочка провайдеров (policy: попытки на адаптер, затем fallback) с учётом метрик успеха/ошибки.

## AC / DoD
- [x] `GeoProvider`, `GeoResolverChain`, `GeoResolverPolicy`.
- [x] Демо-стабы OpenCage/Nominatim для Tallinn/Narva.
- [x] Тест fallback на втором провайдере для Narva.

## Task Artifacts
- Task workspace: [`../../../task-m2-08-02-geo-resolver-adapter-chain/README.md`](../../../task-m2-08-02-geo-resolver-adapter-chain/README.md)
- Task specification: [`../../../task-m2-08-02-geo-resolver-adapter-chain/task-m2-08-02-geo-resolver-adapter-chain.md`](../../../task-m2-08-02-geo-resolver-adapter-chain/task-m2-08-02-geo-resolver-adapter-chain.md)
- Phase log: [`../../../task-m2-08-02-geo-resolver-adapter-chain/BULLRUN-PHASE-LOG.md`](../../../task-m2-08-02-geo-resolver-adapter-chain/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-08-02-geo-resolver-adapter-chain/acceptance-verification-STORY-M2-08-02.md`](../../../task-m2-08-02-geo-resolver-adapter-chain/acceptance-verification-STORY-M2-08-02.md)
