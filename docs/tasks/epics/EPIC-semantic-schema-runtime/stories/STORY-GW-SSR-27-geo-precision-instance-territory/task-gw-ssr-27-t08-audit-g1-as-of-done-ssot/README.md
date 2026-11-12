# task-gw-ssr-27-t08-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for T00–T05 + Verified SSOT

## Meta
- **Story:** [STORY-GW-SSR-27](../STORY-GW-SSR-27-geo-precision-instance-territory.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000084 (parent product AC Done); wave `run_mode=gw_ssr_27_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-27
- **Depends on:** T00–T07 Done (product AC / G27 PASS)
- **Audit ref:** [`audit-gw-ssr-27-geo-precision-instance-territory-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-27-geo-precision-instance-territory-2026-09-01.md) **G1**
- **Scaffolded:** 2026-09-01T13:25:12Z
- **Completed:** 2026-09-01T13:26:28Z
- **Gate Date:** 2026-09-01T13:26:28Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-27_gap_20260901T132422Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T00/T01/T03/T04 (+T02/T05 scaffold-tense) Code Facts + pipeline/backlog §Verified + backlog AC `[ ]` still present-tense pre-P3 vs live geo precision. Docs only — As-of-Done vs Historical. No runtime. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-27-geo-precision-instance-territory-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-27-geo-precision-instance-territory-2026-09-01.md) §3 / §5.
2. Live README — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) `geo_model` / `gpt_instance_territory` / three-level.
3. Live types — [`contracts.py`](../../../../../../../src/core/schema/contracts.py) `GEO_PRECISION_LEVELS` / `GeoModelBlock` / `GptInstanceTerritory*` / SchemaContext fields.
4. Live loader — [`resolver.py`](../../../../../../../src/core/schema/resolver.py) `_parse_geo_model` / `_parse_gpt_instance_territory`.
5. Live wire/persist — `intake/contracts.py` `detail_level`; `domain/contracts.py` `StoryGeoSnapshot.detail_level`; sqlite/supabase `geo_detail_level`.
6. Live projection — `mapper.py` UC-G03; `ProjectionInput.geo_detail_level`.
7. Live tests — [`tests/test_gw_ssr_27_geo_precision.py`](../../../../../../../tests/test_gw_ssr_27_geo_precision.py) (10 tests).
8. **As-of-Done (P6):** T00–T05 Code Facts + pipeline/backlog §Verified split As-of-Done vs Historical; backlog AC `[x]` — G1 CLOSED 2026-09-01T13:26:28Z.
9. Pointer stays pkg-000084 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
10. Product AC T00–T07 yes; G27 gate PASS 2026-09-01T13:21:04Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows; As-of-Done cites live README/types/loader/wire/projection/tests; backlog AC checked.

## Acceptance / DoD
- [x] T00/T01/T02/T03/T04/T05 Code Facts: As-of-Done (live) vs Historical (pre-P3 present-tense)
- [x] Pipeline §Verified + backlog §Verified as-built: As-of-Done vs Historical
- [x] Backlog §Target / AC checkboxes → `[x]` (product Done)
- [x] T06/T07 **не** reopen for product
- [x] No `src/` / ClusterLens / invent coords / HTTP geo-filter edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 **не** переписан
- [x] `current.yaml` stays pkg-000084
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-27-t08.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- T00–T05 README Code Facts (same story folder)
- Pipeline [`STORY-GW-SSR-27-geo-precision-instance-territory.md`](../STORY-GW-SSR-27-geo-precision-instance-territory.md) §Verified
- Backlog [`STORY-GW-SSR-27-geo-precision-instance-territory.md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md) §Verified + §Target AC
- This folder: `acceptance-verification-gw-ssr-27-t08.md` (P6 only)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; invent coords; HTTP geo-filter
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000084
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–26 product; start SSR-28/29
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-28/29 / 06/07/12.

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-27-geo-precision-instance-territory/task-gw-ssr-27-t0{0,1,2,3,4,5}-*/README.md
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-27-geo-precision-instance-territory/STORY-GW-SSR-27-geo-precision-instance-territory.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-27-geo-precision-instance-territory.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
