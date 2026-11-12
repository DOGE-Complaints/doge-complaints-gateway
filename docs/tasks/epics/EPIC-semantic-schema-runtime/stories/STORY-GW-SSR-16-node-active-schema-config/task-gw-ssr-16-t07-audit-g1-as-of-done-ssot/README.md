# task-gw-ssr-16-t07-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-16 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-16](../STORY-GW-SSR-16-node-active-schema-config.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000073 (parent product AC Done); wave `run_mode=gw_ssr_16_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-16
- **Depends on:** T01–T06 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-16-node-active-schema-config-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-16-node-active-schema-config-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T14:30:53Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-16_gap_20260830T142856Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T14:31:42Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT still Todo/Historical vs product Done. Backlog §Verified present-tense «без node schema полей» / lifespan не pack id; epic PS «SSR-16…18 Todo» без As-of-Done SSR-16; dashboard Notes/epic-rollup/wave `:92` still Todo. Docs only. No runtime. No intake 4xx (→17). No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-16-node-active-schema-config-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-16-node-active-schema-config-2026-08-30.md) §3 / §5.
2. Product fields exist — [`schema.py:63–64`](../../../../../../../src/core/config/schema.py) `node_schema_id` / `node_schema_version`; EnvSpec [`:262–268`](../../../../../../../src/core/config/schema.py); `_require_value` [`:684–685`](../../../../../../../src/core/config/schema.py).
3. Lifespan logs pair — [`asgi_app.py:121–128`](../../../../../../../src/core/api/asgi_app.py).
4. Stale backlog §Verified — [`STORY-GW-SSR-16-node-active-schema-config.md:26–33`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md).
5. Epic PS still «Next … SSR-16…18 Todo» — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md).
6. Dashboard Notes `:55` / epic `:61` / wave `:92` still Todo — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
7. Pointer stays pkg-000073 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
8. Product AC T01–T06 yes; G16 8 passed; gate PASS 2026-08-30T14:24:58Z.

## Gap / Проблема
Present-tense SSOT contradicts code Done. Operators reading backlog/epic/dashboard still see SSR-16 as Todo / AppConfig without node fields.

## Acceptance / DoD
- [x] Backlog SSR-16 §Verified: As-of-Done (fields `:63–64`; lifespan `:121–128`) vs Historical (pre-P3 «без node schema полей» / lifespan не pack id)
- [x] Epic PS: **As-of-Done (SSR-16 pkg-000073)**; remaining Todo = SSR-17…18 (not «16…18 Todo»)
- [x] Dashboard Notes `:55` / epic rollup `:61` / wave `:92` — SSR-16 Done; 17+18 Todo
- [x] No `src/` / intake 4xx / ClusterLens / `GET /schema-active` edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000073
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-16-t07.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Problem Statement)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (Notes `:55` / epic `:61` / wave `:92`)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; intake 4xx (SSR-17); `ClusterLens`; `GET /schema-active`
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000073
- `gateway-mvp-dashboard.md`; pie T-wave
- Start SSR-17/06/07/12; reopen 01–05/08–15 product
- T-wave G3 / `audit-gw-ssr-0*` rewrite
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / IDX/QRY.
  - Не реализовывать SSR-06/07/12/17.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'без node schema полей|SSR-16…18 Todo|Node env \+ boot — \*\*Todo\*\*' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md
rg -n 'As-of-Done \(SSR-16|node_schema_id' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-16-node-active-schema-config.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
