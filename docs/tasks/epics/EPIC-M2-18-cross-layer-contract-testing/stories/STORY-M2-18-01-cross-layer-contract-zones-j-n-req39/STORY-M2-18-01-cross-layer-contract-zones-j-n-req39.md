# STORY-M2-18-01: Cross-layer contract zones J–N (REQ-39)

## Meta
- Key: `STORY-M2-18-01`
- Parent Epic: [`../../../EPIC-M2-18-cross-layer-contract-testing.md`](../../../EPIC-M2-18-cross-layer-contract-testing.md)
- Type: Technical Story
- Status: Done (Build); audit follow-up closed (T06–T09)
- Stream: M2 quality / contract testing / post-REQ-24 pipeline
- Decision Ref: [`../../../../../requirements/39-cross-layer-contract-testing.md`](../../../../../requirements/39-cross-layer-contract-testing.md) §10–14 (zones J–N); depends REQ-24, REQ-27, REQ-34, REQ-40
- Operative queue: [`../../../../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml`](../../../../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml) — tasks T01–T05
- Depends on: STORY-M2-06-06 (REQ-24), STORY-M2-06-05 (REQ-40), STORY-M2-04-05 (REQ-34)
- Blocks: STORY-M2-18-02 (optional ordering); demo confidence for GET `/tallinn/issues` on real canvas

## Story Goal
Добавить offline contract-тесты для новых SEAM-зон J–N: clustering → `doge_issues`, geo propagation, `IssueProjectionReadStore`, `filter_projection_rows`, полный sandbox pipeline.

## Product decisions (fixed)
- Clustering trigger in tests: `ApiDependencies.story_cluster_orchestrator.process_all_pending()` — **not** `POST /clustering/trigger` (route absent in `src/core/api/`)
- Fixtures: `CLUSTER_MIN_SIZE=1`, `CLUSTER_READINESS_THRESHOLD=1`, `APP_PROFILE=demo` (per REQ-39 §N, `test_req24_tallinn_issues_read_api.py`)
- Table: `doge_issues` (REQ-27)

## Scope
- New test modules: `test_issue_projection_store_contract.py`, `test_filter_projection_rows_contract.py`, `test_clustering_pipeline_contract.py`, `test_geo_propagation_contract.py`, `test_e2e_sandbox_full_pipeline.py`
- Reuse helpers from `test_req24_*` / `test_req40_*` where DRY

## Out of scope
- Zones A–I (STORY-M2-18-02)
- Supabase live parametrization for L (InMemory + SQLite only in contract file)
- Production code changes unless tests prove gap

## Nested tasks

| Order | Task folder | Zone |
|-------|-------------|------|
| 1 | [`task-m2-18-01-t01-zone-l-issue-projection-store-contract`](./task-m2-18-01-t01-zone-l-issue-projection-store-contract/README.md) | L |
| 2 | [`task-m2-18-01-t02-zone-m-filter-projection-rows-contract`](./task-m2-18-01-t02-zone-m-filter-projection-rows-contract/README.md) | M |
| 3 | [`task-m2-18-01-t03-zone-j-clustering-pipeline-contract`](./task-m2-18-01-t03-zone-j-clustering-pipeline-contract/README.md) | J |
| 4 | [`task-m2-18-01-t04-zone-k-geo-propagation-contract`](./task-m2-18-01-t04-zone-k-geo-propagation-contract/README.md) | K |
| 5 | [`task-m2-18-01-t05-zone-n-e2e-sandbox-full-pipeline`](./task-m2-18-01-t05-zone-n-e2e-sandbox-full-pipeline/README.md) | N |
| 6 | [`task-m2-18-01-t06-audit-gap39-m-geo-addr-filters`](./task-m2-18-01-t06-audit-gap39-m-geo-addr-filters/README.md) | audit M |
| 7 | [`task-m2-18-01-t07-audit-gap39-k-geo-fixtures-decouple`](./task-m2-18-01-t07-audit-gap39-k-geo-fixtures-decouple/README.md) | audit K |
| 8 | [`task-m2-18-01-t08-audit-gap39-j03-policy-version-sqlite`](./task-m2-18-01-t08-audit-gap39-j03-policy-version-sqlite/README.md) | audit J |
| 9 | [`task-m2-18-01-t09-audit-gap39-l-supabase-mock-contract`](./task-m2-18-01-t09-audit-gap39-l-supabase-mock-contract/README.md) | audit L |

## AC / DoD (story level)
- [ ] AC-39-3: Zone J — 4 tests (`CLUSTER_MIN_SIZE`, idempotency, policy_version)
- [ ] AC-39-4: Zone K — 4 tests (geo cascade to `payload_json["geo"]`)
- [ ] AC-39-5: Zone L — 4 parametrized store contract tests (InMemory + SQLite)
- [ ] AC-39-6: Zone M — 8 filter engine tests (null-safety, bbox, district OR/AND)
- [ ] AC-39-7: Zone N — 6 sandbox E2E tests (canvas → intake → issues → GET)
- [ ] `pytest tests/test_issue_projection_store_contract.py tests/test_filter_projection_rows_contract.py tests/test_clustering_pipeline_contract.py tests/test_geo_propagation_contract.py tests/test_e2e_sandbox_full_pipeline.py -q` green
- [ ] Story gate: [`story-acceptance-gate-STORY-M2-18-01.md`](./story-acceptance-gate-STORY-M2-18-01.md)

## Traceability: REQ-39 §16 rows 1–5 → tasks

| REQ row | Zone | Task |
|---------|------|------|
| 1 | L | T01 |
| 2 | M | T02 |
| 3 | J | T03 |
| 4 | K | T04 |
| 5 | N | T05 |

## Traceability: audit §8 → T06–T09

| Audit gap | Task |
|-----------|------|
| GAP-39-M-GEO-ADDR | T06 |
| GAP-39-K-DEP | T07 |
| GAP-39-J03-PRIVATE | T08 |
| GAP-39-L-SUPA | T09 |

## Audit follow-up (2026-05-18)

- Source: [`audit-req39-cross-layer-contract-testing-2026-05-18.md`](../../../../../analysis/audit-req39-cross-layer-contract-testing-2026-05-18.md) — 5 gaps, non-blocking
- Override: `run_mode=story18_audit_req39_followup` in [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md)
- **Не** менять immutable [`pkg-000020`](../../../../gateway-active-packages/pkg-000020-20260518-req39-cross-layer-contract-testing.yaml)

| Audit gap | Task |
|-----------|------|
| GAP-39-M-GEO-ADDR | T06 |
| GAP-39-K-DEP | T07 |
| GAP-39-J03-PRIVATE | T08 |
| GAP-39-L-SUPA | T09 |

## Conflict-scan
- `test_req24_tallinn_issues_read_api.py` — keep; contract files add seam-focused coverage
- `test_req40_geo_propagation.py` — T04 must not duplicate; focus Protocol/seam assertions
- Audit gaps — test debt only; no pkg-000020 edits
