# task-gw-ssr-19-t04-tests

## Task: tests — load / missing / invalid primary (T04)

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` T04

## Purpose
`tests/test_gw_ssr_19_*`: load ok; missing `node_clustering` → loader error; invalid primary → error; `ClusterLens` enum not extended.

## Code Facts
- `tests/test_gw_ssr_19_*` — **0 files** at P1 scaffold
- Loader error type — [`errors.py:21`](../../../../../../../src/core/schema/errors.py) `UnsupportedVersionError`
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [x] load ok для pack с валидным блоком
- [x] missing `node_clustering` → loader error
- [x] invalid primary → loader error
- [x] `ClusterLens` members ровно 10
- [x] Нет factory wire tests as product of this story
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_19_*.py`

## Out of scope
- Factory wire (→20). `live_integration` proof.
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
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_19_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```
