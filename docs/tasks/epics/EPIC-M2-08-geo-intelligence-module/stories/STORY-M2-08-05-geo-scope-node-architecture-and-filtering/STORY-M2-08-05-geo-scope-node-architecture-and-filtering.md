# STORY-M2-08-05: Geo scope, node architecture and geo filtering (REQ-35)

## Meta
- Key: `STORY-M2-08-05`
- Parent Epic: [`../../../EPIC-M2-08-geo-intelligence-module.md`](../../../EPIC-M2-08-geo-intelligence-module.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 Geo Intelligence / cluster geo policy
- Decision Ref: [`../../../../../requirements/35-geo-scope-node-architecture-and-filtering.md`](../../../../../requirements/35-geo-scope-node-architecture-and-filtering.md); [`../../../../../analysis/gap-interview-decisions-2026-05-13.md`](../../../../../analysis/gap-interview-decisions-2026-05-13.md) — G-02
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000014-20260515-req35-geo-scope-node-architecture.yaml`](../../../../gateway-active-packages/pkg-000014-20260515-req35-geo-scope-node-architecture.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **7** тасков T01–T07 (immutable)
- Audit follow-up (override only): T08 — [`audit-req35-geo-scope-node-architecture-2026-05-16.md`](../../../../../analysis/audit-req35-geo-scope-node-architecture-2026-05-16.md); `run_mode=story08_05_audit_req35_followup` в [`Gateway_builder.plan.md`](../../../../../../../.cursor/plans/Gateway_builder.plan.md); **не** менять `pkg-000014`
- Depends on: STORY-M2-08-01..04 (geo cache, resolver chain, intake integration); REQ-33 intake v2 for `handle_story_intake`
- Supersedes (behavior): none — new geo admin levels and cluster/intake geo policy
- Out of scope: REQ-36 `alpha_score()` / tie-breaker; private nodes / web3; real OpenCage/Nominatim mapping (post-demo)

## Story Goal
Расширить `StoryGeoSnapshot` структурированными admin-уровнями; реализовать `CLUSTER_GEO_FILTER` в cluster engine; добавить `CLUSTER_GEO_SCOPE` с rejection на intake (HTTP 422 `GEO_SCOPE_MISMATCH`); обновить демо-стабы, persistence и тесты по REQ-35.

## Scope
- Runtime: `domain/contracts.py`, `geo/providers.py`, `config/schema.py`, `cluster/engine.py`, `api/handlers.py`, `infrastructure/db_sqlite.py`, `infrastructure/db_supabase.py`, `example.env`
- Tests: REQ-35 §5 acceptance (scope rejection, geo filter granularity, geo-agnostic intake)

## Out of scope
- Реальная интеграция OpenCage/Nominatim admin-level mapping (post-demo)
- Приватные ноды, web3 токенизация, криптоверификация типа ноды (REQ-35 §6)
- `CLUSTER_TIE_BREAKER` / REQ-36 alpha scoring

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-08-05-t01-story-geo-snapshot-admin-levels`](./task-m2-08-05-t01-story-geo-snapshot-admin-levels/README.md) | pkg-000014 |
| 2 | [`task-m2-08-05-t02-geo-provider-stubs-admin-fields`](./task-m2-08-05-t02-geo-provider-stubs-admin-fields/README.md) | pkg-000014 |
| 3 | [`task-m2-08-05-t03-persistence-geo-snapshot-jsonb`](./task-m2-08-05-t03-persistence-geo-snapshot-jsonb/README.md) | pkg-000014 |
| 4 | [`task-m2-08-05-t04-config-cluster-geo-scope-and-filter`](./task-m2-08-05-t04-config-cluster-geo-scope-and-filter/README.md) | pkg-000014 |
| 5 | [`task-m2-08-05-t05-cluster-engine-geo-filter`](./task-m2-08-05-t05-cluster-engine-geo-filter/README.md) | pkg-000014 |
| 6 | [`task-m2-08-05-t06-intake-geo-scope-rejection`](./task-m2-08-05-t06-intake-geo-scope-rejection/README.md) | pkg-000014 |
| 7 | [`task-m2-08-05-t07-tests-req35-acceptance`](./task-m2-08-05-t07-tests-req35-acceptance/README.md) | pkg-000014 |
| 8 | [`task-m2-08-05-t08-audit-gap35-01-sqlite-admin-geo-roundtrip`](./task-m2-08-05-t08-audit-gap35-01-sqlite-admin-geo-roundtrip/README.md) | audit-req35-2026-05-16 |

## AC / DoD (story level)
- [x] `StoryGeoSnapshot` содержит `admin_settlement`, `admin_country` (минимум) после geo resolve
- [x] `CLUSTER_GEO_SCOPE=settlement:tallinn` → нарвская геолокация → HTTP 422 `GEO_SCOPE_MISMATCH`
- [x] `CLUSTER_GEO_SCOPE=settlement:tallinn` → история без `location_query` → принята
- [x] `CLUSTER_GEO_FILTER=settlement` → Tallinn и Narva в разных кластерах
- [x] `CLUSTER_GEO_FILTER=country` (дефолт) → эстонские истории кластеризуются вместе
- [x] Демо-стабы возвращают корректные admin-уровни
- [x] `gateway_resolve_queue.py --verify` → `ok 7 paths` for pkg-000014
- [x] AUDIT-GAP-35-01: SQLite roundtrip asserts `geo_admin_*` (audit follow-up T08)

## Traceability: REQ-35 §5 → tasks

| REQ AC | Task |
|--------|------|
| admin_settlement / admin_country on snapshot | T01, T02, T03 |
| CLUSTER_GEO_SCOPE Tallinn vs Narva 422 | T04, T06, T07 |
| No location_query accepted under scope | T06, T07 |
| CLUSTER_GEO_FILTER settlement splits clusters | T05, T07 |
| CLUSTER_GEO_FILTER country default | T04, T05, T07 |
| Demo stubs admin levels | T02, T07 |

## Traceability: audit → tasks

| Audit gap | Task |
|-----------|------|
| AUDIT-GAP-35-01 SQLite admin fields roundtrip | T08 |

## Conflict-scan
| Existing | Action |
|----------|--------|
| STORY-M2-04-05 | REQ-35 explicitly out of scope there — no overlap |
| REQ-36 alpha / tie-breaker | Do not change `CLUSTER_TIE_BREAKER` behavior beyond existing civic defaults |
| G-02 default `country` vs schema `any` | T04 aligns env default and validation |
| GAP-35-01 (implementation, T01) vs AUDIT-GAP-35-01 (audit §5) | T01 closed (model fields); audit SQLite test → **T08 only** |
