# task-gw-req57-03-t07-audit-g1-asgi-lifespan-sweep-test

## Task: tests — ASGI lifespan starts/stops sweep cron (G1)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** tests
- **Status:** ✅ Done
- **Package:** pkg-000115 (parent product AC Done); wave `run_mode=gw_req57_03_audit_followup`
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-REQ57-03
- **Depends on:** T01–T06 Done (product AC / gate PASS)
- **Audit ref:** [`../../../../../../analysis/audit-gw-req57-03-sweep-retry-sense-brief-2026-10-15.md`](../../../../../../analysis/audit-gw-req57-03-sweep-retry-sense-brief-2026-10-15.md) **G1**
- **Scaffolded:** 2026-10-15T12:08:59Z
- **Decision Ref:** P5 `.cursor/plans/p5_gw_req57_03_gap_20261015T120749Z.plan.md` G1 TASKED follow_up=none

## Purpose
Close G1 (LOW): suite covers `SenseBriefSweepCronJob.run_once` but not app lifespan start/stop when `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED=true`. Product wire Present (`asgi_app.py` ~229–265). Assert cron started when nudge enabled; skipped when disabled. HTTP double / no live aibridge. Product T01–T06 AC **не** reopen. G2/G3 WAIVED.

## Code Facts
### Live (post-P6 close) — 2026-10-15T12:11:38Z
1. Lifespan spy tests Present — enabled → init/start/stop; disabled → no SenseBriefSweepCronJob.
2. Suite `tests/test_gw_req57_03_sweep_retry_sense_brief.py` **7 passed**.
3. current.yaml pkg-000115 unchanged.

## Gap
Closed in P6 (test evidence).

## Acceptance / DoD
- [x] Test asserts lifespan starts sweep cron when nudge enabled
- [x] Test asserts no start (or skip) when nudge disabled
- [x] No live aibridge/LLM; no invent AC beyond G1 evidence
- [x] current.yaml stays pkg-000115
- [x] BULLRUN phases complete when closed
- [x] acceptance-verification-gw-req57-03-t07.md signed (P6)

## Done
- **Closed:** 2026-10-15T12:11:38Z (P6 `gw_req57_03_audit_followup`)

## Where to change
- `doge-complaints-gateway/tests/test_gw_req57_03_sweep_retry_sense_brief.py`

## Out of scope
T03 line-ref docs (T08); §Актуальная точка (G2); bind→ready stub (G3); mutate pkg-000115

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req57_03_sweep_retry_sense_brief.py -k lifespan
```
