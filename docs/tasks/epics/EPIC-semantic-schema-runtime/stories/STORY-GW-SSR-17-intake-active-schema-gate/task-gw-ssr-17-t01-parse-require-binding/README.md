# task-gw-ssr-17-t01-parse-require-binding

## Task: implement — require schema_binding (T01)

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000074
- **Skill declared:** python-pro
- **Depends on:** SSR-16 Done (G16)
- **Scaffolded:** 2026-08-30T14:37:24Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` T01

## Purpose
Absent key / `{}` / `null` → `IntakeValidationError` (не civic None). Same parse on stash. Do not invent civic fallback.

## Code Facts
- Binding optional; empty/`null` → civic None — [`contracts.py:227–232`](../../../../../../../src/core/intake/contracts.py)
- Absent key → skip parse, stays None — [`contracts.py:480–482`](../../../../../../../src/core/intake/contracts.py)
- Stash copies binding onto submit — [`contracts.py:585`](../../../../../../../src/core/intake/contracts.py)
- SSR-03 civic-absent / `{}` still None — [`test_gw_ssr_03_optional_v2_semantic_wire.py:57–71`](../../../../../../../tests/test_gw_ssr_03_optional_v2_semantic_wire.py)
- G17 — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.2

## Acceptance / DoD
- [x] Absent `schema_binding` / `{}` / `null` → `IntakeValidationError` (не civic None)
- [x] Same parse on stash
- [x] BULLRUN phases complete

## Where to change
- `doge-complaints-gateway/src/core/intake/contracts.py` `_parse_schema_binding_block` `:227–263` + call site `:480–482`; stash `:585`

## Out of scope
- Civic None. Подставлять активный id. GPT UI.
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
rg -n "_parse_schema_binding_block|schema_binding" doge-complaints-gateway/src/core/intake/contracts.py
```
