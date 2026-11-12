# task-gw-ssr-29-t07-audit-g1-as-of-done-ssot

## Task: add — As-of-Done vs Historical for T01–T03 Code Facts

## Meta
- **Story:** [STORY-GW-SSR-29](../STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000086 (parent product AC Done); wave `run_mode=gw_ssr_29_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-29
- **Depends on:** T01–T06 Done (product AC / G29 PASS)
- **Audit ref:** [`audit-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam-2026-09-01.md`](../../../../../../analysis/audit-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam-2026-09-01.md) **G1**
- **Scaffolded:** 2026-09-01T13:51:52Z
- **Completed:** 2026-09-01T13:53:08Z
- **Gate Date:** 2026-09-01T13:53:08Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-29_gap_20260901T135152Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01–T03 Code Facts still present-tense pre-P3 vs live manuals/README/INDEX. Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen product manuals unless drift.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-29-….md`](../../../../../../analysis/audit-gw-ssr-29-taxonomy-docs-operator-copy-paste-seam-2026-09-01.md) §3 / §5.
2. Live manual — [`schema-packs-node-data-model-ru.md`](../../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) 3-file + dual contour + copy-paste.
3. Live README — [`schema-packs/README.md`](../../../../../../../schema-packs/README.md) links manual SSR-29.
4. Live INDEX — taxonomy-pack 26/28/29 Done; Progress **3/3**.
5. **As-of-Done (P6):** T01–T03 Code Facts split As-of-Done vs Historical — G1 CLOSED 2026-09-01T13:53:08Z.
6. Pointer stays pkg-000086.
7. Product AC T01–T06 yes; G29 PASS 2026-09-01T13:49:03Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows.

## Acceptance / DoD
- [x] T01/T02/T03 Code Facts: As-of-Done (live) vs Historical (pre-P3)
- [x] T04–T06 **не** reopen for product
- [x] No `src/` / invent / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000086
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-29-t07.md` signed (Date post P6)

## Where to change
- T01–T03 README Code Facts
- This folder: `acceptance-verification-gw-ssr-29-t07.md` (P6 only)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- Product manual rewrite unless drift
- New pkg; invent SSR-06/07/12

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam/task-gw-ssr-29-t0{1,2,3}-*/README.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
