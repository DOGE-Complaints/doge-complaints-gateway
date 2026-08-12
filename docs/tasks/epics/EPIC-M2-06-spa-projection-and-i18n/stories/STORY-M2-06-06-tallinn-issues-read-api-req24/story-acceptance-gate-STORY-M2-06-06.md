# Story acceptance gate — STORY-M2-06-06

- **Story:** Tallinn issues read API (REQ-24)
- **Package:** `pkg-000019-20260518-req24-tallinn-issues-read-api.yaml`
- **Result:** PASS
- **Date:** 2026-05-17
- **Audit follow-up (T09–T10):** PASS — 2026-05-17; run [`run-summary-20260517-req24-audit-followup-t09-t10.md`](../../../run-reports/run-summary-20260517-req24-audit-followup-t09-t10.md)

## AC checklist (REQ-24 §7)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: `doge_issues` table (SQLite) | PASS | `test_req24_ac1_sqlite_doge_issues_table_exists` |
| AC-2: write path uses `doge_issues` | PASS | `test_req24_ac2_write_path_uses_doge_issues`, `test_req24_ac2_sqlite_write_path_uses_doge_issues_table` |
| AC-3: empty list | PASS | `test_req24_ac3_empty_list` |
| AC-4: list after intake | PASS | `test_req24_ac4_list_after_intake` |
| AC-5: status filter (payload status) | PASS | `test_req24_ac5_status_filter` |
| AC-6: type filter | PASS | `test_req24_ac6_type_filter` |
| AC-7: GET by id | PASS | `test_req24_ac7_get_by_id` |
| AC-8: GET missing 404 | PASS | `test_req24_ac8_get_missing_returns_404` |
| AC-9: CORS OPTIONS | PASS | `test_req24_ac9_cors_options` |
| AC-10: POST without bearer 401 | PASS | `test_req24_ac10_post_without_bearer_returns_401` |
| AC-11: POST with bearer 201 | PASS | `test_req24_ac11_post_with_bearer_creates_issue` |
| AC-12: manual issue in list | PASS | `test_req24_ac12_manual_issue_appears_in_list` |
| AC-13: OpenAPI paths | PASS | `test_openapi_contains_tallinn_paths` |
| AC-14: bbox filter | PASS | `test_req24_ac14_bbox_filter` |
| AC-15: geo-less excluded when bbox active | PASS | `test_req24_ac15_geo_less_excluded_when_bbox_active` |
| AC-16: district normalized | PASS | `test_req24_ac16_district_normalized` |
| AC-17: multi-value district OR | PASS | `test_req24_ac17_geo_district_multi_value_or` |
| AC-18: bbox + district AND | PASS | `test_req24_ac18_bbox_and_district_and` |
| AC-19: created_after / created_before | PASS | `test_req24_ac19_created_after_before` |
| AC-20: empty geo param ignored | PASS | `test_req24_ac20_empty_geo_param_ignored` |
| `gateway_resolve_queue.py --verify` ok 8 paths | PASS | pkg-000019 |

## Runtime files

- `src/core/application/issue_create.py` (Protocol, `create_manual_issue`, projection row status = SPA status)
- `src/core/projection/read_filters.py`
- `src/core/infrastructure/repositories.py`, `db_sqlite.py`, `db_supabase.py`
- `src/core/infrastructure/service_factory.py`, `src/core/application/factory.py`
- `src/core/api/dependencies.py`, `handlers.py`, `asgi_app.py`
- `docs/runtime-docs/api-reference/openapi.yaml`
- `tests/test_req24_tallinn_issues_read_api.py`

## Commands

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && python3 -m pytest tests/test_req24_tallinn_issues_read_api.py -q  # 23 tests
cd doge-complaints-gateway && python3 -m pytest -q
```
