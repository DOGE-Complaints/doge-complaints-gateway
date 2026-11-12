# task-gw-ssr-21-t04-story-acceptance-gate

## Task: analyze — story acceptance + G21

## Meta
- **Story:** [STORY-GW-SSR-21](../STORY-GW-SSR-21-node-clustering-docs.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000078
- **Skill declared:** python-pro
- **Depends on:** T01–T03 Done
- **Scaffolded:** 2026-08-30T19:50:48Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-21-node-clustering-docs.md` Target / AC + runbook §6.3
- **Gate Date:** 2026-08-30T19:53:57Z

## Purpose
Story acceptance + G21. Commands from runbook §6.3 **verbatim**. PASS: мануал оба контура + путь «правка pack + рестарт»; 05-env не учит семантические CLUSTER_* как текущий SSOT; cron documented; T-wave G3 строка на месте; closed audits не в diff. After PASS: INDEX/dashboard Status for SSR-21; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-22/06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-21-node-clustering-docs.md`](../STORY-GW-SSR-21-node-clustering-docs.md) §Target / AC
- G21 commands — [`orchestrator-cluster-knobs-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md) §6.3
- T-wave G3 historical — [`orchestrator-t-wave-runbook.md:271`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) `` `GET /tallinn/issues` на месте `` — **do not rewrite**

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-21.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-21-t04.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G21: мануал оба контура; 05-env moved/pack; cron stay; G3 `:271` на месте; audits не в diff
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-22/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-21.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3)

## Out of scope
- Implementing docs (T01–T03); start SSR-22/06/07/12; rewrite G3
- Overlay bans (every task):
  - Docs only. No product runtime except doc-driven typos.
  - Semantic `CLUSTER_*` documented as **moved to pack**. **Keep** `CLUSTER_CRON_*` in env docs.
  - **No ClusterLens add/remove.** Enum stays 10 (`types.py:10–22`).
  - **Нет `GET /schema-active`.** Нет invent HTTP. Нет IDX.
  - Не учить «клиент выбирает pack». Не учить dual-source env+pack.
  - Geo `settlement:tallinn` в pack tallinn — данные зоны, не URL `/tallinn`.
  - **Не переписывать T-wave G3** (`orchestrator-t-wave-runbook.md:271`).
  - **Нет SSR-06/07/12.** Не reopen 01–20. Не стартовать 22…25 в этом pkg.
  - Stay `semantic-schema-runtime`. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать. Closed audits не в diff.

## Verification commands
```bash
# P3 only (G21) — from workspace:
rg -n "node_clustering|exact_lenses" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES|CLUSTER_PRIMARY_LENS|CLUSTER_GEO_SCOPE" \
  doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "CLUSTER_CRON" doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
# G3 historical line (do not rewrite):
rg -n "GET /tallinn/issues" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
