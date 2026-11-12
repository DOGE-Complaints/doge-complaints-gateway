# task-gw-ssr-19-t00-contract-readme

## Task: add — document `node_clustering.civic` key (T00)

## Meta
- **Story:** [STORY-GW-SSR-19](../STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000076
- **Skill declared:** python-pro
- **Depends on:** SSR-18 Done (G18)
- **Scaffolded:** 2026-08-30T19:16:21Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md` T00

## Purpose
Зафиксировать shape `node_clustering.civic` в `schema-packs/README.md` (SCHEMA-005, not frozen YAML dialect).

## Code Facts
- README keys exact/dual/card; no civic block — [`schema-packs/README.md:26–29`](../../../../../../../schema-packs/README.md)
- Civic knobs only AppConfig — [`schema.py:47–59`](../../../../../../../src/core/config/schema.py); EnvSpec [`:166–240`](../../../../../../../src/core/config/schema.py)
- D-SSR-9 — [`INDEX.md:52`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- G19 — [`orchestrator-cluster-knobs-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md) §6.1

## Acceptance / DoD
- [x] `schema-packs/README.md` документирует ключ `node_clustering.civic` и поля из story In
- [x] Не invent frozen YAML dialect
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/schema-packs/README.md` (рядом с `exact_lenses` / `dual_civic_lenses` / `card_fields`)

## Out of scope
- Frozen YAML dialect invent. Factory wire (→20).
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
rg -n "node_clustering" doge-complaints-gateway/schema-packs/README.md
```
