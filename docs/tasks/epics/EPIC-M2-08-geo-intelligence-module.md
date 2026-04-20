# EPIC-M2-08: Geo Intelligence Module

## Epic Meta
- Status: Implemented (Waiting Commits)
- Priority: Medium-High
- Owner: TBD
- Target: Sprint 2-4 (parallel track)

## Business Goal
Сохранить и модернизировать geo-логику как единственный осознанный reuse из legacy.

## Problem Statement
Текущий геомодуль содержит полезный intent, но реализация нестабильна и несовместима с целевой архитектурой.

## Scope
### In Scope
- GeoService facade;
- provider adapters (OpenCage/Nominatim policy chain);
- canonical geo cache store;
- location normalization and confidence scoring;
- cluster-ready geo tags.

### Out of Scope
- advanced geospatial analytics;
- map visualization layer.

## Stakeholders
- Product Analytics
- Backend/Data team

## Dependencies
- EPIC-M2-01 completed
- EPIC-M2-02 baseline store available

## Success Metrics
- cache hit ratio растет спринт-к-спринту;
- external geocode failures не ломают intake flow;
- geo fields доступны для cluster lenses.

## Epic Acceptance Criteria
- geo lookup строго использует canonical cache;
- provider timeout/retry policy реализована;
- no schema mismatch for geo persistence;
- logs/metrics покрывают geo pipeline.

## Risks and Mitigation
- Риск: сторонние geocoding API rate limits.  
  Mitigation: cache-first strategy + backoff + provider fallback.

## Definition of Done
- geo модуль стабилен, наблюдаем и интегрирован в story intelligence.

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-M2-08-01 | [Canonical geo cache schema](./EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-01-canonical-geo-cache-schema.md) | Implemented (Waiting Commits) |
| STORY-M2-08-02 | [GeoResolver adapter chain](./EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-02-geo-resolver-adapter-chain.md) | Implemented (Waiting Commits) |
| STORY-M2-08-03 | [GeoService in intake pipeline](./EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-03-geo-service-intake-integration.md) | Implemented (Waiting Commits) |
| STORY-M2-08-04 | [Geo resilience and metrics tests](./EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-04-geo-resilience-and-metrics-tests.md) | Implemented (Waiting Commits) |
