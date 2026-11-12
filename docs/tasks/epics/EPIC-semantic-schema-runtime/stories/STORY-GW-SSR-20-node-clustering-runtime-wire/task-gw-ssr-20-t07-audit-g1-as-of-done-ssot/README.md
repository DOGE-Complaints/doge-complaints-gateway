# task-gw-ssr-20-t07-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-20 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-20](../STORY-GW-SSR-20-node-clustering-runtime-wire.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000077 (parent product AC Done); wave `run_mode=gw_ssr_20_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-20
- **Depends on:** T01–T06 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-20-node-clustering-runtime-wire-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-20-node-clustering-runtime-wire-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T19:44:28Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-20_gap_20260830T194428Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T19:45:21Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «Engine из config» / `cluster_geo_scope` vs civic pack wire. Confirm epic/dashboard As-of-Done SSR-20. Docs only. No runtime. No ClusterLens. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-20-node-clustering-runtime-wire-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-20-node-clustering-runtime-wire-2026-08-30.md) §3 / §5.
2. Factory civic from pack — [`service_factory.py:95–121`](../../../../../../../src/core/infrastructure/service_factory.py).
3. Handlers geo from pack — [`handlers.py:254–257`](../../../../../../../src/core/api/handlers.py).
4. AppConfig without semantic cluster_* — [`schema.py:37–56`](../../../../../../../src/core/config/schema.py).
5. Stale backlog §Verified — [`STORY-GW-SSR-20-node-clustering-runtime-wire.md:24–34`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md).
6. Stale pipeline §Verified — [`STORY-GW-SSR-20-node-clustering-runtime-wire.md:52–62`](../STORY-GW-SSR-20-node-clustering-runtime-wire.md).
7. Dashboard Status already Done — [`gateway-semantic-schema-runtime-dashboard.md`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
8. Pointer stays pkg-000077 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
9. Product AC T01–T06 yes; G20 spot 21 passed; gate PASS 2026-08-30T19:40:38Z.

## Gap / Проблема
Present-tense story §Verified contradicts factory/handlers Done. Operators reading backlog/pipeline still see «Engine из config».

## Acceptance / DoD
- [x] Backlog SSR-20 §Verified: As-of-Done (engine/gate/min/geo from pack civic; semantic CLUSTER_* gone; cron stay) vs Historical («из config» / `cluster_geo_scope`)
- [x] Pipeline §Verified synced (same split)
- [x] Epic/dashboard As-of-Done SSR-20 confirmed (Status Done; cluster-knobs 19–20 closed, 21 Todo)
- [x] No `src/` / ClusterLens / `GET /schema-active` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000077
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-20-t07.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-20-node-clustering-runtime-wire/STORY-GW-SSR-20-node-clustering-runtime-wire.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (confirm As-of-Done)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (confirm As-of-Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000077
- `gateway-mvp-dashboard.md`; pie T-wave
- Invent SSR-06/07/12; reopen 01–19 product; start 21
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'Engine из config|cluster_geo_scope' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-20-node-clustering-runtime-wire/STORY-GW-SSR-20-node-clustering-runtime-wire.md
rg -n 'As-of-Done \(SSR-20' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-20-node-clustering-runtime-wire.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
