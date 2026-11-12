# task-gw-req57-02-t08-audit-g3-g5-ssot-docs

## Task: docs — backlog Code touchpoints + ENV-CHECKLIST SSOT (G3+G5)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** docs
- **Status:** ✅ Done
- **Package:** pkg-000114 (parent product AC Done); wave `run_mode=gw_req57_02_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-02
- **Depends on:** T01–T07 Done (product AC / gate PASS)
- **Audit ref:** [`../../../../../../analysis/audit-gw-req57-02-nudge-on-create-publish-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-02-nudge-on-create-publish-2026-10-15.md) **G3, G5**
- **Scaffolded:** 2026-10-15T11:47:15Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_02_gap_20261015T114558Z.plan.md` G3, G5 TASKED follow_up=none

## Purpose
Close G3+G5 (LOW): backlog §Code touchpoints still scaffold «New outbound HTTP client module (implement choice)» while `sense_brief_nudge.py` Present. ENV-CHECKLIST said unset ENABLED → fail-closed ambiguously vs product `_require_value` + schema default `false`. Align SSOT to code. Product T01–T07 AC **не** reopen. G1/G2 WAIVED.

## Code Facts
### Live (post-P6 close) — 2026-10-15T11:50:24Z
1. Backlog Code touchpoints → As-of-Done paths (`issue_create.py`, `sense_brief_nudge.py`, `schema.py`/`example.env`, `service_factory.py`).
2. ENV-CHECKLIST: unset ENABLED → schema default `false` (boot OK); `false`/missing URL|token when enabled → runtime fail-closed (claims: `schema.py` EnvSpec default + `_require_value` + nudge service).
3. Product code/tests unchanged by T08 (docs-only).

## Gap
Closed in P6 (docs SSOT).

## Acceptance / DoD
- [x] Backlog Code touchpoints → As-of-Done paths (`sense_brief_nudge.py`, `issue_create.py`, `schema.py` / example.env)
- [x] ENV-CHECKLIST: unset ENABLED = schema default `false` (boot OK via `_require_value`); false / missing URL|token when enabled = runtime fail-closed
- [x] No invent AC; product gate T01–T07 **не** reopen
- [x] §«Актуальная точка» **не** переписан (G2 WAIVED)
- [x] current.yaml stays pkg-000114
- [x] BULLRUN phases complete when closed
- [x] acceptance-verification-gw-req57-02-t08.md signed (P6)

## Done
- **Closed:** 2026-10-15T11:50:24Z (P6 `gw_req57_02_audit_followup`)

## Where to change
- `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- `…/ENV-CHECKLIST.md`

## Out of scope
Rewrite §Актуальная точка (G2); ASGI create test (G1 WAIVED); create_manual_issue test (T09); mutate pkg-000114

## Verification commands
```bash
rg -n "implement choice|sense_brief_nudge|unset|AIBRIDGE_SENSE_BRIEF_NUDGE" doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md | head -40
```
