# task-gw-ssr-24-t08-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for T01–T06 Code Facts

## Meta
- **Story:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000081 (parent product AC Done); wave `run_mode=gw_ssr_24_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-24
- **Depends on:** T01–T07 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-24-geo-detail-persist-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-24-geo-detail-persist-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T21:09:04Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-24_gap_20260830T210820Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T21:10:10Z

## Purpose
Закрыть G1 (MEDIUM): T01–T06 Code Facts still present-tense «нет street» / `geo_admin_*` only / «No `test_gw_ssr_24_*`» vs live persist (`contracts.py:41–45`). Docs only. Backlog+pipeline §Verified already As-of-Done — **не reopen**. No runtime. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-24-geo-detail-persist-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-24-geo-detail-persist-2026-08-30.md) §3 / §5.
2. Live persist: `StoryGeoSnapshot` street/house/house_range/houses/address_line — [`contracts.py:41–45`](../../../../../../../src/core/domain/contracts.py).
3. **As-of-Done:** T01–T06 Code Facts split As-of-Done vs Historical — t01 `:18–22`; t02 `:18–21`; t03 `:18–24`; t04 `:18–21`; t05 `:18–22`; t06 `:18–22`.
4. Backlog §Verified already As-of-Done — [`STORY-GW-SSR-24-geo-detail-persist.md:28`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md).
5. Pointer stays pkg-000081 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
6. Product AC T01–T07 yes; G24 gate PASS 2026-08-30T21:00:56Z; T08 G1 CLOSED 2026-08-30T21:10:10Z.

## Gap / Проблема
G1 CLOSED: present-tense «нет street» / «No `test_gw_ssr_24_*`» only in Historical rows.

## Acceptance / DoD
- [x] T01–T06 Code Facts: As-of-Done (live persist depth / tests file) vs Historical (pre-P3 «нет street» / no `test_gw_ssr_24_*`)
- [x] Backlog+pipeline §Verified **не** reopen (already split)
- [x] No `src/` / ClusterLens / `GET /schema-active` / IDX / `story_dimensions` / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 `:271` **не** переписан
- [x] `current.yaml` stays pkg-000081
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-24-t08.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- T01–T06 README Code Facts (same story folder)
- This folder: `acceptance-verification-gw-ssr-24-t08.md` (P6 only)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; IDX / `story_dimensions`; GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000081
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–23 product; start SSR-25
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12 / SSR-25.
  - Не переписывать T-wave G3.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'нет street|No `test_gw_ssr_24' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-24-geo-detail-persist/task-gw-ssr-24-t0{1,2,3,4,5,6}-*/README.md
rg -n 'As-of-Done \(SSR-24' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-24-geo-detail-persist.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
sed -n '271p' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
