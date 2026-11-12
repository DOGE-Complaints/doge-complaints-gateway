# task-gw-ssr-17-t04-tests

## Task: tests — G17 reject/accept + civic HTTP fixtures (T04)

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000074
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-08-30T14:37:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` T04

## Purpose
`tests/test_gw_ssr_17_*`: reject absent/mismatch; accept match (202). Adapt civic HTTP fixtures (binding + env): req24, e2e sandbox, `tests/smoke` intake ls02/ls03, `test_gw_ssr_03` civic-absent, grep POST без `schema_binding`. Env = SSR-16 helper. Adapt, не skip всех.

## Code Facts
- SSR-03 civic-absent / `{}` still None — [`test_gw_ssr_03_optional_v2_semantic_wire.py:57–71`](../../../../../../../tests/test_gw_ssr_03_optional_v2_semantic_wire.py)
- Helper — [`gw_ssr_16_node_schema.py`](../../../../../../../tests/gw_ssr_16_node_schema.py)
- `tests/test_gw_ssr_17_*` — **0 files** at scaffold
- G17 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.2

## Acceptance / DoD
- [x] reject absent/`{}`/null; reject mismatch id or version
- [x] accept match → 202
- [x] civic HTTP fixtures adapted (binding + env), не skip-all
- [x] GPT UI files не в diff
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/tests/test_gw_ssr_17_*.py`
- civic HTTP fixtures: req24, e2e sandbox, `tests/smoke` ls02/ls03, `test_gw_ssr_03` civic-absent

## Out of scope
- `live_integration` как proof. GPT UI files. Skip-all civic suite.
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
# P3 only — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_17_*.py
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py
```
