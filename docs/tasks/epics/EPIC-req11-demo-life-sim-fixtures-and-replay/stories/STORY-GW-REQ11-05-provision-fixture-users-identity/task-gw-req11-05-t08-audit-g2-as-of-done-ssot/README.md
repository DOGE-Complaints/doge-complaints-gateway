# task-gw-req11-05-t08-audit-g2-as-of-done-ssot

## Task: docs — As-of-Done vs Historical SSOT (G2)

## Meta
- **Story:** [STORY-GW-REQ11-05](../STORY-GW-REQ11-05-provision-fixture-users-identity.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-09-29T18:19:28Z
- **Package:** pkg-000104 (parent product AC Done); wave `run_mode=gw_req11_05_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-05
- **Depends on:** T01–T07 Done (product AC / gate PASS*)
- **Audit ref:** [`audit-gw-req11-05-provision-fixture-users-identity-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-05-provision-fixture-users-identity-2026-09-29.md) **G2**
- **Scaffolded:** 2026-09-29T18:18:26Z
- **Completed:** 2026-09-29T18:19:28Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_05_gap_20260929T181746Z.plan.md` G2 TASKED follow_up=none

## Purpose
Закрыть G2 (LOW): backlog §Verified present-tense pre-P3 «Absent» / pool M=20 while Status=Done. Docs-only As-of-Done vs Historical. G1/G3 WAIVED operator.

## Code Facts
1. Audit G2 — backlog Verified present-tense Absent / pool M=20 (pre-P6).
2. Product Present — `life_sim_provision_users.py` + lib; `.secrets/` gitignored; `--life-sim` secrets-1:1; pool deprecated.
3. Gate PASS* 2026-09-29T18:15:05Z; live signup 429 = G1 WAIVED operator.
4. **As-of-Done (P6 2026-09-29T18:19:28Z):** G2 CLOSED — backlog §Verified + pipeline Code touchpoints split As-of-Done vs Historical.
5. Pointer stays pkg-000104; product Story Done (AC under gate framing + blocker).

## Gap
**G2 CLOSED:** present-tense pre-P3 «Absent» / active pool claim only in Historical rows of backlog Verified.

## Acceptance / DoD
- [x] Backlog §Verified: As-of-Done vs Historical (provision Present; pool deprecated for new Pass)
- [x] Optional: pipeline «Code touchpoints» As-of-Done + Historical «named only»
- [x] T07 product gate **не** reopen
- [x] Product tooling/tests not reopened; no invent OTP HTTP; no invent secrets (G1 WAIVED)
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000104
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-05-t08.md` signed (P6)

## Where to change
- Backlog STORY-GW-REQ11-05 §Verified (done)
- Pipeline Code touchpoints Historical label (done)
- Bullrun T08 row + P6 registry (on close)

## Out of scope
Product/provision execute; invent OTP HTTP; live signup retry as Pass (G1 WAIVED); §Актуальная точка rewrite (G3 WAIVED); mutate pkg-000104.
- Overlay bans:
  - Docs-only As-of-Done.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000104 / current.yaml.
  - Never commit secrets.

## Verification commands
```bash
rg -n 'Absent|pool M=20|As-of-Done|Historical' \
  doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-05-provision-fixture-users-identity.md \
  doge-complaints-gateway/docs/tasks/epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-05-provision-fixture-users-identity/STORY-GW-REQ11-05-provision-fixture-users-identity.md \
  | head -40
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
