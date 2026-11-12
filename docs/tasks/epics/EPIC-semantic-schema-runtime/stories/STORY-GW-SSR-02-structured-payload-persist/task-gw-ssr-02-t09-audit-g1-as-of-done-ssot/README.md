# task-gw-ssr-02-t09-audit-g1-as-of-done-ssot

## Meta
- **Story:** [STORY-GW-SSR-02](../STORY-GW-SSR-02-structured-payload-persist.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000062 (parent product Done); wave `run_mode=gw_ssr_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-02
- **Depends on:** T00–T08 Done
- **Audit ref:** [`audit-gw-ssr-02-structured-payload-persist-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-02-structured-payload-persist-2026-08-28.md) **G1**
- **Scaffolded:** 2026-08-28T13:53:59Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-02_gap_20260828T135245Z.plan.md` G1 TASKED follow_up=none

## Purpose
As-of-Done vs Historical split для persistent SSOT: backlog SSR-02 §Verified still `structured_payload` **Not found** / lifecycle «by name, not `replace`»; INDEX persist constructors + Hosted SELECT seams still pre-P3 line cites. Без правки persist runtime.

## Code Facts
- Product binding on disk — [`contracts.py:68–74`](../../../../../../../src/core/domain/contracts.py)
- Lifecycle — [`services.py:461–465`](../../../../../../../src/core/application/services.py) `replace(current, lifecycle_status=…, updated_at=…)`
- sqlite INSERT+SET live — [`db_sqlite.py:597–646`](../../../../../../../src/core/infrastructure/db_sqlite.py) (`ON CONFLICT` `:610`; `bound_schema_version = excluded…` `:642`)
- supabase save live — [`db_supabase.py:496+`](../../../../../../../src/core/infrastructure/db_supabase.py); omit-probe binding [`:470–476`](../../../../../../../src/core/infrastructure/db_supabase.py) `_STORIES_BINDING_COLUMNS`; `required_columns_ready` [`:388`](../../../../../../../src/core/infrastructure/db_supabase.py)
- Stale backlog verified — [`STORY-GW-SSR-02:32–34`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md) **Not found** / reconstruct by name
- Stale INDEX seams — [`INDEX.md:109–111`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) lifecycle copy **без новых полей**; sqlite cite `:537–569`; supabase row `:439–462`; omit-probe **только** `geo_admin_*`; `required_columns_ready` cite `:336`
- Pipeline §Verified **updated** in P3 (not this gap’s primary target)
- Product Status 🔵 Done; gate PASS 2026-08-28T13:47:57Z

## Acceptance / DoD
- [x] Backlog SSR-02 §Verified current state: Current (binding fields exist; `replace` lifecycle) vs Historical (pre-P3 Not found / by-name reconstruct)
- [x] INDEX persist constructors seam: As-of-Done (`replace` + live sqlite INSERT/SET cites) vs Historical pre-P3
- [x] INDEX Hosted SELECT seam: omit-probe includes binding; `required_columns_ready` cite live `:388` (not `:336`); binding still **not** in `/ready` required set
- [x] No `src/` / migration / intake edits
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-02-t09.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md` (§Verified current state)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` (persist constructors + Hosted SELECT seams)

## Out of scope
- G2 sqlite `save_story` return hash (T10); G3 bullrun §Актуальная точка
- Persist algorithm / hash helper / CREATE TABLE rewrite
- INDEX/runbook §4 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :106–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :388).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path.
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`.

## Verification commands
```bash
rg -n 'Not found|by name, not .replace|lifecycle copy без новых полей|db_sqlite.py:537|db_supabase.py:439|omit-probe только' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
```
