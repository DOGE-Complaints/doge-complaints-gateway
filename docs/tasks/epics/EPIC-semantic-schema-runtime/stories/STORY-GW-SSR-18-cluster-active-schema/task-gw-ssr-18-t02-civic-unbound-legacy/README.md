# task-gw-ssr-18-t02-civic-unbound-legacy

## Task: implement — unbound civic as-is (T02)

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000075
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T14:55:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` T02

## Purpose
Unbound READY_FOR_PROFILE civic as-is. `_civic_ready` stays unbound-only. Do not migrate civic rows. Do not delete civic engine.

## Code Facts
- `_civic_ready` unbound only — [`cluster_orchestrator.py:87–88`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic branch after bound check — [`:277`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic unlabeled tests — [`test_clustering_engine.py`](../../../../../../../tests/test_clustering_engine.py)
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- G18 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.3

## Acceptance / DoD
- [x] Unbound READY_FOR_PROFILE → civic path as-is
- [x] `ClusterLens` members remain 10
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/cluster_orchestrator.py` `_civic_ready` `:87–88` + civic branch after `:277`

## Out of scope
- Migrate civic rows. Удаление civic engine. ClusterLens member.
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
rg -n "_civic_ready|is_schema_bound" doge-complaints-gateway/src/core/application/cluster_orchestrator.py
```
