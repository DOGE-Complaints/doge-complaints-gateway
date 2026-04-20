# STORY-M2-08-03: GeoService in intake pipeline

## Meta
- Key: `STORY-M2-08-03`
- Parent Epic: [`../../EPIC-M2-08-geo-intelligence-module.md`](../../EPIC-M2-08-geo-intelligence-module.md)
- Type: Technical Story
- Status: Implemented (Waiting Commits)
- Stream: M2 Geo
- Skill declared: `python-pro`

## Story Goal
Опциональное поле `narrative.location_query` в intake и запись `StoryRecord.geo` без поломки существующих клиентов.

## AC / DoD
- [x] Парсинг `location_query` в `parse_story_intake_request`.
- [x] `StoryIntakeService` с опциональным `GeoService`; DI через `DefaultServiceFactory`.
- [x] Интеграционный тест: Tallinn → geo на сторе.

## Task Artifacts
- Task workspace: [`../../../task-m2-08-03-geo-service-intake-integration/README.md`](../../../task-m2-08-03-geo-service-intake-integration/README.md)
- Task specification: [`../../../task-m2-08-03-geo-service-intake-integration/task-m2-08-03-geo-service-intake-integration.md`](../../../task-m2-08-03-geo-service-intake-integration/task-m2-08-03-geo-service-intake-integration.md)
- Phase log: [`../../../task-m2-08-03-geo-service-intake-integration/BULLRUN-PHASE-LOG.md`](../../../task-m2-08-03-geo-service-intake-integration/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-08-03-geo-service-intake-integration/acceptance-verification-STORY-M2-08-03.md`](../../../task-m2-08-03-geo-service-intake-integration/acceptance-verification-STORY-M2-08-03.md)
