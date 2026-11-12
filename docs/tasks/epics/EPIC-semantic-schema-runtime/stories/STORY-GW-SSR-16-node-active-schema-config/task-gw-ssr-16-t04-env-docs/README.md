# task-gw-ssr-16-t04-env-docs

## Task: docs — `.env.test.example` + server-env section (T04)

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` T04

## Purpose
`.env.test.example` **две строки** (`NODE_SCHEMA_ID`, `NODE_SCHEMA_VERSION`). `server-env-quickstart.md` **одна секция**. Example pair on disk: `tallinn_civic` / `v1`.

## Code Facts
- `.env.test.example` — **0** `NODE_SCHEMA_*` / `SCHEMA_PACK` this APPLY — [`doge-complaints-gateway/.env.test.example`](../../../../../../../.env.test.example)
- `server-env-quickstart.md` exists — [`docs/runtime-docs/manuals/server-env-quickstart.md`](../../../../../runtime-docs/manuals/server-env-quickstart.md)
- `SCHEMA_PACKS_ROOT` documented **not** in AppConfig — [`05-env-config-and-launch.md:37`](../../../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md), [`:123`](../../../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md)
- G16 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1

## Acceptance / DoD
- [x] `.env.test.example` две строки `NODE_SCHEMA_ID` + `NODE_SCHEMA_VERSION`
- [x] `server-env-quickstart.md` одна секция (пример `tallinn_civic` / `v1`)
- [x] `SCHEMA_PACKS_ROOT` не описан как required поле AppConfig
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/.env.test.example`
- `doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md`

## Out of scope
- Railway secrets invent. New hosted env names. Move `SCHEMA_PACKS_ROOT` into AppConfig docs as a required AppConfig field.
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" doge-complaints-gateway/.env.test.example
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md
```
