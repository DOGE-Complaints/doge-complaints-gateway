# task-gw-ssr-30-t06-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical for T03 + backlog (G1)

## Meta
- **Story:** [STORY-GW-SSR-30](../STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000087 (parent product AC Done); wave `run_mode=gw_ssr_30_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-SSR-30
- **Depends on:** T00–T05 Done (product AC / G30 PASS)
- **Audit ref:** [`audit-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness-2026-09-02.md`](../../../../../../analysis/audit-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness-2026-09-02.md) **G1**
- **Scaffolded:** 2026-09-02T14:05:46Z
- **Completed:** 2026-09-02T14:05:46Z
- **Gate Date:** 2026-09-02T14:05:46Z
- **Decision Ref:** P5 `.cursor/plans/p5_ssr-30_gap_20260902T140504Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): T03 Code Facts / Gap still present-tense pre-P3; backlog §Verified «Нет card_fields»; Pitfalls absent-test stale. Docs-only As-of-Done vs Historical. No rewrite §«Актуальная точка» (G2 WAIVED). Do not reopen pack/projection unless drift.

## Code Facts
1. Audit G1 — [`audit-gw-ssr-30-….md`](../../../../../../analysis/audit-gw-ssr-30-tallinn-card-fields-spa-overlay-readiness-2026-09-02.md) §3 / §5.
2. Live INDEX — row 30 Done (Awaiting Commits) pkg-000087; Progress SSR-30 Done.
3. Live spa-16 — Tallinn Declare note for MVP `card_fields`.
4. Live tallinn `pack.json` — MVP `card_fields` three paths.
5. Live test — `test_tallinn_civic_mvp_card_fields_present` (+ `test_gw_ssr_30_*`).
6. **As-of-Done (P6):** T03 Code Facts + backlog §Verified/Pitfalls split As-of-Done vs Historical — G1 CLOSED 2026-09-02T14:05:46Z.
7. Pointer stays pkg-000087.
8. Product AC T00–T05 yes; G30 PASS 2026-09-02T14:00:46Z.

## Gap / Проблема
G1 CLOSED: present-tense pre-P3 claims only in Historical rows.

## Acceptance / DoD
- [x] T03 Code Facts: As-of-Done (live) vs Historical (pre-P3); Gap closed/historical
- [x] Backlog §Verified + Pitfalls: As-of-Done vs Historical
- [x] T00–T02 / T04–T05 **не** reopen for product
- [x] No `src/` / invent / pack.json / GPT UI edits
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] `current.yaml` stays pkg-000087
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-ssr-30-t06.md` signed (Date post P6)

## Where to change
- T03 README Code Facts / Gap
- Backlog `$storyFile` §Verified current state + Pitfalls
- This folder: `acceptance-verification-gw-ssr-30-t06.md` (P6)

## Out of scope
- G2 bullrun §«Актуальная точка» (WAIVED)
- Product pack / projection reopen unless drift
- New pkg; invent SSR-06/07/12; SPA FE

## Verification commands
```bash
rg -n "As-of-Done|Historical" \
  doge-complaints-gateway/docs/tasks/epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness/task-gw-ssr-30-t03-index-spa-docs-note/README.md \
  doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
