# acceptance-verification — GW-SSR-22 t00

- **Result:** PASS
- **Date:** 2026-08-30T20:07:21Z
- **Package:** pkg-000079

## Evidence

**T00 lock: intake 4xx** (`IntakeValidationError("geo unavailable")` → 400). Not boot ConfigError. Factory already always wires `GeoService` (`service_factory.py:64`); hole is handlers skip when `geo_service is None`. T02 = N/A.
