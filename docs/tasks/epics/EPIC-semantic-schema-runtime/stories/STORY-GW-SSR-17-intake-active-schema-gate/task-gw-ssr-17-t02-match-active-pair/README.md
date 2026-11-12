# task-gw-ssr-17-t02-match-active-pair

## Task: implement — match binding to NODE_SCHEMA_* (T02)

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000074
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T14:37:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` T02

## Purpose
Parsed pair must equal `AppConfig.node_schema_id` / `node_schema_version`. Else `IntakeValidationError` → HTTP 4xx. Do not rewrite payload `schema_id`.

## Code Facts
- `AppConfig.node_schema_id` / `node_schema_version` — [`schema.py:63–64`](../../../../../../../src/core/config/schema.py)
- `create_story` validates only if `binding is not None` — [`services.py:239–260`](../../../../../../../src/core/application/services.py)
- Submit `IntakeValidationError` → HTTP **400** — [`handlers.py:333–346`](../../../../../../../src/core/api/handlers.py)
- Stash `IntakeValidationError` → HTTP **400** — [`handlers.py:581–584`](../../../../../../../src/core/api/handlers.py)
- G17 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.2

## Acceptance / DoD
- [x] id+version == AppConfig pair; иначе `IntakeValidationError` / 4xx
- [x] Do not rewrite client `schema_id`
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py` `create_story` `:239–260`

## Out of scope
- Silent coerce чужого pack на активный. Rewrite client `schema_id`.
- Overlay bans (every task):
  - **Intake gate only.** Нет/mismatch binding → 4xx. Не civic None. Не silent coerce.
  - **Не подставлять** активный `NODE_SCHEMA_*`, если клиент не прислал pair.
  - **Validate только активный pack.** Не validate чужого `pack.json`.
  - **Нет смены `ClusterLens`.** Civic engine **не** удалять. Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет `POST /node/issues` rewrite.
  - **Нет SSR-06/07/12/18.** Не reopen 01–05/08–16. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Env fixtures = SSR-16 helper. Не `live_integration` как proof.

## Verification commands
```bash
rg -n "node_schema_id|schema_binding" doge-complaints-gateway/src/core/application/services.py
```
