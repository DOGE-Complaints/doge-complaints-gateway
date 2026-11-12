# task-gw-ssr-16-t02-boot-resolve

## Task: implement — boot `resolve_pack` → ConfigError (T02)

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` T02

## Purpose
On start / `load_config_from_env`, `resolve_pack(SchemaRef(schema_id=…, schema_version=…))`. Unknown id / missing version dir → **`ConfigError`** (wrap `UnknownSchemaError` / `UnsupportedVersionError`). No silent civic fallback. Pair = `schema-packs/<id>/<version>/`. Example on disk: `tallinn_civic` / `v1`.

## Code Facts
- `resolve_pack` by `SchemaRef` only; no list-dir; missing id → `UnknownSchemaError`; missing version dir → `UnsupportedVersionError` — [`resolver.py:138–153`](../../../../../../../src/core/schema/resolver.py)
- `SCHEMA_PACKS_ROOT` = `_ENV_PACKS_ROOT`; `default_packs_root` via `os.environ` — [`resolver.py:19`](../../../../../../../src/core/schema/resolver.py), [`:23–30`](../../../../../../../src/core/schema/resolver.py)
- `SchemaRef.schema_id` / `schema_version` — [`contracts.py:24–26`](../../../../../../../src/core/schema/contracts.py)
- `UnknownSchemaError` / `UnsupportedVersionError` — [`errors.py:17–22`](../../../../../../../src/core/schema/errors.py)
- `load_config_from_env` **no** `resolve_pack` this APPLY — [`schema.py:492`](../../../../../../../src/core/config/schema.py), [`:655–684`](../../../../../../../src/core/config/schema.py)
- Packs on disk — `schema-packs/legal_process/v1/pack.json`; `mobility_observation/v1/pack.json`; `tallinn_civic/v1/pack.json`
- `get_api_dependencies` → `load_config_from_env` — [`dependencies.py:16`](../../../../../../../src/core/api/dependencies.py), [`:32`](../../../../../../../src/core/api/dependencies.py)
- G16 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1

## Acceptance / DoD
- [x] Нет пары / нет каталога pack → процесс не стартует (`ConfigError`)
- [x] Каталог на диске резолвится (пример `tallinn_civic` / `v1`)
- [x] Unknown id / missing dir → `ConfigError` (не silent civic fallback)
- [x] `SCHEMA_PACKS_ROOT` остаётся `os.environ` в resolver
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/config/schema.py` `load_config_from_env` (boot)
- Reuse [`resolver.py:138–153`](../../../../../../../src/core/schema/resolver.py) as-is (do not add list-dir)

## Out of scope
- Тихий civic fallback. Invent `ACTIVE_PACK`. Move `SCHEMA_PACKS_ROOT` into AppConfig. Intake 4xx (→ SSR-17).
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n "resolve_pack|UnknownSchemaError|UnsupportedVersionError" doge-complaints-gateway/src/core/config/schema.py
rg -n "SCHEMA_PACKS_ROOT" doge-complaints-gateway/src/core/config/schema.py
```
