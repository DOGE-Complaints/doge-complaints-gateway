# 09. Module: Geo Intelligence

## Decision
Из legacy сохраняется только смысл геомодуля, но реализация переписывается под новый каркас.

## Responsibilities
- normalize location hint;
- resolve coordinates via provider chain;
- persist resolved geo profile;
- provide geo features for clustering and issue framing.

## Target design
- `GeoService` (domain facade).
- `GeoResolverAdapter` (OpenCage/Nominatim/provider chain).
- `GeoCacheRepository` (single canonical table, no schema split).
- `GeoPolicy` (timeouts, retry, quotas).

## Mandatory fixes vs legacy
- единая таблица кэша (no `location_directory` vs `address_directory` mismatch);
- write-back cache на успешный resolve;
- explicit timeout/retry/circuit breaker;
- structured logs instead of prints;
- graceful fallback when provider unavailable.

## Data outputs
- canonical coordinates;
- location confidence score;
- normalized city/region/country;
- geo tags for cluster lenses.
