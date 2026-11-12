# task-gw-ssr-34-t07-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for backlog §Verified (G1)

## Meta
- **Story:** [STORY-GW-SSR-34](../STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000091 (parent product AC Done); wave `run_mode=gw_ssr_34_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-SSR-34
- **Depends on:** T01–T06 Done (product AC / G34 PASS)
- **Audit ref:** [`audit-gw-ssr-34-uus-active-schema-packs-volume-ops-2026-09-07.md`](../../../../../../analysis/audit-gw-ssr-34-uus-active-schema-packs-volume-ops-2026-09-07.md) **G1**
- **Scaffolded:** 2026-09-07T08:38:47Z
- **Completed:** 2026-09-07T08:38:47Z
- **Gate Date:** 2026-09-07T08:38:47Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-34_gap_20260907T083847Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified still present-tense («Volume почти не описан»; gitignore не исключает uus). Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen manuals/gitignore/env unless drift.

## Code Facts
1. Audit G1 — backlog §Verified stale Volume/gitignore claims.
2. Live product — Local/Railway playbooks + warehouse D-SSR-12; `.gitignore:18` uus.
3. **As-of-Done (P6):** backlog §Verified split — G1 CLOSED 2026-09-07T08:38:47Z.
4. Pointer stays pkg-000091; G34 PASS 2026-09-07T08:32:02Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 Volume/gitignore only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified (+ Claims if needed): As-of-Done vs Historical
- [x] T06 product gate **не** reopen
- [x] Product manuals/gitignore/env not reopened (no drift)
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000091
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-34-t07.md` signed

## Where to change
- Backlog `$storyFile` §Verified (+ Claims)
- This folder: `acceptance-verification-gw-ssr-34-t07.md` (P6)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- Product manuals/gitignore/env reopen unless drift
- SCHEMA_ROOT_URL / pack repair / Railway UI

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
