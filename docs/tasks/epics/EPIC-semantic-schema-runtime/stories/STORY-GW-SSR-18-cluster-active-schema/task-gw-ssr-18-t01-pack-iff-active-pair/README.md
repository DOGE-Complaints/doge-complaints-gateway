# task-gw-ssr-18-t01-pack-iff-active-pair

## Task: implement — pack/dual iff NODE_SCHEMA_* (T01)

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000075
- **Skill declared:** python-pro
- **Depends on:** SSR-17 Done (G17)
- **Scaffolded:** 2026-08-30T14:55:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` T01

## Purpose
Pack/dual iff `(story.schema_id, story.bound_schema_version)` == `NODE_SCHEMA_*`. Else skip + log, no membership. Dual from **active** pack.json, not foreign story pack. Do not rewrite `story.schema_id` to env.

## Code Facts
- Bound → `_process_bound_story` — [`cluster_orchestrator.py:274–275`](../../../../../../../src/core/application/cluster_orchestrator.py)
- `_process_bound_story` pack then dual — [`:121–124`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Dual via story pack — [`:90–95`](../../../../../../../src/core/application/cluster_orchestrator.py); [`pack_engine.py:71–79`](../../../../../../../src/core/schema/pack_engine.py)
- G18 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.3

## Acceptance / DoD
- [x] Persist pair ≠ `NODE_SCHEMA_*` → skip (лог), нет pack membership
- [x] Persist pair == env → exact-lenses активного pack; dual только если active pack.json true
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` `process_story` `:274–275` + `_process_bound_story` `:121–124` + `_dual_civic_enabled` `:90–95`

## Out of scope
- ClusterLens member. Подменять `story.schema_id` на env.
- Overlay bans (every task):
  - **Cluster only active pack.** Persist pair ≠ `NODE_SCHEMA_*` → skip (лог), не membership чужим pack.json.
  - **Unbound civic as-is.** `_civic_ready` stays unbound-only. Не migrate civic rows.
  - **Dual only from active pack.json.** Не подменять `story.schema_id` на env.
  - **Нет смены `ClusterLens`.** Civic engine **не** удалять. Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет нового cron. Нет new SQL. Нет IDX.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–17. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "is_schema_bound|_process_bound_story|_dual_civic_enabled" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
```
