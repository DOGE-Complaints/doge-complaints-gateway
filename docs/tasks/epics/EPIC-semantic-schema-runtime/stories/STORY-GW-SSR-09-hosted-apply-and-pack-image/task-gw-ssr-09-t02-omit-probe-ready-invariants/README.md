# task-gw-ssr-09-t02-omit-probe-ready-invariants

## Task: tests — omit-probe and `/ready` invariants

## Meta
- **Story:** [STORY-GW-SSR-09](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000067
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-29T18:09:45Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-09-hosted-apply-and-pack-image.md` T02

## Purpose
Code invariants: omit-probe cuts binding **only** when probe fails; `required_columns_ready` stories set excludes the six binding names; civic `/ready` does not require binding (no 503 from missing binding cols). Restart cache (`stories_binding_columns_ready`) documented; **live restart = operator**, not overnight DoD. Do not change civic path.

## Code Facts
- Probe + cache — [`db_supabase.py:366–386`](../../../../../../../src/core/infrastructure/db_supabase.py)
- Omit SELECT — [`db_supabase.py:470–476`](../../../../../../../src/core/infrastructure/db_supabase.py) `_story_select_fields_for_db`
- `/ready` — [`db_supabase.py:388`](../../../../../../../src/core/infrastructure/db_supabase.py) stories keys `:392–403` without binding names
- Binding set — [`db_supabase.py:333–341`](../../../../../../../src/core/infrastructure/db_supabase.py)

## Acceptance / DoD
- [x] Assert omit-probe cuts binding only when `stories_binding_columns_ready` is false
- [x] `required_columns_ready` stories set has no `schema_id` / `bound_schema_version` / `structured_payload` / `payload_hash` / `profile_id` / `profile_version`
- [x] Civic `/ready` path does not require binding columns
- [x] Cache/restart fact documented (live restart = operator)
- [x] Civic path unchanged
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/infrastructure/db_supabase.py` as-is unless a pointed test is missing
- `doge-complaints-gateway/tests/test_gw_ssr_09_*` if needed
- No civic engine/factory edits

## Out of scope
- Live hosted restart as overnight DoD
- Change civic path; add binding to `required_columns_ready`
- Invent Dockerfile; invent HTTP
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py:108–111`).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:30–44`).
  - Не invent HTTP filter / IDX/QRY. `GET /tallinn/issues` stays (`asgi_app.py` :462).
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/10/12. Не reopen SSR-08.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0[1-5]*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Overlay UI spa-app — **not this story**.
  - Не invent Dockerfile.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "required_columns_ready" -A 40 doge-complaints-gateway/src/core/infrastructure/db_supabase.py
rg -n "schema_id|bound_schema_version|structured_payload" doge-complaints-gateway/src/core/infrastructure/db_supabase.py
rg -n "stories_binding_columns_ready|_STORIES_BINDING_COLUMNS" doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
