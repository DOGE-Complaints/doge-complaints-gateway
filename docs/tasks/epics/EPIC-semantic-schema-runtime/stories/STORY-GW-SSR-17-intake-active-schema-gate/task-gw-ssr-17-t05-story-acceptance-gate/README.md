# task-gw-ssr-17-t05-story-acceptance-gate

## Task: analyze — story acceptance + G17

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000074
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-08-30T14:37:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` Target / AC + runbook §6.2

## Purpose
Story acceptance + G17. Commands from runbook §6.2 **verbatim**. PASS: civic HTTP без binding 4xx; match 202; mismatch 4xx; GPT UI не в diff; `ClusterLens` = 10; no `GET /schema-active`. After PASS: INDEX/dashboard Status for SSR-17; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-18 in this pkg; **not** start SSR-06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-17-intake-active-schema-gate.md`](../STORY-GW-SSR-17-intake-active-schema-gate.md) §Target / AC (verbatim)
- G17 commands — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.2
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-17.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-17-t05.md` signed (Date post P3 verify only)
- [x] All story Target / AC covered
- [x] G17: civic HTTP без binding → 4xx; match → 202; mismatch → 4xx
- [x] GPT UI files не в diff
- [x] `ClusterLens` members **ровно** baseline (10)
- [x] нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions`
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-18/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-17.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-18/06/07/12
- Overlay bans (every task):
  - **Intake gate only.** Нет/mismatch binding → 4xx. Не civic None. Не silent coerce.
  - **Не подставлять** активный `NODE_SCHEMA_*`, если клиент не прислал pair.
  - **Validate только активный pack.** Не validate чужого `pack.json`.
  - **Нет смены `ClusterLens`.** Civic engine **не** удалять. Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет GPT UI / REQ-45.** Нет `POST /node/issues` rewrite.
  - **Нет SSR-06/07/12/18.** Не reopen 01–05/08–16. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - Env fixtures = SSR-16 helper. Не `live_integration` как proof.

## Verification commands
```bash
# P3 only (G17) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_17_*.py
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "schema-active|/schema-filter|story_dimensions" src/core/api/asgi_app.py
```
