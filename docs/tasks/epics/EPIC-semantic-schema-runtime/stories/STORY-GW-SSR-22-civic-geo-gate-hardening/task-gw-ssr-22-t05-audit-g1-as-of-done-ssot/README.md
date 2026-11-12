# task-gw-ssr-22-t05-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-22 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000079 (parent product AC Done); wave `run_mode=gw_ssr_22_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-22
- **Depends on:** T00–T04 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T20:20:45Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-22_gap_20260830T201957Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T20:24:12Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «`geo_service is None` → skip check» vs intake 4xx. T00/T01 Code Facts still cite skip. Docs only. No runtime. No T-wave G3 rewrite. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-22-civic-geo-gate-hardening-2026-08-30.md) §3 / §5.
2. Product: scope + no service → `IntakeValidationError("geo unavailable")` — [`handlers.py:258–260`](../../../../../../../src/core/api/handlers.py).
3. Stale backlog §Verified — [`STORY-GW-SSR-22-civic-geo-gate-hardening.md:29`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md).
4. Stale pipeline §Verified — [`STORY-GW-SSR-22-civic-geo-gate-hardening.md:57`](../STORY-GW-SSR-22-civic-geo-gate-hardening.md).
5. T00 Code Facts still «if geo_service is not None» — [`task-gw-ssr-22-t00…/README.md:19`](../task-gw-ssr-22-t00-fail-mode-decision/README.md).
6. T01 Code Facts still «Silent skip when service None» — [`task-gw-ssr-22-t01…/README.md:20`](../task-gw-ssr-22-t01-handlers-no-silent-skip/README.md).
7. Pointer stays pkg-000079 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
8. Product AC T00–T04 yes; G22 gate PASS 2026-08-30T20:07:21Z.

## Gap / Проблема
Present-tense story §Verified contradicts handlers after P3. Operators still see «skip check».

## Acceptance / DoD
- [x] Backlog SSR-22 §Verified: As-of-Done (scope+no service → intake 4xx / geo unavailable) vs Historical («skip check»)
- [x] Pipeline §Verified synced (same split)
- [x] T00/T01 Code Facts updated to raise, not skip
- [x] No `src/` / ClusterLens / `GET /schema-active` / `geo_detail` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 `:271` **не** переписан
- [x] `current.yaml` stays pkg-000079
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-22-t05.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-22-civic-geo-gate-hardening/STORY-GW-SSR-22-civic-geo-gate-hardening.md` (§Verified)
- T00/T01 README Code Facts (same story folder)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; `geo_detail` (→23); GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000079
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–21 product; start 23…25
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12 / SSR-23.
  - Не переписывать T-wave G3.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'skip check' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-22-civic-geo-gate-hardening/STORY-GW-SSR-22-civic-geo-gate-hardening.md
rg -n 'As-of-Done \(SSR-22' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-22-civic-geo-gate-hardening.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
sed -n '271p' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
