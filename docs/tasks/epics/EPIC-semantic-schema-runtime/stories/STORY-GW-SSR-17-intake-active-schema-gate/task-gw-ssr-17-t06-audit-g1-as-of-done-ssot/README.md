# task-gw-ssr-17-t06-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-17 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Type:** docs
- **Status:** 🔵 Done
- **Package:** pkg-000074 (parent product AC Done); wave `run_mode=gw_ssr_17_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-17
- **Depends on:** T01–T05 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-17-intake-active-schema-gate-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-17-intake-active-schema-gate-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T14:49:24Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-17_gap_20260830T144924Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T14:51:13Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense civic-optional vs code 4xx. Confirm epic/dashboard As-of-Done SSR-17. Docs only. No runtime. No ClusterLens. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-17-intake-active-schema-gate-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-17-intake-active-schema-gate-2026-08-30.md) §3 / §5.
2. Parse required — [`contracts.py:227–241`](../../../../../../../src/core/intake/contracts.py); absent key [`:480–482`](../../../../../../../src/core/intake/contracts.py).
3. Match + validate active pack — [`services.py:249–271`](../../../../../../../src/core/application/services.py).
4. Stale backlog §Verified — [`STORY-GW-SSR-17-intake-active-schema-gate.md:26–33`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md).
5. Stale pipeline §Verified — [`STORY-GW-SSR-17-intake-active-schema-gate.md:53–60`](../STORY-GW-SSR-17-intake-active-schema-gate.md).
6. Epic PS already As-of-Done SSR-17 — [`EPIC-semantic-schema-runtime.md:16`](../../../../EPIC-semantic-schema-runtime.md).
7. Dashboard Status already Done — [`gateway-semantic-schema-runtime-dashboard.md:7,48`](../../../../../gateway-semantic-schema-runtime-dashboard.md).
8. Pointer stays pkg-000074 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
9. Product AC T01–T05 yes; G17 22 passed; gate PASS 2026-08-30T14:45:34Z.

## Gap / Проблема
Present-tense story §Verified contradicts code Done. Operators reading backlog/pipeline still see civic-optional binding.

## Acceptance / DoD
- [x] Backlog SSR-17 §Verified: As-of-Done (required binding; match `NODE_SCHEMA_*`; validate active pack) vs Historical (civic-optional / `{}`=None)
- [x] Pipeline §Verified synced (same split)
- [x] Epic/dashboard As-of-Done SSR-17 confirmed (Status Done; Next = SSR-18)
- [x] No `src/` / ClusterLens / `GET /schema-active` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000074
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-17-t06.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md` (confirm As-of-Done)
- `doge-complaints-gateway/docs/tasks/gateway-semantic-schema-runtime-dashboard.md` (confirm As-of-Done)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000074
- `gateway-mvp-dashboard.md`; pie T-wave
- Start SSR-18/06/07/12; reopen 01–16 product
- T-wave G3 / `audit-gw-ssr-0*` rewrite
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12/18.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'Binding optional|Validate только если binding is not None|Civic HTTP без binding зелёный' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md
rg -n 'As-of-Done \(SSR-17' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-17-intake-active-schema-gate.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
```
