# task-gw-ssr-18-t05-story-acceptance-gate

## Task: analyze — story acceptance + G18

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000075
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-08-30T14:55:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` Target / AC + runbook §6.3

## Purpose
Story acceptance + G18. Commands from runbook §6.3 **verbatim**. PASS: skip log; civic engine green; offline pytest; мануал не учит «клиент любой pack»; `ClusterLens` = 10; no `GET /schema-active`. After PASS: INDEX/dashboard Status for SSR-18; pie T-wave **no**; волна node-schema закрыта. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-18-cluster-active-schema.md`](../STORY-GW-SSR-18-cluster-active-schema.md) §Target / AC (verbatim)
- G18 commands — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.3
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-18.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-18-t05.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G18: mismatch skip; civic unlabeled green; full offline pytest
- [x] мануал не учит «клиент выбирает любой pack» / «решает тело intake»
- [x] `ClusterLens` members **ровно** baseline (10)
- [x] нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions`
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-18.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-06/07/12
- Overlay bans (every task):
  - **Cluster only active pack.** Persist pair ≠ `NODE_SCHEMA_*` → skip (лог), не membership чужим pack.json.
  - **Unbound civic as-is.** `_civic_ready` stays unbound-only. Не migrate civic rows.
  - **Dual only from active pack.json.** Не подменять `story.schema_id` на env.
  - **Нет смены `ClusterLens`.** Civic engine **не** удалять. Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет нового cron. Нет new SQL. Нет IDX.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–17. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Не `live_integration` как proof.

## Verification commands
```bash
# P3 only (G18) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_18_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration"
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "клиент выбирает любой pack|решает тело intake" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```
