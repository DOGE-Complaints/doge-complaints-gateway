# task-gw-ssr-19-t05-story-acceptance-gate

## Task: analyze — story acceptance + G19

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** T00–T04 Done
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` Target / AC + runbook §6.1

## Purpose
Story acceptance + G19. Commands from runbook §6.1 **verbatim**. PASS: pytest 19; three packs with block; README key; ClusterLens=10; factory still reads AppConfig CLUSTER_*. After PASS: INDEX/dashboard Status for SSR-19; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-20/06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-19-node-clustering-pack-contract.md`](../STORY-GW-SSR-19-node-clustering-pack-contract.md) §Target / AC (verbatim)
- G19 commands — [`orchestrator-cluster-knobs-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md) §6.1
- Factory still CLUSTER_* — [`service_factory.py:93–113`](../../../../../../../src/core/infrastructure/service_factory.py)
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-19.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-19-t05.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G19: pytest 19; three packs; README key; ClusterLens=10; factory still AppConfig CLUSTER_*
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-20/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-19.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-20/06/07/12
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
# P3 only (G19) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_19_*.py
rg -n "node_clustering" schema-packs/README.md src/core/schema/
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "node_clustering" schema-packs/tallinn_civic/v1/pack.json schema-packs/legal_process/v1/pack.json schema-packs/mobility_observation/v1/pack.json
```
