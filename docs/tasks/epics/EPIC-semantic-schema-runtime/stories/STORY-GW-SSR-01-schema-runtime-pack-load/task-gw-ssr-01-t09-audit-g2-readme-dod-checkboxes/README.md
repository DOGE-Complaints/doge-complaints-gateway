# task-gw-ssr-01-t09-audit-g2-readme-dod-checkboxes

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061 (parent product Done); wave `run_mode=gw_ssr_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-01
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md) **G2**
- **Scaffolded:** 2026-08-28T13:26:25Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-01_gap_20260828T132458Z.plan.md` G2 TASKED follow_up=none

## Purpose
Отметить T00–T07 README «Acceptance / DoD» `[x]` по evidence существующих `acceptance-verification-gw-ssr-01-t0N.md` Result PASS. Meta Status уже 🔵 Done. Не re-implement product.

## Code Facts
- T00–T07 Meta Status 🔵 Done (Awaiting Commits)
- Acceptance PASS — e.g. [`acceptance-verification-gw-ssr-01-t00.md`](../task-gw-ssr-01-t00-pack-layout-manifest/acceptance-verification-gw-ssr-01-t00.md)
- DoD checkboxes still `[ ]` — T00 README Acceptance (audit G2); same class T01–T07
- Code Facts «P1 scaffold» in T00/T01 — audit: not the G2 drift; optional Historical note, not required

## Acceptance / DoD
- [x] T00–T07 README Acceptance / DoD items that P3 closed are `[x]`
- [x] Each tick traces to `acceptance-verification-gw-ssr-01-t0N.md` PASS (or gate PASS for T07)
- [x] No product `src/` / pack / test implementation in this task
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-01-t09.md` signed (Date post P6 verify only)

## Where to change
- `task-gw-ssr-01-t00-pack-layout-manifest/README.md` … `task-gw-ssr-01-t07-story-acceptance-gate/README.md` (Acceptance / DoD checkboxes only)

## Out of scope
- G1 SSOT present-tense (T08); G3 nesting test (T10); rewriting Code Facts tables unless needed for Historical label
- INDEX/runbook §4 bans:
  - Не добавлять член в `ClusterLens` (`types.py` :10–22).
  - Не править `lens_dimension` под pack (`engine.py` :66–79).
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` (`gates.py` :11–14) и civic factory (`service_factory.py` :106–109).
  - Не класть binding-колонки в `required_columns_ready` (`db_supabase.py` :336).
  - Не добавлять таблицы в `REQUIRED_READINESS_TABLES` (`:29–43`).
  - Не invent HTTP filter / новый intake path.
  - Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
  - Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
  - `build_index` / `project` — stub/no-op, не «working IDX/PROC».
  - Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
  - Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
  - Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».

## Verification commands
```bash
rg -n 'Acceptance / DoD|- \[ \]' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-01-schema-runtime-pack-load/task-gw-ssr-01-t0*/README.md
```
