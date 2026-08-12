# Story acceptance gate — STORY-M2-08-05

- Story: `STORY-M2-08-05`
- Gate status: **PASS**
- Requirement: REQ-35 (`35-geo-scope-node-architecture-and-filtering.md`); G-02
- Package: `pkg-000014-20260515-req35-geo-scope-node-architecture.yaml`

## Evidence

- `StoryGeoSnapshot` admin hierarchy: `admin_district`, `admin_settlement`, `admin_region`, `admin_country` (`domain/contracts.py`).
- Demo stubs Tallinn/Narva populate admin fields (`geo/providers.py`).
- Persistence roundtrip SQLite + Supabase + bootstrap DDL (`db_sqlite.py`, `db_supabase.py`, `000_full_init.sql`).
- `CLUSTER_GEO_SCOPE` optional `level:value`; `CLUSTER_GEO_FILTER` ∈ district|settlement|region|country, default `country` (`config/schema.py`, `geo/scope.py`, `example.env`).
- Cluster engine applies `geo_filter_bucket`; geo-agnostic stories use `geo:agnostic` (`cluster/engine.py`).
- Intake rejects out-of-scope location with HTTP 422 `GEO_SCOPE_MISMATCH`; stories without `location_query` accepted under scope (`api/handlers.py`, `api/envelope.py`).
- Acceptance module `tests/test_req35_geo_scope_and_filter.py`; all task gates T01–T07 PASS.

## Verification commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest -q --tb=short
cd doge-complaints-gateway && python3 -m pytest tests/test_req35_geo_scope_and_filter.py -q
```
