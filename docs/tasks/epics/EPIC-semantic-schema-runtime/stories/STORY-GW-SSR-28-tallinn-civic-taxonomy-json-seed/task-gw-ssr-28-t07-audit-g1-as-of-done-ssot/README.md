# task-gw-ssr-28-t07-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for T02–T04 Code Facts

## Meta
- **Story:** [STORY-GW-SSR-28](../STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000085 (parent product AC Done); wave `run_mode=gw_ssr_28_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-28
- **Depends on:** T01–T06 Done (product AC / G28 PASS)
- **Audit ref:** [`audit-gw-ssr-28-tallinn-civic-taxonomy-json-seed-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-28-tallinn-civic-taxonomy-json-seed-2026-09-01.md) **G1**
- **Scaffolded:** 2026-09-01T13:40:23Z
- **Completed:** 2026-09-01T13:41:25Z
- **Gate Date:** 2026-09-01T13:41:25Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-28_gap_20260901T133933Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T02/T03/T04 Code Facts still present-tense pre-P3 vs live tallinn taxonomy seed. Docs only — As-of-Done vs Historical. No re-seed. No rewrite §«Актуальная точка» (G2 WAIVED). Pipeline/backlog Verified already As-of-Done (not in scope unless drift found).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-28-tallinn-civic-taxonomy-json-seed-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-28-tallinn-civic-taxonomy-json-seed-2026-09-01.md) §3 / §5.
2. Live seed — [`taxonomy.json`](../../../../../../../schema-packs/tallinn_civic/v1/taxonomy.json) 13 axes / 182 keys.
3. Live manifest — [`pack.json`](../../../../../../../schema-packs/tallinn_civic/v1/pack.json) `"taxonomy_schema": "taxonomy.json"`.
4. Live tests — [`tests/test_gw_ssr_28_taxonomy_seed.py`](../../../../../../../tests/test_gw_ssr_28_taxonomy_seed.py) (7) + helper [`ssr28_gpt_taxonomy_extract.py`](../../../../../../../tests/helpers/ssr28_gpt_taxonomy_extract.py).
5. **As-of-Done (P6):** T02–T04 Code Facts split As-of-Done vs Historical — G1 CLOSED 2026-09-01T13:41:25Z.
6. Pipeline/backlog Verified already As-of-Done (P3; no drift this P6).
7. Pointer stays pkg-000085 — [`gateway-active-package.current.yaml`](../../../../../gateway-active-package.current.yaml).
8. Product AC T01–T06 yes; G28 gate PASS 2026-09-01T13:35:45Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows; As-of-Done cites live seed/manifest/tests.

## Acceptance / DoD
- [x] T02/T03/T04 Code Facts: As-of-Done (live) vs Historical (pre-P3 present-tense)
- [x] Pipeline/backlog Verified — confirm already As-of-Done (no invent rewrite); fix only if drift
- [x] T01/T05/T06 **не** reopen for product
- [x] No `src/` / ClusterLens / invent vocab / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000085
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-28-t07.md` signed (Date post P6 live verify + `--print-utc-now`)

## Where to change
- T02–T04 README Code Facts (same story folder)
- This folder: `acceptance-verification-gw-ssr-28-t07.md` (P6 only)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED reason=operator)
- Runtime / invent taxonomy keys; legal/mobility seeds; GPT UI materialize
- Invent `EPIC-M2-*`; new pkg; `gateway-active-package.current.yaml` stays pkg-000085
- Start SSR-29 product; reopen 01–27 product
- Overlay bans:
  - **No invent** taxonomy vocabulary.
  - **No ClusterLens** add/remove.
  - Не переписывать bullrun §«Актуальная точка».

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed/task-gw-ssr-28-t0{2,3,4}-*/README.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
