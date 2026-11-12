# task-gw-ssr-16-t03-lifespan-log

## Task: implement — lifespan log active pair (T03)

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` T03

## Purpose
Log `node_schema_id` / version next to existing `startup.config`. No payload dump.

## Code Facts
- Lifespan logs `db_backend` / cron, **not** pack id — [`asgi_app.py:110–137`](../../../../../../../src/core/api/asgi_app.py)
- `get_api_dependencies` → `deps.config` — [`asgi_app.py:114`](../../../../../../../src/core/api/asgi_app.py); [`dependencies.py:32`](../../../../../../../src/core/api/dependencies.py)
- No `GET /schema-active` / `story_dimensions` / `schema-filter` in asgi this APPLY — 0 hits `asgi_app.py`
- G16 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1

## Acceptance / DoD
- [x] Lifespan логирует активную пару (`node_schema_id` / version)
- [x] No dump `structured_payload` / pack.json
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/api/asgi_app.py` `_lifespan` (рядом с `startup.config`)

## Out of scope
- Dump payload. `GET /schema-active`. Intake 4xx (→ SSR-17).
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "node_schema_id|NODE_SCHEMA" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "schema-active|story_dimensions|/schema-filter" doge-complaints-gateway/src/core/api/asgi_app.py
```
