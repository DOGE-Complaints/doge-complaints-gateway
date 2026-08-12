# STORY-M2-06-06: Tallinn issues read API (REQ-24)

## Meta
- Key: `STORY-M2-06-06`
- Parent Epic: [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- Type: Technical Story
- Status: Done (Awaiting Commits); audit follow-up T09–T10 closed (2026-05-17)
- Stream: M2 SPA projection / public read API / operator manual create
- Decision Ref: [`../../../../../requirements/24-tallinn-issues-read-api.md`](../../../../../requirements/24-tallinn-issues-read-api.md); [`../../../../../requirements/27-doge-issue-domain-rename.md`](../../../../../requirements/27-doge-issue-domain-rename.md) (table `doge_issues`); [`../../../../../solution architecture/18-issue-filtering-and-geo-search-architecture.md`](../../../../../solution%20architecture/18-issue-filtering-and-geo-search-architecture.md) §7–§8
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000019-20260518-req24-tallinn-issues-read-api.yaml`](../../../../gateway-active-packages/pkg-000019-20260518-req24-tallinn-issues-read-api.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **8** тасков T01–T08 (immutable)
- Depends on: STORY-M2-06-05 (REQ-40 geo in payload); STORY-M2-06-01..04 (projection base); REQ-27 (`doge_issues` table as-is in runtime)
- Blocks: SPA `VITE_LIFE_REALITY_MODE=GFL-DRIVEN` read path (consumer per REQ-24 §1)

## Story Goal
Закрыть REQ-24: `IssueProjectionReadStore`, read-методы во всех backends, HTTP `GET /tallinn/issues`, `GET /tallinn/issues/{issue_id}`, protected `POST /tallinn/issues`, фильтры (категориальные + geo/time/institution), CORS, OpenAPI и acceptance tests AC-1..AC-20.

## Product decisions (fixed)
- Persistence table: **`doge_issues`** (REQ-27 supersedes REQ-24 §2.1 `tallinn_issues_projections`).
- Wire payload: `DOGEIssue.to_public_dict()` shape (includes optional `"geo"` per REQ-40).
- GET list/detail — **public**; `POST /tallinn/issues` — Bearer protected (REQ-24 §1.3).
- Canonical path `POST /tallinn/issues` (not deprecated `POST /issues`).

## Scope
- Runtime: `issue_create.py`, `repositories.py`, `db_sqlite.py`, `db_supabase.py`, `factory.py`, `service_factory.py`, `dependencies.py`, `handlers.py`, `asgi_app.py`, `issue_create.create_manual_issue`
- Tests: `tests/test_req24_tallinn_issues_read_api.py`
- Docs: `docs/runtime-docs/api-reference/openapi.yaml`

## Out of scope
- REQ-24 §2.1 table rename (closed by REQ-27)
- `issues_dashboard` view removal (REQ-24 §9)
- PostGIS, pagination, SPA code changes
- Centroid geo v2; `geo_postal_code` data fill (REQ-40 Phase 3)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-06-06-t01-issue-projection-read-store-protocol`](./task-m2-06-06-t01-issue-projection-read-store-protocol/README.md) | pkg-000019 |
| 2 | [`task-m2-06-06-t02-inmemory-read-store-list-get`](./task-m2-06-06-t02-inmemory-read-store-list-get/README.md) | pkg-000019 |
| 3 | [`task-m2-06-06-t03-sqlite-supabase-read-store`](./task-m2-06-06-t03-sqlite-supabase-read-store/README.md) | pkg-000019 |
| 4 | [`task-m2-06-06-t04-factory-di-read-store-wiring`](./task-m2-06-06-t04-factory-di-read-store-wiring/README.md) | pkg-000019 |
| 5 | [`task-m2-06-06-t05-handlers-tallinn-issues-and-manual-create`](./task-m2-06-06-t05-handlers-tallinn-issues-and-manual-create/README.md) | pkg-000019 |
| 6 | [`task-m2-06-06-t06-routes-cors-public-tallinn-issues`](./task-m2-06-06-t06-routes-cors-public-tallinn-issues/README.md) | pkg-000019 |
| 7 | [`task-m2-06-06-t07-extended-filters-geo-time-institution`](./task-m2-06-06-t07-extended-filters-geo-time-institution/README.md) | pkg-000019 |
| 8 | [`task-m2-06-06-t08-req24-acceptance-tests-and-openapi`](./task-m2-06-06-t08-req24-acceptance-tests-and-openapi/README.md) | pkg-000019 |
| 9 | [`task-m2-06-06-t09-audit-gap24-a-req27-ac-table-contract`](./task-m2-06-06-t09-audit-gap24-a-req27-ac-table-contract/README.md) | audit override |
| 10 | [`task-m2-06-06-t10-audit-gap24-b-filter-edge-ac-tests`](./task-m2-06-06-t10-audit-gap24-b-filter-edge-ac-tests/README.md) | audit override |

## AC / DoD (story level)
- [x] `IssueProjectionReadStore` Protocol with full filter signature (REQ-24 §3.1)
- [x] InMemory / SQLite / Supabase `list_projections` + `get_projection` read `doge_issues` (AC-1, AC-3..7)
- [x] Factory + `ApiDependencies.issue_projection_read_store` wired
- [x] Handlers + `create_manual_issue` (AC-7..12)
- [x] Routes, CORS, `PUBLIC_ROUTES` (AC-9)
- [x] Geo/time/institution filters (AC-14..20, AC-19)
- [x] `tests/test_req24_tallinn_issues_read_api.py` + OpenAPI three endpoints (AC-13)
- [x] `gateway_resolve_queue.py --verify` → `ok 8 paths` for pkg-000019

**Gate:** [`story-acceptance-gate-STORY-M2-06-06.md`](./story-acceptance-gate-STORY-M2-06-06.md) — PASS 2026-05-17

## Traceability: REQ-24 → tasks

| REQ-24 | Task |
|--------|------|
| §3.1 Protocol | T01 |
| §3.2 InMemory read | T02 |
| §3.3–3.4 SQLite/Supabase read | T03 |
| §5 Factory/DI | T04 |
| §4.1 Handlers + manual create | T05 |
| §4.2 Routes/CORS | T06 |
| §3.1.1 Phase 2 filters | T07 |
| §6 step 12, §7 AC | T08 |
| Audit GAP-A/C (REQ-27 AC-1/AC-2) | T09 |
| Audit GAP-B (AC-15/17/18/19 tests) | T10 |

## Audit follow-up (2026-05-17)

Источник: [`audit-req24-tallinn-issues-api-2026-05-17.md`](../../../../../analysis/audit-req24-tallinn-issues-api-2026-05-17.md). Исполнение: override `run_mode=story06_06_audit_req24_followup` в [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md); **не** менять immutable `pkg-000019`.

## Conflict-scan

| Existing | Action |
|----------|--------|
| `pkg-000018` (REQ-40) | Immutable; do not modify |
| REQ-24 §2.1 `tallinn_issues_projections` | Superseded by REQ-27 — use `doge_issues` in code/tasks |
| Audit GAP-A (rename to `tallinn_issues_projections`) | **Superseded by REQ-27** — T09 closes AC-1/AC-2 via docs + AC-2 test only; no DDL |
| `POST /issues` deprecated | Do not add; canonical `POST /tallinn/issues` only |
| STORY-M2-06-05 | Prerequisite (geo in payload); do not revert |
| `pkg-000019` (T01–T08) | Immutable; audit follow-up T09–T10 outside YAML |
