# task-gw-ssr-19-t02-loader-parse-validate

## Task: implement — parse + validate `node_clustering.civic` (T02)

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` T02

## Purpose
Parse + validate; missing `node_clustering` / invalid primary → `UnsupportedVersionError` (loader error as-of SSR-01). Mirror `schema.py` (`primary ∈ active`, known lens ids, ranges 1–100). No silent default without block.

## Code Facts
- Resolver parses exact/dual/card; **no** `node_clustering` — [`resolver.py:38–62,120–134`](../../../../../../../src/core/schema/resolver.py)
- Missing/invalid pack keys → `UnsupportedVersionError` — [`errors.py:21`](../../../../../../../src/core/schema/errors.py)
- Primary ∈ active + known lens — [`schema.py:460–469`](../../../../../../../src/core/config/schema.py)
- min_size positive int; readiness ≤100 — [`schema.py:605–616`](../../../../../../../src/core/config/schema.py)

## Acceptance / DoD
- [x] Нет блока / битый primary → loader error (`UnsupportedVersionError`)
- [x] Valid block → `SchemaContext` populated
- [x] Нет silent default без блока; нет env override
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/schema/resolver.py` (`:120–134` return + new parse)

## Out of scope
- Silent default без блока. Factory/`ConfigError` boot (→20). Env override.
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
rg -n "node_clustering|UnsupportedVersionError" doge-complaints-gateway/src/core/schema/resolver.py
```
