# task-gw-ssr-14-t03-audit-g1-epic-ssot

## Task: add — epic Meta/Scope/PS + dashboard Notes As-of-Done SSR-14

## Meta
- **Story:** [STORY-GW-SSR-14](../STORY-GW-SSR-14-docs-abstract-node-paradigm.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000071 (parent product Done); wave `run_mode=gw_ssr_14_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-14
- **Depends on:** T01–T02 Done (product AC/DoD, G14)
- **Audit ref:** [`audit-gw-ssr-14-docs-abstract-node-paradigm-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-14-docs-abstract-node-paradigm-2026-08-29.md) **G1**
- **Scaffolded:** 2026-08-29T19:34:22Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-14_gap_20260829T193330Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-29T19:35:28Z

## Purpose
Закрыть G1 (MEDIUM): persistent SSOT drift — epic Meta `:4` / Scope `:32` / Problem Statement `:16` still «SSR-14…15 Todo» + dashboard Notes `:52,58` still next=14 — vs Stories `:93` / DoD `:77` / INDEX Done. As-of-Done SSR-14; remaining Todo = SSR-15. Keep DoD `:77`. Без runtime. Без rewrite §«Актуальная точка» (G2 WAIVED). **G14:** docs inventory `/tallinn/`→`/node/` current contract.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-14-docs-abstract-node-paradigm-2026-08-29.md`](../../../../../../analysis/audit-gw-ssr-14-docs-abstract-node-paradigm-2026-08-29.md) §3 / §5.
2. Product G14 — operational `rg` empty `/tallinn/(issues|network-pulse|emerging-signals)`; T-wave [`orchestrator-t-wave-runbook.md:271`](../../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md) historical.
3. INDEX row 14 Done — [`INDEX.md:88`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) 🔵 Done (Awaiting Commits).
4. INDEX header + Progress already Done-lump — [`INDEX.md:14,110`](../../../../../backlog-stories/semantic-schema-runtime/INDEX.md) «SSR-08 + … + SSR-14 Done»; remaining Todo SSR-15.
5. Epic Stories row SSR-14 Done — [`EPIC-semantic-schema-runtime.md:93`](../../../../EPIC-semantic-schema-runtime.md).
6. Epic DoD already has SSR-14 line — [`EPIC-semantic-schema-runtime.md:77`](../../../../EPIC-semantic-schema-runtime.md) — **keep**.
7. **Epic Meta still Todo-lump** — [`EPIC-semantic-schema-runtime.md:4`](../../../../EPIC-semantic-schema-runtime.md) «SSR-14…15 🟡 Todo».
8. **Epic Scope SSR-14 still Todo** — [`EPIC-semantic-schema-runtime.md:32`](../../../../EPIC-semantic-schema-runtime.md).
9. **Epic PS still «Backlog (SSR-14…15 Todo)»** — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md).
10. Dashboard Remaining row 14 Done — [`gateway-semantic-schema-runtime-dashboard.md:45`](../../../../../gateway-semantic-schema-runtime-dashboard.md) + wave `:86`.
11. **Dashboard Notes still next=14** — [`:52`](../../../../../gateway-semantic-schema-runtime-dashboard.md); epic row [`:58`](../../../../../gateway-semantic-schema-runtime-dashboard.md) «SSR-14…15 Todo».
12. Bullrun §«Актуальная точка» still MVP ES-03/M2-24 — [`bullrun-launch-index.md:17–20`](../../../../../bullrun-launch-index.md) (G2 WAIVED — **do not rewrite**).
13. Pointer stays pkg-000071 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
14. Product Story Done (AC/DoD, G14) = **yes**. Empty OPEN gap-list = **no** until this task + P7 (G2 WAIVED kept).

## Gap / Проблема
Persistent SSOT (не `docs/analysis/**`): epic Meta/Scope/PS + dashboard Notes still present-tense Todo-lump after pkg-000071 G14 Done.

## Acceptance / DoD
- [x] Epic Meta `:4`: SSR-14 🔵 Done; remaining Todo = SSR-15 only
- [x] Epic Scope `:32`: SSR-14 **Done** pkg-000071 T01–T02 gate PASS 2026-08-29T19:30:07Z
- [x] Epic Problem Statement `:16`: As-of-Done SSR-14 (docs inventory `/tallinn/`→`/node/`); remaining Backlog Todo = SSR-15 tests
- [x] Epic DoD `:77` / Stories `:93` / INDEX Done-lump **не** revert
- [x] Dashboard Notes `:52` + epic row `:58`: next product = SSR-15 Todo (not 14→15)
- [x] Status backlog+pipeline stays 🔵 Done; do not reopen product AC T01–T02
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] Нет invented `EPIC-M2-*` rows
- [x] No `src/` / `ClusterLens` / identity edits
- [x] No pytest this wave (docs-only)
- [x] `gateway-mvp-dashboard.md` **не** править; pie T-wave **не** трогать
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-14-t03.md` signed (Date post P6 live `--verify` + `--print-utc-now` only)

## Where to change
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (Meta `:4` / Scope `:32` / PS `:16`; keep DoD `:77` / Stories `:93`)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (Notes `:52` + epic row `:58`; keep Remaining `:45` Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `ClusterLens` / invent HTTP / identity
- `gateway-mvp-dashboard.md`; pie T-wave; `spa-mvp-dashboard.md`
- New pkg; `gateway-active-package.current.yaml` stays pkg-000071
- SSR-06/07/12/15 execute; reopen 01–05/08–13
- T-wave G3 / `audit-gw-ssr-0*` rewrite
- Overlay UI spa-app — **not this story**
- INDEX/runbook §8 + fence hard bans:
  - Не добавлять член в `ClusterLens`.
  - Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` и civic factory.
  - Не invent HTTP filter / IDX/QRY.
  - Не трогать `doge-identity-service` (D-SSR-3).
  - Не реализовывать SSR-06/07/12/15. Не reopen 01–05/08–13.
  - Не переписывать T-wave G3 / `audit-gw-ssr-0*`.
  - `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` stay.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'SSR-14|SSR-15' doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md
rg -n 'SSR-14|SSR-15' doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md
# G2: heading block 17–20 must still be EPIC-M2-24 / ES-03 (do not rewrite)
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
