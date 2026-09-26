# task-gw-req9-02-t04-audit-g1-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G1)

## Meta
- **Story:** [STORY-GW-REQ9-02](../STORY-GW-REQ9-02-make-test.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000097 (parent product AC Done); wave `run_mode=gw_req9_02_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ9-02
- **Depends on:** T01–T03 Done (product AC / gate PASS)
- **Audit ref:** [`audit-gw-req9-02-make-test-2026-09-26.md`](../../../../../../analysis/audit-gw-req9-02-make-test-2026-09-26.md) **G1**
- **Scaffolded:** 2026-09-26T12:29:39Z
- **Completed:** 2026-09-26T12:31:20Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req9_02_gap_20260926T122851Z.plan.md` G1 TASKED follow_up=none

## Purpose
Закрыть G1 (LOW): backlog §Verified still present-tense «no `test`» while product shipped. Docs-only As-of-Done vs Historical. Optional «Техническое решение (projected)» → as-shipped. Pipeline §Verified already split — confirm only. No rewrite §«Актуальная точка» (G2 WAIVED). 4 offline fails stay WAIVED out-of-DoD (no product fix).

## Code Facts
1. Audit G1 — backlog §Verified claimed `.PHONY` without `test` (pre-P3 present-tense).
2. Live product — `Makefile:1` PHONY includes `test`+`test-live`; `:50–54` marker targets; gate PASS 2026-09-26T12:22:28Z.
3. **As-of-Done (P6 2026-09-26T12:31:20Z):** G1 CLOSED — backlog §Verified split As-of-Done vs Historical; «Техническое решение» as-shipped; pipeline §Verified already aligned.
4. Pointer stays pkg-000097; product Story Done (AC-01…03).

## Gap
**G1 CLOSED:** present-tense pre-P3 only in Historical rows.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (live PHONY `test`+`test-live`; targets `Makefile:50–54`; Historical: pre-P3 no `test`)
- [x] Optional: backlog «Техническое решение (projected)» → as-shipped note
- [x] Pipeline §Verified: confirm As-of-Done/Historical — no present-tense drift
- [x] T01–T03 product gate **не** reopen
- [x] Makefile / invent CI **не** reopen
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] 4 offline fails **не** become product tasks (WAIVED out-of-DoD)
- [x] `current.yaml` stays pkg-000097
- [x] BULLRUN phases complete
- [x] `acceptance-verification-gw-req9-02-t04.md` signed

## Where to change
- Backlog `STORY-GW-REQ9-02-make-test.md` §Verified (+ projected → as-shipped)
- Pipeline Nested T04 status
- Bullrun T04 row + P6 registry

## Out of scope
Product/Makefile reopen; invent CI; claim Railway from offline test; fix 4 SSR/bootstrap fails; §Актуальная точка rewrite (G2 WAIVED).
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `semantic-schema-runtime`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000097 / current.yaml.

## Verification commands
```bash
rg -n 'As-of-Done|Historical|no `test`|test-live|PHONY' doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-02-make-test.md
rg -n 'As-of-Done|Historical' doge-complaints-gateway/docs/tasks/epics/EPIC-req9-ops-parity-env-naming/stories/STORY-GW-REQ9-02-make-test/STORY-GW-REQ9-02-make-test.md
head -1 doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml
```
