# BULLRUN Phase Log — TASK-M2-08-05-T06

- [x] Analysis: GAP-35-05 — no intake boundary for node geo scope
- [x] Implement: pre-create scope check in `api/handlers.py`; `GeoScopeMismatchError` → 422 `GEO_SCOPE_MISMATCH` in `api/envelope.py`; `geo_matches_scope` helper
- [x] Verify: `acceptance-verification-m2-08-05-t06.md`; HTTP tests Narva reject / no-location accept / Tallinn accept
