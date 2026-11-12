# task-gw-ssr-31-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for T01–T03 + backlog (G1)

## Meta
- **Story:** [STORY-GW-SSR-31](../STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000088 (parent product AC Done); wave `run_mode=gw_ssr_31_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-31
- **Depends on:** T01–T05 Done (product AC / G31 PASS)
- **Audit ref:** [`audit-gw-ssr-31-node-specific-contour2-taxonomy-axes-2026-09-04.md`](../../../../../../analysis/audit-gw-ssr-31-node-specific-contour2-taxonomy-axes-2026-09-04.md) **G1**
- **Scaffolded:** 2026-09-04T13:02:12Z
- **Completed:** 2026-09-04T13:02:12Z
- **Gate Date:** 2026-09-04T13:02:12Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-31_gap_20260904T125959Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T01–T03 Code Facts/Gaps still present-tense pre-P3 Contour2 lockstep; backlog §Verified as-built + Claims «implementation not started». Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen resolver unless drift. README «must equal 13» → SSR-33 residual (not this task).

## Code Facts
1. Audit G1 — [`audit-gw-ssr-31-….md`](../../../../../../analysis/audit-gw-ssr-31-node-specific-contour2-taxonomy-axes-2026-09-04.md) §3 / §5.
2. Live resolver — Contour2 unlock; `rg TAXONOMY_AXIS_VALUES src/core/schema/resolver.py` empty.
3. Live tests — SSR-26/28/31 suites green (20 passed at G31).
4. **As-of-Done (P6):** T01–T03 Code Facts + backlog §Verified/Claims split As-of-Done vs Historical — G1 CLOSED 2026-09-04T13:02:12Z.
5. Pointer stays pkg-000088.
6. Product AC T01–T05 yes; G31 PASS 2026-09-04T12:55:28Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows.

## Acceptance / DoD
- [x] T01–T03 Code Facts: As-of-Done (live) vs Historical (pre-P3); Gaps closed/historical
- [x] Backlog §Verified + Claims: As-of-Done vs Historical
- [x] T04–T05 **не** reopen for product
- [x] No `src/` / invent / resolver reopen / README SSR-33
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000088
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-31-t06.md` signed (Date post P6)

## Where to change
- T01–T03 README Code Facts / Gap
- Backlog `$storyFile` §Verified as-built + Claims
- This folder: `acceptance-verification-gw-ssr-31-t06.md` (P6)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- schema-packs README L44 (SSR-33)
- Product resolver reopen unless drift
- New pkg; invent Contour1 / ClusterLens

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes/task-gw-ssr-31-t0{1,2,3}-*/README.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
