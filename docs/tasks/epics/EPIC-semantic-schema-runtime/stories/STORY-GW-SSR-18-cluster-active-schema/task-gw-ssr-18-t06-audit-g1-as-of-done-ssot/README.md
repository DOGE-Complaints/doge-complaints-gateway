# task-gw-ssr-18-t06-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-18 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000075 (parent product AC Done); wave `run_mode=gw_ssr_18_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-18
- **Depends on:** T01–T05 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-18-cluster-active-schema-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-18-cluster-active-schema-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T15:11:22Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-18_gap_20260830T151122Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T15:12:33Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «Bound → pack **этой** story» vs code skip-unless-active. Confirm epic/dashboard As-of-Done SSR-18. Docs only. No runtime. No ClusterLens. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-18-cluster-active-schema-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-18-cluster-active-schema-2026-08-30.md) §3 / §5.
2. Bound mismatch → skip, not pack этой story — [`cluster_orchestrator.py:303–307`](../../../../../../../src/core/application/cluster_orchestrator.py).
3. Dual from **active** pack.json — [`:113–124`](../../../../../../../src/core/application/cluster_orchestrator.py); [`pack_engine.py:71–79`](../../../../../../../src/core/schema/pack_engine.py).
4. Civic unbound-only — [`:89–91`](../../../../../../../src/core/application/cluster_orchestrator.py).
5. Stale backlog §Verified — [`STORY-GW-SSR-18-cluster-active-schema.md:26–32`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md).
6. Stale pipeline §Verified — [`STORY-GW-SSR-18-cluster-active-schema.md:53–61`](../STORY-GW-SSR-18-cluster-active-schema.md).
7. Epic PS already As-of-Done SSR-18 — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md).
8. Dashboard Status already Done — [`gateway-semantic-schema-runtime-dashboard.md:7,49`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
9. Pointer stays pkg-000075 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
10. Product AC T01–T05 yes; G18 spot 21 passed; gate PASS 2026-08-30T15:06:33Z.

## Gap / Проблема
Present-tense story §Verified contradicts code Done. Operators reading backlog/pipeline still see «pack этой story» (`:274–275`).

## Acceptance / DoD
- [x] Backlog SSR-18 §Verified: As-of-Done (pack/dual iff persist == `NODE_SCHEMA_*`; mismatch skip+log; unbound civic) vs Historical («pack этой story» `:274–275`)
- [x] Pipeline §Verified synced (same split)
- [x] Epic/dashboard As-of-Done SSR-18 confirmed (Status Done; node-schema 16–18 closed)
- [x] No `src/` / ClusterLens / `GET /schema-active` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000075
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-18-t06.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-18-cluster-active-schema/STORY-GW-SSR-18-cluster-active-schema.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (confirm As-of-Done)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (confirm As-of-Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000075
- `gateway-mvp-dashboard.md`; pie T-wave
- Invent SSR-06/07/12; reopen 01–17 product
- T-wave G3 / `audit-gw-ssr-0*` rewrite
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'Bound → pack \*\*этой\*\* story|cluster_orchestrator.py:274' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-18-cluster-active-schema/STORY-GW-SSR-18-cluster-active-schema.md
rg -n 'As-of-Done \(SSR-18' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
