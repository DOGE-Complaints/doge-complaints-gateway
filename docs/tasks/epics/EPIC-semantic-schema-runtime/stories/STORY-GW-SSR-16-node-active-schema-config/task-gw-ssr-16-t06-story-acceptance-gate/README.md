# task-gw-ssr-16-t06-story-acceptance-gate

## Task: analyze — story acceptance + G16

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000073
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-08-30T14:18:27Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` Target / AC + runbook §6.1
- **Gate Date:** 2026-08-30T14:24:58Z

## Purpose
Story acceptance + G16. Commands from runbook §6.1 **verbatim**. PASS: missing env `ConfigError`; existing pack loads; missing dir `ConfigError`; both fields required; `ClusterLens` = 10; no `GET /schema-active`. After PASS: INDEX/dashboard Status for SSR-16; pie T-wave **no**. **Not** `gateway-mvp-dashboard.md`; **not** bullrun §«Актуальная точка»; **not** start SSR-17 in this pkg; **not** start SSR-06/07/12.

## Code Facts
- Template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Story AC — [`STORY-GW-SSR-16-node-active-schema-config.md`](../STORY-GW-SSR-16-node-active-schema-config.md) §Target / AC (verbatim)
- G16 commands — [`orchestrator-node-schema-runbook.md`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md) §6.1
- `ClusterLens` baseline 10 — [`types.py:10–22`](../../../../../../../src/core/cluster/types.py)
- Wave dashboard — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md) (P3 Done Status OK; pie T-wave no)

## Acceptance / DoD
- [x] `story-acceptance-gate-STORY-GW-SSR-16.md` with AC checklist (verbatim) PASS/FAIL + evidence paths
- [x] `acceptance-verification-gw-ssr-16-t06.md` signed (Date post P3 verify only — replace scaffold floor)
- [x] All story Target / AC covered
- [x] G16: pytest `test_gw_ssr_16_*` зелёный
- [x] missing env → `ConfigError`; существующий pack грузится; несуществующий id → fail-fast
- [x] оба поля required в `AppConfig` / `ENV_SCHEMA`
- [x] `ClusterLens` members **ровно** baseline (10)
- [x] нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions`
- [x] Live `--project gateway --verify` recorded
- [x] BULLRUN phases complete
- [x] Do **not** rewrite bullrun §«Актуальная точка»; do **not** edit `gateway-mvp-dashboard.md`; pie T-wave no. Do not start SSR-17/06/07/12.

## Where to change
- This folder: `story-acceptance-gate-STORY-GW-SSR-16.md` (P3 — replace Result/Date after live verify)
- Sync SSR INDEX / `gateway-semantic-schema-runtime-dashboard.md` on PASS (P3) — not this P1 scaffold.

## Out of scope
- Implementing missing product gaps; P3 execution; start SSR-17/06/07/12
- Overlay bans (every task):
  - **`NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` only.** Не invent `DEFAULT_SCHEMA_PACK` / `ACTIVE_PACK`.
  - **`SCHEMA_PACKS_ROOT` не поле `AppConfig`.** Остаётся `os.environ` в `resolver.py:19–30`.
  - **Нет intake gate** — SSR-17. **Нет смены `ClusterLens`.** Нет `GET /schema-active`. Нет filter HTTP. Нет `story_dimensions`.
  - **Нет SSR-06/07/12.** Не reopen 01–05/08–15. Stay `semantic-schema-runtime`.
  - Не переписывать T-wave G3. Не переписывать bullrun §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md` / `spa-mvp-dashboard.md`. Pie T-wave **не** трогать.
  - G16 **не** полный suite (фикстуры HTTP без env — массовая правка в 17).

## Verification commands
```bash
# P3 only (G16) — from doge-complaints-gateway:
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_16_*.py
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```
