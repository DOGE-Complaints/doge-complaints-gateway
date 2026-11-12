# STORY-GW-SSR-27 — Geo precision + instance territory

## Meta
- **Key:** `STORY-GW-SSR-27-geo-precision-instance-territory`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** P1 — geo-precision wave (sequence **27**)
- **Тип:** implement (pack + wire/persist/projection)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Parent REQ:** 51 · 35
- **decision_ref:** backlog SSR-27
- **Skill declared:** python-pro
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000084-20260901-gw-ssr-27-geo-precision-instance-territory.yaml`](../../../../gateway-active-packages/pkg-000084-20260901-gw-ssr-27-geo-precision-instance-territory.yaml)
- **Git:** только `semantic-schema-runtime`
- **Зависит от:** SSR-25; parallel-safe vs SSR-26/28/29
- **Scaffolded:** 2026-09-01T13:12:45Z

## Nested tasks (pkg-000084)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-27-t00-contract-readme`](./task-gw-ssr-27-t00-contract-readme/README.md) |
| T01 | [`task-gw-ssr-27-t01-types-geo-precision`](./task-gw-ssr-27-t01-types-geo-precision/README.md) |
| T02 | [`task-gw-ssr-27-t02-loader-geo-blocks`](./task-gw-ssr-27-t02-loader-geo-blocks/README.md) |
| T03 | [`task-gw-ssr-27-t03-wire-persist-detail-level`](./task-gw-ssr-27-t03-wire-persist-detail-level/README.md) |
| T04 | [`task-gw-ssr-27-t04-projection-detail-level`](./task-gw-ssr-27-t04-projection-detail-level/README.md) |
| T05 | [`task-gw-ssr-27-t05-tests`](./task-gw-ssr-27-t05-tests/README.md) |
| T06 | [`task-gw-ssr-27-t06-manual-three-level-geo`](./task-gw-ssr-27-t06-manual-three-level-geo/README.md) |
| T07 | [`task-gw-ssr-27-t07-story-acceptance-gate`](./task-gw-ssr-27-t07-story-acceptance-gate/README.md) |
| T08 | [`task-gw-ssr-27-t08-audit-g1-as-of-done-ssot`](./task-gw-ssr-27-t08-audit-g1-as-of-done-ssot/README.md) (audit follow-up) |

## Зачем простыми словами

Precision index (`detail_level`) + GPT instance territory pack blocks + wire→persist→Issue.geo. Node `geo_scope` stays SSR-22. Gateway parses instance territory; GPT enforces STOP (GPT-SSR-08).

## Scope / Out of scope

**In:** README; types+loader; detail_level chain; projection UC-G03; tests; manual three-level; gate.

**Out:** ClusterLens; invent coords; HTTP geo-filter; street/house on Issue; invent tallinn district/bbox without OP; SSR-28/29; gateway instance enforce MVP.

## Verified current state (As-of-Done vs Historical)

### As-of-Done (post-P3 pkg-000084 / G27 PASS 2026-09-01T13:21:04Z)

| Fact | Ref |
|------|-----|
| `detail_level` on GeoDetail + snapshot | `intake/contracts.py`; `domain/contracts.py` |
| Pack `geo_model` + `gpt_instance_territory` | `schema/contracts.py` / `resolver.py`; tallinn seed Option B |
| Mapper UC-G03 without inventing coords | `projection/mapper.py` |
| Tests file 10 cases | `tests/test_gw_ssr_27_geo_precision.py` |
| `ClusterLens` = 10 | `types.py:10–22` |

### Historical (P1 scaffold 2026-09-01T13:12:45Z)

| Fact | Ref |
|------|-----|
| No `detail_level` in GeoDetail | `intake/contracts.py` `GEO_DETAIL_ALLOWED_KEYS` |
| No snapshot `detail_level` | `domain/contracts.py` |
| No pack geo_model / instance territory | `schema/contracts.py` / `resolver.py` |
| Mapper geo lat+lon gated | `projection/mapper.py` |
| Pipeline SSR-27 | scaffolded 2026-09-01T13:12:45Z |

## Target / AC

- [x] **AC-GW-SSR27-01…06** — see backlog story Target / AC
