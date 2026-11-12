# task-gw-ssr-09-t01-hosted-sql-binding-migration

## Task: data — six binding columns on disk (SQL artifact)

## Meta
- **Story:** [STORY-GW-SSR-09](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md)
- **Type:** data
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000067
- **Skill declared:** python-pro
- **Depends on:** SSR-02 Done (DDL already in repo)
- **Scaffolded:** 2026-08-29T18:09:45Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-09-hosted-apply-and-pack-image.md` T01

## Purpose
Keep/assert `20260828_1400_gw_ssr_02_stories_schema_binding.sql` on disk with six `ADD COLUMN IF NOT EXISTS` names matching `_STORIES_BINDING_COLUMNS`. G9: live hosted apply is **not** overnight proof — hosted apply = operator/deploy (runbook §6.2). Do not DROP tables. Do not put names in `required_columns_ready`.

## Code Facts
- Migration — [`20260828_1400_gw_ssr_02_stories_schema_binding.sql:4–10`](../../../../../../../supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql) six nullable cols
- Binding set — [`db_supabase.py:333–341`](../../../../../../../src/core/infrastructure/db_supabase.py) `_STORIES_BINDING_COLUMNS`
- `/ready` without binding — [`db_supabase.py:388`](../../../../../../../src/core/infrastructure/db_supabase.py)
- G9 — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.2

## Acceptance / DoD
- [x] `test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql`
- [x] SQL lists six names: `schema_id`, `bound_schema_version`, `profile_id`, `profile_version`, `structured_payload`, `payload_hash`
- [x] Names match `_STORIES_BINDING_COLUMNS`
- [x] Pipeline/manual note: hosted apply + restart = operator/deploy, not this pkg’s live proof
- [x] No DROP; no binding names in `required_columns_ready`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql` (already exists — verify)
- Operator note in pipeline story §G9 / runtime-docs manual if missing

## Out of scope
- Live Railway SQL as P3 DoD
- DROP tables; bind names into `/ready` required set
- Invent Dockerfile; invent HTTP; GPT emit; change `AppConfig`
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
test -f doge-complaints-gateway/supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
rg -n "schema_id|bound_schema_version|profile_id|profile_version|structured_payload|payload_hash" \
  doge-complaints-gateway/supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
rg -n "_STORIES_BINDING_COLUMNS" -A 12 doge-complaints-gateway/src/core/infrastructure/db_supabase.py
```
