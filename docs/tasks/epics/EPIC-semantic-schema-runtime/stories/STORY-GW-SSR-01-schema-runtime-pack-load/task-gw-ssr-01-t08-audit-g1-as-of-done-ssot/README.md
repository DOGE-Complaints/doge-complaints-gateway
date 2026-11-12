# task-gw-ssr-01-t08-audit-g1-as-of-done-ssot

## Meta
- **Story:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000061 (parent product Done); wave `run_mode=gw_ssr_01_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-01
- **Depends on:** T00–T07 Done
- **Audit ref:** [`audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md`](../../../../../../analysis/audit-gw-ssr-01-schema-runtime-pack-load-2026-08-28.md) **G1**
- **Scaffolded:** 2026-08-28T13:26:25Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-01_gap_20260828T132458Z.plan.md` G1 TASKED follow_up=none

## Purpose
As-of-Done vs Historical split для persistent SSOT: INDEX seam «jsonschema **нет**»; backlog + pipeline §Verified current state (`src/core/schema/` / `jsonschema` **Not found**); epic Problem Statement «нет schema/packs/jsonschema»; root `backlog-stories/INDEX.md` epic-id `_(none yet)_` while `EPIC-semantic-schema-runtime.md` exists. Без правки runtime.

## Code Facts
- Runtime on disk — Glob `src/core/schema/` (8 files post-P3)
- Packs on disk — `schema-packs/legal_process/v1`, `schema-packs/mobility_observation/v1`, `schema-packs/README.md`
- `jsonschema>=4.18.0` — [`pyproject.toml:16`](../../../../../../../pyproject.toml); [`requirements.txt:5`](../../../../../../../requirements.txt)
- Stale INDEX seam — [`semantic-schema-runtime/INDEX.md:112`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «jsonschema **нет**»
- Stale verified table — backlog [`STORY-GW-SSR-01`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md) §Verified current state; pipeline copy same story folder
- Stale epic lead — [`EPIC-semantic-schema-runtime.md:16`](../../../../../epics/EPIC-semantic-schema-runtime.md)
- Root INDEX — [`backlog-stories/INDEX.md:48`](../../../../../backlog-stories/INDEX.md) `_(none yet)_` / «epic id не invent»
- Product Status 🔵 Done; gate PASS 2026-08-28T13:18:56Z

## Acceptance / DoD
- [x] INDEX seam JSON Schema lib: As-of-Done (declared + importable) vs Historical (pre-P3)
- [x] Backlog + pipeline §Verified current state: Current facts (`src/core/schema/` exists, jsonschema in deps) vs Historical pre-P3
- [x] Epic Problem Statement does not claim absence of schema/packs/jsonschema as present tense
- [x] Root `backlog-stories/INDEX.md` epic map row points at `EPIC-semantic-schema-runtime` (not `_(none yet)_`)
- [x] No `src/` / pack / intake edits
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-01-t08.md` signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` (seam row)
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md` (§Verified current state)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-01-schema-runtime-pack-load/STORY-GW-SSR-01-schema-runtime-pack-load.md` (same table)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Problem Statement)
- `doge-complaints-gateway/docs/tasks/backlog-stories/INDEX.md` (epic-id row)

## Out of scope
- G2 README DoD checkboxes (T09); G3 nesting test (T10); G4 bullrun §Актуальная точка
- Runtime / pack / intake / identity
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
rg -n 'jsonschema.*нет|Not found|нет `src/core/schema`' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md
rg -n 'EPIC-semantic-schema-runtime|none yet' doge-complaints-gateway/docs/tasks/backlog-stories/INDEX.md
```
