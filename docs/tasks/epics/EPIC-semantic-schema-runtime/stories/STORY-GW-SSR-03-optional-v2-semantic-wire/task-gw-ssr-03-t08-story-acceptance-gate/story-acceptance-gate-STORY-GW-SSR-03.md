# Story acceptance gate — STORY-GW-SSR-03

- **Story:** Optional `schema_binding` on m2.story_intake_envelope.v2
- **Package:** `pkg-000063-20260828-gw-ssr-03-optional-v2-semantic-wire.yaml`
- **Result:** PASS
- **Date:** 2026-08-28T14:13:05Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-GW-REQ3-15 / AC-015: `schema_binding` present → bind + validate `structured_payload`; absent → civic intake succeeds. | PASS | `tests/test_gw_ssr_03_optional_v2_semantic_wire.py::test_present_schema_binding_persists_and_hashes_server_side`; `test_absent_schema_binding_is_civic_legacy`; `test_empty_schema_binding_object_is_civic` |
| AC-GW-REQ3-10 / COMPAT-001: do not remove `m2.story_intake_envelope.v2`. | PASS | civic parse still requires `INTAKE_SCHEMA_VERSION`; `tests/test_story_intake_contract.py` green |
| FLOW-003: named tokens persisted; silently ignoring = non-compliant. | PASS | present path maps envelope → `StoryRecord.schema_version`, inner → `schema_id` / `bound_schema_version` / profiles / payload + server hash; unknown keys / invalid payload raise `IntakeValidationError` |
| Tests §29: optional parse vs ignore-absent; civic intake green. | PASS | G3: `test_gw_ssr_03_*.py` + `test_story_intake_contract.py` + `test_gpt_signals_intake.py` → 41 passed |
| T08 extra: stash + submit share parse. | PASS | `test_stash_and_submit_share_binding` |
| T08 extra: `GET /tallinn/issues` stays; no filter path. | PASS | `test_get_tallinn_issues_route_stays`; `asgi_app.py:462` |
| T08 extra: `required_columns_ready` without binding; ClusterLens unchanged. | PASS | `test_required_columns_ready_omits_binding_names`; `test_clusterlens_baseline_unchanged` |

## Commands (live verification 2026-08-28T14:13:05Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
cd doge-complaints-gateway && .venv/bin/python -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_03_optional_v2_semantic_wire.py \
  tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py
# → 41 passed
rg -n "schema_binding" src/core/intake/contracts.py src/core/application/services.py
rg -n "def (GET|POST|PUT|PATCH|DELETE)|add_route|/tallinn/" src/core/api/asgi_app.py
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
