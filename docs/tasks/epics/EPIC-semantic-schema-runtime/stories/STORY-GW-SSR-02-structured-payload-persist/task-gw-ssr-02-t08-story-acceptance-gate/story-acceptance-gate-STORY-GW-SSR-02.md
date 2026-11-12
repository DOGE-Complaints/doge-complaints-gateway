# Story acceptance gate — STORY-GW-SSR-02

- **Story:** Schema/profile binding + structured_payload persist
- **Package:** `pkg-000062-20260828-gw-ssr-02-structured-payload-persist.yaml`
- **Result:** PASS
- **Date:** 2026-08-28T13:47:57Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ3-02 / AC-002: two unrelated payloads persist on same core model; no schema-specific DDL between them. | PASS | `tests/test_gw_ssr_02_structured_payload_persist.py::test_two_payloads_same_sqlite_table`; one `stories` table; migration ADD COLUMN only |
| AC-GW-REQ3-03 / AC-003: stored structured Story identifies envelope version, schema ID/version, profile ID/version, payload. | PASS | `StoryRecord.schema_version` envelope + `schema_id` / `bound_schema_version` / `profile_id` / `profile_version` / `structured_payload` round-trip sqlite+memory |
| DATA-001: no node-specific `stories` columns for domain fields. | PASS | no `institution_type` / `story_dimensions`; six nullable binding columns only |
| DATA-004: deterministic hash of canonical validated payload persisted as `payload_hash`. | PASS | `src/core/schema/payload.py`; persist uses `authoritative_payload_hash`; client hash ignored |
| Existing M2 persist of current envelope `schema_version` remains operational. | PASS | civic all-None save + intake create; `test_story_intake_contract.py` + `test_story_intake_field_persistence.py` green |
| T08 extra: lifecycle advance keeps binding (`dataclasses.replace`). | PASS | `test_lifecycle_advance_keeps_binding`; `services.py` `replace(current, lifecycle_status=…, updated_at=…)` |
| T08 extra: `required_columns_ready` without binding cols; intake still no `schema_binding`. | PASS | `test_readiness_probe_does_not_require_binding_columns`; `test_intake_parser_has_no_schema_binding` |
| T08 extra: `ClusterLens` enum unchanged. | PASS | `test_clusterlens_baseline_unchanged` |

## Commands (live verification 2026-08-28T13:47:57Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --print-utc-now
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_02_structured_payload_persist.py \
  tests/test_stories_schema_cross_layer_invariant.py \
  tests/test_story_intake_contract.py tests/test_story_intake_field_persistence.py
# → 36 passed
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
