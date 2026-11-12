# task-gw-ssr-23-t06-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for SSR-23 persistent SSOT

## Meta
- **Story:** [STORY-GW-SSR-23](../STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000080 (parent product AC Done); wave `run_mode=gw_ssr_23_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-23
- **Depends on:** T00–T05 Done (product AC)
- **Audit ref:** [`audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md) **G1**
- **Scaffolded:** 2026-08-30T20:47:34Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-23_gap_20260830T204550Z.plan.md` G1 TASKED follow_up=none
- **Gate Date:** 2026-08-30T20:49:54Z

## Purpose
Закрыть G1 (MEDIUM): backlog + pipeline §Verified still present-tense «`location_query` only» / «`geo.district` only»; T00–T03 Code Facts still cite absent `geo_intake` / no `geo_detail`. Docs only. No runtime. No T-wave G3 rewrite. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md) §3 / §5.
2. Product: root `geo_detail` parse — [`contracts.py:650–654`](../../../../../../../src/core/intake/contracts.py); three packs `geo_intake`.
3. **As-of-Done:** backlog §Verified split (`geo_detail` + `geo_intake` vs Historical) — [`STORY-GW-SSR-23-geo-detail-intake-contract.md:28–33`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md).
4. **As-of-Done:** pipeline §Verified same split — [`STORY-GW-SSR-23-geo-detail-intake-contract.md:58–64`](../STORY-GW-SSR-23-geo-detail-intake-contract.md).
5. **As-of-Done:** T00 Code Facts README `geo_detail` + `geo_intake` — [`task-gw-ssr-23-t00…/README.md:19–22`](../task-gw-ssr-23-t00-contract-readme/README.md).
6. **As-of-Done:** T01 Code Facts `geo_detail` on stash/intake — [`task-gw-ssr-23-t01…/README.md:19–21`](../task-gw-ssr-23-t01-parse-sidecar/README.md).
7. **As-of-Done:** T02 Code Facts `geo_intake` on three packs — [`task-gw-ssr-23-t02…/README.md:19–22`](../task-gw-ssr-23-t02-pack-geo-intake/README.md).
8. **As-of-Done:** T03 Code Facts merge overlay — [`task-gw-ssr-23-t03…/README.md:19–22`](../task-gw-ssr-23-t03-merge-location/README.md).
9. Pointer stays pkg-000080 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
10. Product AC T00–T05 yes; G23 gate PASS 2026-08-30T20:40:50Z; T06 G1 CLOSED 2026-08-30T20:49:54Z.

## Gap / Проблема
G1 CLOSED: present-tense «location_query only» / «geo.district only» only in Historical rows.

## Acceptance / DoD
- [x] Backlog SSR-23 §Verified: As-of-Done (`geo_detail` + pack `geo_intake`) vs Historical («location_query only» / «geo.district only»)
- [x] Pipeline §Verified synced (same split)
- [x] T00–T03 Code Facts updated to live wire (not pre-P3 absent)
- [x] No `src/` / ClusterLens / `GET /schema-active` / SQL street-houses (→24) / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 `:271` **не** переписан
- [x] `current.yaml` stays pkg-000080
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-23-t06.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md` (§Verified)
- `doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-23-geo-detail-intake-contract/STORY-GW-SSR-23-geo-detail-intake-contract.md` (§Verified)
- T00–T03 README Code Facts (same story folder)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; `GET /schema-active`; SQL street/houses (→24); GPT UI
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000080
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–22 product; start 24…25
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-06/07/12 / SSR-24.
  - Не переписывать T-wave G3.
  - Не переписывать `bullrun-launch-index.md` §«Актуальная точка».
  - Не править `gateway-mvp-dashboard.md`. Pie T-wave **не** трогать.

## Verification commands
```bash
rg -n 'location_query only|geo.district only' \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-23-geo-detail-intake-contract/STORY-GW-SSR-23-geo-detail-intake-contract.md
rg -n 'As-of-Done \(SSR-23' \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md
sed -n '17,20p' doge-complaints-gateway/docs/tasks/bullrun-launch-index.md
sed -n '271p' doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```
