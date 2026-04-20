# STORY-M2-08-01: Canonical geo cache schema

## Meta
- Key: `STORY-M2-08-01`
- Parent Epic: [`../../EPIC-M2-08-geo-intelligence-module.md`](../../EPIC-M2-08-geo-intelligence-module.md)
- Type: Technical Story
- Status: Implemented (Waiting Commits)
- Stream: M2 Geo
- Skill declared: `python-pro`

## Story Goal
Зафиксировать канонический ключ кеша и in-memory хранилище георезолва без расхождения с доменной моделью.

## AC / DoD
- [x] `normalize_location_query`, `GeoCacheRepository`, `InMemoryGeoCacheRepository`.
- [x] Запись результата как `StoryGeoSnapshot` в домене.
- [x] Тест cache hit после повторного запроса.

## Task Artifacts
- Task workspace: [`../../../task-m2-08-01-canonical-geo-cache-schema/README.md`](../../../task-m2-08-01-canonical-geo-cache-schema/README.md)
- Task specification: [`../../../task-m2-08-01-canonical-geo-cache-schema/task-m2-08-01-canonical-geo-cache-schema.md`](../../../task-m2-08-01-canonical-geo-cache-schema/task-m2-08-01-canonical-geo-cache-schema.md)
- Phase log: [`../../../task-m2-08-01-canonical-geo-cache-schema/BULLRUN-PHASE-LOG.md`](../../../task-m2-08-01-canonical-geo-cache-schema/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-08-01-canonical-geo-cache-schema/acceptance-verification-STORY-M2-08-01.md`](../../../task-m2-08-01-canonical-geo-cache-schema/acceptance-verification-STORY-M2-08-01.md)
