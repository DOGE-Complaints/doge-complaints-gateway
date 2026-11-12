# task-gw-ssr-16-t01-config-fields

## Task: implement — EnvSpec + AppConfig `NODE_SCHEMA_*` (T01)

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** SSR-15 Done (G15)
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` T01

## Purpose
`EnvSpec` + `AppConfig` fields `node_schema_id` / `node_schema_version` bound to env **`NODE_SCHEMA_ID`**, **`NODE_SCHEMA_VERSION`**. Both `required=True`, `default=None`. Fail-fast empty (strip + empty → `ConfigError`) like missing `API_BASE_URL` (`_require_value`). Wire `load_config_from_env` constructor. No default «первый pack».

## Code Facts
- `AppConfig` ends `story_draft_ttl_seconds`; **no** node schema fields — [`schema.py:34–62`](../../../../../../../src/core/config/schema.py)
- `EnvSpec` — [`schema.py:18–23`](../../../../../../../src/core/config/schema.py); `ENV_SCHEMA` starts [`:65`](../../../../../../../src/core/config/schema.py)
- `API_BASE_URL` `required=True` — [`schema.py:72–77`](../../../../../../../src/core/config/schema.py)
- `ConfigError` — [`schema.py:9–10`](../../../../../../../src/core/config/schema.py)
- `_require_value` missing required → `ConfigError` — [`schema.py:466–475`](../../../../../../../src/core/config/schema.py)
- `load_config_from_env` `_require_value(API_BASE_URL)` [`:495`](../../../../../../../src/core/config/schema.py); `return AppConfig(` [`:655–684`](../../../../../../../src/core/config/schema.py)
- Etalon missing required — [`test_config_loading.py:102–104`](../../../../../../../tests/test_config_loading.py)
- G16 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1

## Acceptance / DoD
- [x] `NODE_SCHEMA_ID` и `NODE_SCHEMA_VERSION` в AppConfig; оба required
- [x] Fail-fast empty (strip + empty → `ConfigError`); no default «первый pack»
- [x] `SCHEMA_PACKS_ROOT` **не** поле AppConfig
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/config/schema.py` (`AppConfig` `:34–62`, `ENV_SCHEMA` `:65+`, `load_config_from_env` `:492+`)

## Out of scope
- Default «первый pack». `DEFAULT_SCHEMA_PACK`. List-dir. `SCHEMA_PACKS_ROOT` field. Intake 4xx (→ SSR-17).
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" doge-complaints-gateway/src/core/config/schema.py
rg -n "DEFAULT_SCHEMA_PACK|SCHEMA_PACKS_ROOT" doge-complaints-gateway/src/core/config/schema.py
```
