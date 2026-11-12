# task-gw-ssr-22-t02-boot-fail-if-chosen

## Task: implement — boot fail-fast если T00=boot (T02)

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** implement
- **Status:** 🔵 Done (N/A) · P4 PASS 2026-08-30T20:13:31Z
- **Package:** pkg-000079
- **Skill declared:** python-pro
- **Depends on:** T00 lock
- **Scaffolded:** 2026-08-30T20:01:08Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` T02

## Purpose
Если T00 = boot ConfigError: fail-fast когда активный pack задаёт `geo_scope`, а `geo_service` не резолвится. Если T00 = intake 4xx: **N/A** — записать reason в acceptance, не удалять `GeoService`.

## Code Facts
- Factory always wires GeoService — [`service_factory.py:64`](../../../../../../../src/core/infrastructure/service_factory.py)
- Civic knobs from pack — [`schema.py:309`](../../../../../../../src/core/config/schema.py) `civic_clustering_from_active_node`
- Intake optional None — [`services.py:100`](../../../../../../../src/core/application/services.py)

## Acceptance / DoD
- [x] Если T00=boot: scope + no geo_service → ConfigError (не silent)
- [x] Если T00=intake: N/A + reason; GeoService не удалён
- [x] Нет глобального require-geo
- [x] BULLRUN phases complete

## Where to change
- Only if T00=boot: factory / boot path that can see pack `geo_scope` and service presence.
- Do **not** delete GeoService.

## Out of scope
- Удалить GeoService. Полный `geo_detail` (→23).
- Overlay bans (every task):
  - Remove silent skip when `geo_scope` active + `geo_service is None`.
  - **No full `geo_detail` / `geo_intake` parse** (→23). No invent HTTP filter.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет IDX. Нет GPT UI.
  - **No global require-geo.** Optional / no-`geo_scope` stays geo-agnostic (REQ-35).
  - **Нет SSR-06/07/12.** Не reopen 01–21. Не стартовать 23…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "geo_service" doge-complaints-gateway/src/core/infrastructure/service_factory.py
```
