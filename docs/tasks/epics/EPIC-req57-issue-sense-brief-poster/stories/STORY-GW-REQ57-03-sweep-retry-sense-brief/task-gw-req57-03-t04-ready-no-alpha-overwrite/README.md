# task-gw-req57-03-t04-ready-no-alpha-overwrite

## Task: implement — ready brief no alpha overwrite (T04)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:03:07Z
- **Package:** pkg-000115
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-10-15T11:57:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md`
- **AC trace:** brief-wins; AC-GW-REQ5703-02

## Purpose
Sweep must not replace ready brief with alpha

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:03:07Z
1. Eligible query excludes `ready`; `run_once` re-checks live projection before nudge.
2. Sweep does not write projection payloads for ready Issues.
3. Path: `sense_brief_sweep.py` + test `test_req57_03_ready_not_overwritten_by_sweep`.

## Gap
**Closed P3 2026-10-15T12:03:07Z.**

## Acceptance / DoD
- [x] Sweep skips / does not overwrite Issues with `generation_status=ready` (no silent alpha replace)
- [x] Aligns with brief-wins lock from 01; no invent regenerate path (04)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-03-t04.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_sweep.py`

## Out of scope
ASGI wire (T03); tests (T05); gate (T06); manual regenerate (04)

## Verification commands
```bash
rg -n "READY_STATUS|skip_ready|assert_ready_payload_unchanged" doge-complaints-gateway/src/core/application/sense_brief_sweep.py tests/test_gw_req57_03_sweep_retry_sense_brief.py
```
