# task-gw-ssr-32-t05-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for backlog §Verified (+ T01–T03 labels) (G1)

## Meta
- **Story:** [STORY-GW-SSR-32](../STORY-GW-SSR-32-node-specific-contour1-wire-axes.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000089 (parent product AC Done); wave `run_mode=gw_ssr_32_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-32
- **Depends on:** T01–T04 Done (product AC / G32 PASS)
- **Audit ref:** [`audit-gw-ssr-32-node-specific-contour1-wire-axes-2026-09-04.md`](../../../../../../analysis/audit-gw-ssr-32-node-specific-contour1-wire-axes-2026-09-04.md) **G1**
- **Scaffolded:** 2026-09-04T13:17:57Z
- **Completed:** 2026-09-04T13:17:57Z
- **Gate Date:** 2026-09-04T13:17:57Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-32_gap_20260904T131757Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified as-built still present-tense Contour1 membership reject. Docs-only As-of-Done vs Historical. Optionally label T01–T03 Code Facts As-of-Done vs Historical for единообразие. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen `axes.py` unless drift.

## Code Facts
1. Audit G1 — backlog §Verified stale membership claim.
2. Live `axes.py` — strip/lower only; `rg Unsupported taxonomy axis` empty.
3. **As-of-Done (P6):** backlog §Verified + Claims split; T01–T03 labeled — G1 CLOSED 2026-09-04T13:17:57Z.
4. Pointer stays pkg-000089; G32 PASS 2026-09-04T13:13:31Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 membership only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Claims if needed): As-of-Done vs Historical
- [x] T01–T03 Code Facts optionally labeled As-of-Done vs Historical
- [x] T04 product gate **не** reopen
- [x] No `src/` / invent / axes reopen / docs SSR-33
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000089
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-32-t05.md` signed

## Where to change
- Backlog `$storyFile` §Verified (+ Claims)
- T01–T03 README Code Facts (labels)
- This folder: `acceptance-verification-gw-ssr-32-t05.md` (P6)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- Product axes reopen unless drift
- Contour2 / ClusterLens / vocabulary

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-32-node-specific-contour1-wire-axes.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-32-node-specific-contour1-wire-axes/task-gw-ssr-32-t0{1,2,3}-*/README.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
