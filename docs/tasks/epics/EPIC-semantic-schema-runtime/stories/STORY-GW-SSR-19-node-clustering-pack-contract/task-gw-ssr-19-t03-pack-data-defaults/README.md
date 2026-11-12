# task-gw-ssr-19-t03-pack-data-defaults

## Task: data — three packs with EnvSpec civic defaults (T03)

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** data
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` T03

## Purpose
Fill `node_clustering.civic` from **current EnvSpec defaults** (`schema.py:166–240`). Tallinn `geo_scope` = `settlement:tallinn`. `legal_process` / `mobility_observation` `geo_scope` = `null`. Do not invent thresholds. Do not copy conftest-reduced `MIN_SIZE_BY_LENS` into pack.json.

## Code Facts
- Three packs exist; no `node_clustering` key — `schema-packs/{tallinn_civic,legal_process,mobility_observation}/v1/pack.json`
- EnvSpec defaults — [`schema.py:166–240`](../../../../../../../src/core/config/schema.py): `CLUSTER_MIN_SIZE=5`; `MIN_SIZE_BY_LENS` includes `composite_primary_micro=8`; readiness `60`; 10 lenses; primary `composite_primary_micro`; signal `canonical`; id `sha256`; geo_filter `country`; geo_scope `None`; tie `alpha`; type `canonical_priority`
- Conftest overlay (test-process only) — [`conftest.py:60–74`](../../../../../../../tests/conftest.py): `MIN_SIZE_BY_LENS` **без** `composite_primary_micro=8`

## Acceptance / DoD
- [x] Три example pack с заполненным блоком
- [x] tallinn: `geo_scope=settlement:tallinn`
- [x] legal_process / mobility: `geo_scope` null
- [x] Нет новых порогов «на глаз»; нет cron keys in pack
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json`
- `doge-complaints-gateway/schema-packs/legal_process/v1/pack.json`
- `doge-complaints-gateway/schema-packs/mobility_observation/v1/pack.json`

## Out of scope
- Новые пороги «на глаз». Cron keys in pack. Factory wire (→20).
- Overlay bans (every task):
  - **`node_clustering.civic` loader + pack data only.** No factory / handler wire (→20).
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **No cron in pack.** `CLUSTER_CRON_*` stay env (D-SSR-9).
  - **No env override** «поверх pack» this story.
  - **Values from current EnvSpec / conftest defaults.** Do not invent new thresholds.
  - **Нет `GET /schema-active`.** Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет new SQL. Нет IDX.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–18. Не стартовать 20/21/22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
rg -n "node_clustering" \
  doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json \
  doge-complaints-gateway/schema-packs/legal_process/v1/pack.json \
  doge-complaints-gateway/schema-packs/mobility_observation/v1/pack.json
rg -n "settlement:tallinn" doge-complaints-gateway/schema-packs/tallinn_civic/v1/pack.json
```
