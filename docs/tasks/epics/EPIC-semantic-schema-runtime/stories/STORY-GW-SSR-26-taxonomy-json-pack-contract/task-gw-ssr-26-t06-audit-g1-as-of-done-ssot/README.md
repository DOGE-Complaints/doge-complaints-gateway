# task-gw-ssr-26-t06-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for T00/T01/T02/T04 + Verified SSOT

## Meta
- **Story:** [STORY-GW-SSR-26](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000083 (parent product AC Done); wave `run_mode=gw_ssr_26_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-26
- **Depends on:** T00–T05 Done (product AC / G26 PASS)
- **Audit ref:** [`audit-gw-ssr-26-taxonomy-json-pack-contract-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-26-taxonomy-json-pack-contract-2026-09-01.md) **G1**
- **Scaffolded:** 2026-09-01T13:05:30Z
- **Completed:** 2026-09-01T13:07:15Z
- **Gate Date:** 2026-09-01T13:07:15Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-26_gap_20260901T130438Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T00/T01/T02/T04 Code Facts + pipeline/backlog §Verified still present-tense pre-P3 vs live taxonomy README/types/loader/tests. Docs only — As-of-Done vs Historical. No runtime. No rewrite §«Актуальная точка» (G2 WAIVED).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-26-taxonomy-json-pack-contract-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-26-taxonomy-json-pack-contract-2026-09-01.md) §3 / §5.
2. Live README key — [`schema-packs/README.md:11,33,35–46`](../../../../../../../schema-packs/README.md).
3. Live types — [`contracts.py:89–122`](../../../../../../../src/core/schema/contracts.py) `TaxonomyPack` / `SchemaContext.taxonomy`.
4. Live loader — [`resolver.py`](../../../../../../../src/core/schema/resolver.py) `_parse_taxonomy_pack` + `load_pack` wire.
5. Live tests — [`tests/test_gw_ssr_26_taxonomy_loader.py`](../../../../../../../tests/test_gw_ssr_26_taxonomy_loader.py) (6 tests).
6. **As-of-Done (P6):** T00/T01/T02/T04 Code Facts + pipeline/backlog §Verified split As-of-Done vs Historical — G1 CLOSED 2026-09-01T13:07:15Z.
7. T03 — no G1 claim; **не reopen**.
8. Pointer stays pkg-000083 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
9. Product AC T00–T05 yes; G26 gate PASS 2026-09-01T13:00:37Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows; As-of-Done cites live README/types/loader/tests.

## Acceptance / DoD
- [x] T00/T01/T02/T04 Code Facts: As-of-Done (live) vs Historical (pre-P3 present-tense)
- [x] Pipeline §Verified + backlog §Verified as-built: As-of-Done vs Historical (same pattern)
- [x] T03 **не** reopen
- [x] No `src/` / ClusterLens / wire taxonomy / tallinn seed / `GET /schema-active` edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] T-wave G3 **не** переписан
- [x] `current.yaml` stays pkg-000083
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-26-t06.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- T00/T01/T02/T04 README Code Facts (same story folder)
- Pipeline [`STORY-GW-SSR-26-taxonomy-json-pack-contract.md`](../STORY-GW-SSR-26-taxonomy-json-pack-contract.md) §Verified
- Backlog [`STORY-GW-SSR-26-taxonomy-json-pack-contract.md`](../../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md) §Verified as-built
- This folder: `acceptance-verification-gw-ssr-26-t06.md` (P6 only)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / `src/**`; `ClusterLens`; wire `parse_taxonomy_payload`; tallinn seed (SSR-28)
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000083
- `gateway-mvp-dashboard.md`; pie T-wave; T-wave G3 rewrite
- Invent SSR-06/07/12; reopen 01–25 product; start SSR-27/28/29
- Overlay bans:
  - Не добавлять член в `ClusterLens`.
  - Не invent HTTP filter / `GET /schema-active`.
  - Не реализовывать SSR-27/28/29 / 06/07/12.

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-26-taxonomy-json-pack-contract/task-gw-ssr-26-t0{0,1,2,4}-*/README.md
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-26-taxonomy-json-pack-contract/STORY-GW-SSR-26-taxonomy-json-pack-contract.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-26-taxonomy-json-pack-contract.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
