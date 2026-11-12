# task-gw-ssr-10-t02-promote-separate-candidates

## Task: implement — separate civic vs pack promote candidates

## Meta
- **Story:** [STORY-GW-SSR-10](../STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000068
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T18:25:31Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md` T02

## Purpose
Не гнать pack candidate через civic type-gate as-is; civic candidate — civic `PromotionGatePolicy` (default `require_actionable_canonical_type=True` / factory unchanged). Две кучи (civic `cluster_id` vs `schema:…`) — отдельные candidates. Не смешивать civic `readiness_score_for_cluster` с pack knobs на одном candidate.

## Code Facts
- Civic type-gate default — [`gates.py:14`](../../../../../../../src/core/promotion/gates.py) `require_actionable_canonical_type: bool = True`
- Civic factory — [`service_factory.py:108–111`](../../../../../../../src/core/infrastructure/service_factory.py) as-is (PromotionGatePolicy knobs; `require_actionable_canonical_type` default from `gates.py`)
- Pack promote mapper — [`pack_policy.py`](../../../../../../../src/core/schema/pack_policy.py) (SSR-05)
- Стыковка story: две кучи — отдельные candidates

## Acceptance / DoD
- [ ] Pack candidate не идёт через civic type-gate as-is
- [ ] Civic candidate uses civic policy (factory / default unchanged)
- [ ] Не один Issue на оба lens id без решения
- [ ] Civic `readiness_score_for_cluster` не смешивать с pack knobs на одном candidate
- [ ] BULLRUN phases complete

## Where to change
- Pack promote path (`pack_policy.py` / orchestrator promote branch)
- Civic factory `src/core/infrastructure/service_factory.py:108–111` **as-is**

## Out of scope
- Один Issue на оба lens id без решения; смена factory / default civic knobs
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79) как default для всех packs.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/11/12/13. Не reopen 01–05/08/09.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "require_actionable_canonical_type: bool = True" \
  doge-complaints-gateway/src/core/promotion/gates.py
rg -n "PromotionGatePolicy|pack_policy" \
  doge-complaints-gateway/src/core/infrastructure/service_factory.py \
  doge-complaints-gateway/src/core/schema/pack_policy.py
```
