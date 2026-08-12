# Acceptance verification — task-m2-16-02-t04-geo-location-query-coverage

## AC checklist
- [x] GAP-SIM-04 закрыт: geo-сценарии имеют location_query coverage.

## Verification commands
```bash
cd doge-complaints-gateway && rg -n "location_query" tests/sandbox/dogestonia_simulation_canvas_v0_1.json
```

## Verification performed
- Added `resident_input.location_query` for all 26 scenarios with `has_location=true`.
- Updated summary file with `geo_location_query_coverage` counters.
