# task-gw-ssr-17-t03-validate-active-pack

## Task: implement — validate payload against active pack (T03)

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000074
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-08-30T14:37:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` T03

## Purpose
On match only: `validate` payload against **active** pack (`resolve_pack` / `SchemaRef` той же env-пары), not the client's foreign pack.json. Persist binding as today.

## Code Facts
- `create_story` `runtime.resolve` / `runtime.validate` — [`services.py:246–260`](../../../../../../../src/core/application/services.py)
- Persist binding after validate — [`services.py:263–268`](../../../../../../../src/core/application/services.py)
- Active pair already on AppConfig — [`schema.py:63–64`](../../../../../../../src/core/config/schema.py)
- G17 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.2

## Acceptance / DoD
- [x] Match → validate + persist binding against **active** pack
- [x] Do not validate чужого pack.json
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/application/services.py` `create_story` `:246–260`

## Out of scope
- Validate чужого pack. `POST /node/issues`. Cluster skip (→18).
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
rg -n "runtime.validate|SchemaRef|node_schema" doge-complaints-gateway/src/core/application/services.py
```
