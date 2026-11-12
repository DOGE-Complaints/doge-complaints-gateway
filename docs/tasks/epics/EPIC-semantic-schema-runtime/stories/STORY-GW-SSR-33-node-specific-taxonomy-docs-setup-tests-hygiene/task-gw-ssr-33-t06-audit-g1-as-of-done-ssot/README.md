# task-gw-ssr-33-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for T01–T04 + backlog §Verified (G1)

## Meta
- **Story:** [STORY-GW-SSR-33](../STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000090 (parent product AC Done); wave `run_mode=gw_ssr_33_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-SSR-33
- **Depends on:** T01–T05 Done (product AC / G33 PASS)
- **Audit ref:** [`audit-gw-ssr-33-node-specific-taxonomy-docs-setup-tests-hygiene-2026-09-04.md`](../../../../../../analysis/audit-gw-ssr-33-node-specific-taxonomy-docs-setup-tests-hygiene-2026-09-04.md) **G1**
- **Scaffolded:** 2026-09-04T13:34:49Z
- **Completed:** 2026-09-04T13:34:49Z
- **Gate Date:** 2026-09-04T13:34:49Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-33_gap_20260904T133449Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01–T04 Code Facts/Gaps и backlog §Verified всё ещё scaffold present-tense. Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen product README/manual unless drift.

## Code Facts
1. Audit G1 — persistent SSOT present-tense on T01–T04 + backlog §Verified.
2. Live product docs — README node-defined; manual D-SSR-11; INDEX inventory; uus handoff obsolete.
3. **As-of-Done (P6):** T01–T04 + backlog §Verified split — G1 CLOSED 2026-09-04T13:34:49Z.
4. Pointer stays pkg-000090; G33 PASS 2026-09-04T13:28:42Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Claims if needed): As-of-Done vs Historical
- [x] T01–T04 Code Facts/Gaps labeled As-of-Done vs Historical
- [x] T05 product gate **не** reopen
- [x] No `src/` / invent / resolver / normalize_axis reopen
- [x] Product README/manual not reopened unless drift
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000090
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-33-t06.md` signed

## Where to change
- Backlog `$storyFile` §Verified (+ Claims)
- T01–T04 README Code Facts / Gap
- This folder: `acceptance-verification-gw-ssr-33-t06.md` (P6)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- Product manuals/README reopen unless drift
- resolver / axes / ClusterLens / uus pack.json / GPT edit

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene/task-gw-ssr-33-t0{1,2,3,4}-*/README.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
