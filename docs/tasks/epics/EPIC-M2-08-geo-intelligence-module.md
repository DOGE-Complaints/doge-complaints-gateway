# EPIC-M2-08: Geo Intelligence Module

## Epic Meta
- Status: Draft
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

## Initial Story Decomposition (Draft)
- STORY-M2-08-01: implement canonical geo cache schema
- STORY-M2-08-02: implement GeoResolver adapter chain
- STORY-M2-08-03: integrate GeoService in intake pipeline
- STORY-M2-08-04: add geo resilience and metrics tests
