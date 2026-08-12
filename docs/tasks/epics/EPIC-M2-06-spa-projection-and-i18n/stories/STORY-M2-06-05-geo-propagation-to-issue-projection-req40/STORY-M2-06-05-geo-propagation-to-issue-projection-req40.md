# STORY-M2-06-05: Geo propagation to issue projection (REQ-40)

## Meta
- Key: `STORY-M2-06-05`
- Parent Epic: [`../../../EPIC-M2-06-spa-projection-and-i18n.md`](../../../EPIC-M2-06-spa-projection-and-i18n.md)
- Type: Technical Story
- Status: Done (Awaiting Commits)
- Stream: M2 SPA projection / geo propagation / issue payload_json
- Decision Ref: [`../../../../../requirements/40-geo-propagation-to-issue-projection.md`](../../../../../requirements/40-geo-propagation-to-issue-projection.md); [`../../../../../solution architecture/18-issue-filtering-and-geo-search-architecture.md`](../../../../../solution%20architecture/18-issue-filtering-and-geo-search-architecture.md) §2, §3, §5, §9 Phase 1
- Operative queue (default Build): [`../../../../gateway-active-packages/pkg-000018-20260517-req40-geo-propagation-issue-projection.yaml`](../../../../gateway-active-packages/pkg-000018-20260517-req40-geo-propagation-issue-projection.yaml) via [`../../../../gateway-active-package.current.yaml`](../../../../gateway-active-package.current.yaml) — **6** тасков T01–T06 (immutable)
- Depends on: STORY-M2-08-03 (geo on `StoryRecord`); STORY-M2-06-01..04 (projection base); REQ-36 `select_dominant_story` / alpha_score (runtime)
- Blocks: REQ-24 §4 geo-filters (AC-14 – AC-19) — **not in this story**
- Out of scope: Immutable `pkg-000017`; REQ-24 read API filters; centroid geo v2; Phase 3 `postal_code`

## Story Goal
Закрыть REQ-40 Phase 1: прокинуть `StoryGeoSnapshot` доминантной истории в `ProjectionInput` → `DOGEIssue` → `payload_json` как вложенный объект `"geo"` (Variant I — inline, без DDL).

## Product decisions (fixed)
- Geo source: **dominant story** via `select_dominant_story()` (REQ-40 §2).
- Storage: **inline in `payload_json`** (REQ-40 §3.1 Variant I).
- Missing geo: ключ `"geo"` **отсутствует** в public dict (not `null`) (REQ-40 §3.2, AC-2).

## Scope
- Runtime: `projection/input.py`, `dto.py`, `mapper.py`, `extraction_policy.py`, `application/issue_create.py`
- Tests: `tests/test_req40_geo_propagation.py`

## Out of scope
- `GET /tallinn/issues` geo filters (REQ-24 Phase 2)
- Centroid geo across cluster stories (REQ-40 §2 TODO v2)
- `postal_code` on `StoryGeoSnapshot` (REQ-40 §6 Phase 3)
- PostGIS / spatial index

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-m2-06-05-t01-projection-input-geo-fields`](./task-m2-06-05-t01-projection-input-geo-fields/README.md) | pkg-000018 |
| 2 | [`task-m2-06-05-t02-doge-issue-geo-subobject`](./task-m2-06-05-t02-doge-issue-geo-subobject/README.md) | pkg-000018 |
| 3 | [`task-m2-06-05-t03-mapper-geo-projection`](./task-m2-06-05-t03-mapper-geo-projection/README.md) | pkg-000018 |
| 4 | [`task-m2-06-05-t04-extraction-policy-geo-snapshot`](./task-m2-06-05-t04-extraction-policy-geo-snapshot/README.md) | pkg-000018 |
| 5 | [`task-m2-06-05-t05-issue-create-bridge-dominant-geo`](./task-m2-06-05-t05-issue-create-bridge-dominant-geo/README.md) | pkg-000018 |
| 6 | [`task-m2-06-05-t06-req40-acceptance-tests`](./task-m2-06-05-t06-req40-acceptance-tests/README.md) | pkg-000018 |

## AC / DoD (story level)
- [x] `ProjectionInput` carries geo_* fields when dominant story has geo (GAP-40-01)
- [x] `DOGEIssue.to_public_dict()` emits `"geo"` sub-object only when lat/lon present (GAP-40-02, GAP-40-03)
- [x] `build_projection_input_from_draft(geo_snapshot=…)` and bridge pass `dominant_story.geo` (GAP-40-04, GAP-40-05)
- [x] REQ-40 §7 AC-1..AC-4 covered by `tests/test_req40_geo_propagation.py` (T06)
- [x] `gateway_resolve_queue.py --verify` → `ok 6 paths` for pkg-000018

**Gate:** [`story-acceptance-gate-STORY-M2-06-05.md`](./story-acceptance-gate-STORY-M2-06-05.md) — PASS (2026-05-17)

## Traceability: REQ-40 → tasks

| REQ-40 | Task |
|--------|------|
| §4.1 ProjectionInput geo fields | T01 |
| §4.2 DOGEIssue + serialize | T02 |
| §4.3 mapper geo mapping | T03 |
| §4.4 extraction_policy geo_snapshot | T04 |
| §4.5 issue_create bridge | T05 |
| §7 acceptance criteria | T06 |

## Conflict-scan

| Existing | Action |
|----------|--------|
| STORY-M2-17-02 / pkg-000017 | Immutable; do not modify |
| REQ-38 `projection/validation.py` | Orthogonal; do not change in this wave |
| REQ-24 geo filters | Out of scope until REQ-40 story Done |
| EPIC-M2-08 GeoService | Upstream only; no resolver changes |
