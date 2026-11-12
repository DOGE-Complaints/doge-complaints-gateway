# task-gw-ssr-09-t04-story-acceptance-gate

## Task: analyze — story acceptance + G9

## Meta
- **Story:** [STORY-GW-SSR-09](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000067
- **Skill declared:** python-pro
- **Depends on:** T01–T03 Done
- **Scaffolded:** 2026-08-29T18:09:45Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-09-hosted-apply-and-pack-image.md` Target / AC + runbook §6.2
- **Gate Date:** 2026-08-29T18:14:04Z

## Purpose
Story acceptance + G9. Commands from runbook §6.2. Explicit: hosted apply = operator/deploy, not overnight proof. After PASS: INDEX/dashboard Status for SSR-09; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-10 in this pkg.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-09-….md`](../STORY-GW-SSR-09-hosted-apply-and-pack-image.md) §Target / AC (verbatim)
- G9 commands — [`orchestrator-post-t-wave-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md) §6.2
- Gate **Date:** only after `--print-utc-now` post live `--verify` (P3) — not P1
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-09.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-09-t04.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G9: `test -f` migration; `rg required_columns_ready`; binding names in `db_supabase.py`; `test -d schema-packs`; `rg story_dimensions|/schema-filter` empty
- [x] Gate/wave note: hosted apply = operator/deploy, not overnight proof
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/10/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-09.md` (P3)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold. No product code required if T01–T03 already satisfy G9 on disk.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-10
- Live Railway apply as overnight DoD; invent Dockerfile
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
# P3 only (G9):
cd doge-complaints-gateway
test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
rg -n "required_columns_ready" -A 40 src/core/infrastructure/db_supabase.py
rg -n "schema_id|bound_schema_version|structured_payload" src/core/infrastructure/db_supabase.py
test -d schema-packs
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```
