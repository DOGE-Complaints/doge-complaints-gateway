# task-gw-ssr-18-t03-tests

## Task: tests — G18 mismatch skip + match pack + civic (T03)

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000075
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-08-30T14:55:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` T03

## Purpose
`tests/test_gw_ssr_18_*`: mismatch bound skip; match pack membership; unlabeled civic `test_clustering_engine.py` зелёный. Не `live_integration` как proof.

## Code Facts
- Bound → pack **этой** story — [`cluster_orchestrator.py:274–275`](../../../../../../../src/core/application/cluster_orchestrator.py)
- Civic unlabeled — [`test_clustering_engine.py`](../../../../../../../tests/test_clustering_engine.py)
- `tests/test_gw_ssr_18_*` — **0 files** at scaffold
- G18 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.3

## Acceptance / DoD
- [x] mismatch bound → skip (нет pack membership чужим pack.json)
- [x] match env pair → pack exact membership
- [x] civic unlabeled `test_clustering_engine.py` зелёный
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_18_*.py`
- keep `tests/test_clustering_engine.py` green

## Out of scope
- Второй cron. `live_integration` proof. GPT UI.
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
# P3 only — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_18_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
```
