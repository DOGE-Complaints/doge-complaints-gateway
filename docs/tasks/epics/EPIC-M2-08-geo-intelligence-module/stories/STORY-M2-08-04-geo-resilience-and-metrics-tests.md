# STORY-M2-08-04: Geo resilience and metrics tests

## Meta
- Key: `STORY-M2-08-04`
- Parent Epic: [`../../EPIC-M2-08-geo-intelligence-module.md`](../../EPIC-M2-08-geo-intelligence-module.md)
- Type: Technical Story
- Status: Done (Committed)
- Stream: M2 Geo
- Skill declared: `python-pro`

## Story Goal
Наблюдаемость geo pipeline: cache hit/miss, провайдеры, деградация intake при неуспешном resolve.

## AC / DoD
- [x] `GeoMetrics` / `InMemoryGeoMetrics`.
- [x] Неизвестная локация не роняет intake; `record_intake_degraded_geo`.
- [x] Тесты метрик и DI `get_geo_service`.

## Task Artifacts
- Task workspace: [`../../../task-m2-08-04-geo-resilience-and-metrics-tests/README.md`](../../../task-m2-08-04-geo-resilience-and-metrics-tests/README.md)
- Task specification: [`../../../task-m2-08-04-geo-resilience-and-metrics-tests/task-m2-08-04-geo-resilience-and-metrics-tests.md`](../../../task-m2-08-04-geo-resilience-and-metrics-tests/task-m2-08-04-geo-resilience-and-metrics-tests.md)
- Phase log: [`../../../task-m2-08-04-geo-resilience-and-metrics-tests/BULLRUN-PHASE-LOG.md`](../../../task-m2-08-04-geo-resilience-and-metrics-tests/BULLRUN-PHASE-LOG.md)
- Acceptance: [`../../../task-m2-08-04-geo-resilience-and-metrics-tests/acceptance-verification-STORY-M2-08-04.md`](../../../task-m2-08-04-geo-resilience-and-metrics-tests/acceptance-verification-STORY-M2-08-04.md)
