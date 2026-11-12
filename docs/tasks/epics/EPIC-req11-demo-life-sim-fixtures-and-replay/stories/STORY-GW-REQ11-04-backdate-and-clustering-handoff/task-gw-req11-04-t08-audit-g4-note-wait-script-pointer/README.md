# task-gw-req11-04-t08-audit-g4-note-wait-script-pointer

## Task: docs — note pointer to wait script (G4)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000103 (parent product AC Done); wave `run_mode=gw_req11_04_audit_followup`
- **Skill declared:** code-documenter
- **Wave:** audit follow-up GW-REQ11-04
- **Depends on:** T01–T06 Done (product AC / gate PASS); T04 wait script Present
- **Audit ref:** [`audit-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`](../../../../../../analysis/audit-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md) **G4**
- **Scaffolded:** 2026-09-29T14:44:38Z
- **Completed:** 2026-09-29T14:46:20Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req11_04_gap_20260929T144351Z.plan.md` G4 TASKED follow_up=none

## Purpose
Закрыть G4 (LOW): operator note T04 embeds clustering-wait bash but omits path to committed `tests/sandbox/life_sim_wait_clustering.sh`. Docs-only one-line (or short) pointer. AC-02 already PASS via embedded runbook + script on disk. No product reopen. G1/G3 WAIVED operator.

## Code Facts
1. Script Present — `tests/sandbox/life_sim_wait_clustering.sh` (CLUSTER_MIN_SIZE / cron; 2× sleep).
2. Note T04 — [`note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`](../../../../../../analysis/note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md) embeds equivalent bash.
3. Gate/story Verified already cite the `.sh` path.
4. **As-of-Done (P6 2026-09-29T14:46:20Z):** G4 CLOSED — note T04 names `life_sim_wait_clustering.sh`.
5. Pointer stays pkg-000103.

## Gap
**G4 CLOSED:** note SSOT includes explicit path to wait script.

## Acceptance / DoD
- [x] Note T04 (or Artifacts table) names `tests/sandbox/life_sim_wait_clustering.sh`
- [x] No invent cluster product APIs
- [x] T06 product gate **не** reopen
- [x] §«Актуальная точка» **не** переписан (G3 WAIVED)
- [x] `current.yaml` stays pkg-000103
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req11-04-t08.md` signed (P6)

## Where to change
- `docs/analysis/note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md` (done)
- Bullrun T08 row (on close)

## Out of scope
Product reopen; invent pool secrets (G1 WAIVED); invent cluster APIs; §Актуальная точка rewrite (G3 WAIVED); T01–T05 Code Facts (T07).
- Overlay bans:
  - Docs-only pointer.
  - Stay `dev`. **Forbidden:** rewrite bullrun §«Актуальная точка».
  - Do not mutate pkg-000103 / current.yaml.

## Verification commands
```bash
rg -n 'life_sim_wait_clustering\.sh' doge-complaints-gateway/docs/analysis/note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md
ls doge-complaints-gateway/tests/sandbox/life_sim_wait_clustering.sh
```
