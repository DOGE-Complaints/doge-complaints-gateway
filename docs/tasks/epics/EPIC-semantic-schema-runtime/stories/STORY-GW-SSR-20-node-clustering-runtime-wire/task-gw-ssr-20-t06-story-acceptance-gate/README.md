# task-gw-ssr-20-t06-story-acceptance-gate

## Task: analyze — story acceptance + G20

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000077
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-08-30T19:31:05Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` Target / AC + runbook §6.2

## Purpose
Story acceptance + G20. Commands from runbook §6.2 **verbatim**. PASS: civic engine/gate/min_size from active pack; semantic CLUSTER_* not in AppConfig; `CLUSTER_CRON_*` stay; missing block → ConfigError; full offline pytest green; ClusterLens=10; no filter HTTP. After PASS: INDEX/dashboard Status for SSR-20; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-21/06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-20-node-clustering-runtime-wire.md`](../STORY-GW-SSR-20-node-clustering-runtime-wire.md) §Target / AC
- G20 commands — [`orchestrator-cluster-knobs-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md) §6.2
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)

## Acceptance / DoD
- [ ] `story-acceptance-gate-STORY-GW-SSR-20.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [ ] `acceptance-verification-gw-ssr-20-t06.md` signed (Date post P3 verify only)
- [ ] All story Target / AC covered
- [ ] G20: pytest 20 + clustering_engine + full offline; no semantic CLUSTER_* required; cron stay; ClusterLens=10
- [ ] Live `--project gateway --verify` recorded
- [ ] BULLRUN phases complete
- [ ] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-21/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-20.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing missing product gaps; start SSR-21/06/07/12
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
# P3 only (G20) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_20_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration"
rg -n "cluster_min_size|CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES" src/core/config/schema.py
rg -n "CLUSTER_CRON_ENABLED|CLUSTER_CRON_INTERVAL_S" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```
