# task-gw-ssr-20-t05-tests

## Task: tests — conftest / config / clustering / suite (T05)

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` T05

## Purpose
`conftest` без monkeypatch семантических CLUSTER_*; `test_config_loading` / `test_cluster_active_lenses_runtime_effect` / config env contracts переписать; civic `test_clustering_engine.py` зелёный; dual path; missing env `CLUSTER_MIN_SIZE` больше не ConfigError. `tests/test_gw_ssr_20_*` для G20. Full offline suite зелёный (runbook §6.2).

## Code Facts
- Conftest overlay — [`conftest.py:60–74`](../../../../../../../tests/conftest.py)
- G20 scope — `tests/test_gw_ssr_20_*.py` (0 files at P1) + `tests/test_clustering_engine.py` + full offline
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [ ] `test_gw_ssr_20_*` + `test_clustering_engine.py` зелёные
- [ ] Offline suite (`-m "not live_integration"`) зелёный после адаптации фикстур
- [ ] Missing env `CLUSTER_MIN_SIZE` больше не ConfigError
- [ ] `ClusterLens` = 10
- [ ] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_20_*.py`
- `doge-complaints-gateway/tests/conftest.py`
- existing config / clustering / active-lenses tests as needed for suite green

## Out of scope
- `live_integration` proof. GPT UI. Start SSR-21.
- Overlay bans (every task):
  - Factory/handlers from **active** pack `node_clustering.civic`. No env override поверх pack.
  - Remove semantic `CLUSTER_*` from AppConfig; **keep** `CLUSTER_CRON_*`.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет filter HTTP. Нет IDX.
  - Не менять civic `require_actionable_canonical_type=True` (только числа из pack).
  - **Нет SSR-06/07/12.** Не reopen 01–19. Не стартовать 21/22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_20_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
```
