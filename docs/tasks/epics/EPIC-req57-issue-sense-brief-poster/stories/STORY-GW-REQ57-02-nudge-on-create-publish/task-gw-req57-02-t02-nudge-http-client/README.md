# task-gw-req57-02-t02-nudge-http-client

## Task: implement — nudge HTTP client (T02)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** arch 02 §2.1; peer accept · AC-02

## Purpose
Client POST {base}/v1/worker/sense-brief/accept + Bearer S2S; body issue_id+generation_version(+optional corpus)

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. `SenseBriefNudgeService` / httpx transport Present — POST `{base}/v1/worker/sense-brief/accept` + Bearer S2S.
2. Path: `src/core/application/sense_brief_nudge.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] HTTP client posts to derived accept URL
- [x] Authorization Bearer AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN
- [x] Body includes issue_id + generation_version (+ optional corpus)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t02.md` signed (P3)

## Where to change
- New outbound HTTP client module under `src/core/` (implement choice)
- Wire auth Bearer + accept path

## Out of scope
Config (T01); corpus (T03); hook (T04); tests (T06)

## Verification commands
```bash
rg -n "sense-brief/accept|AIBRIDGE_WORKER_SENSE_BRIEF" doge-complaints-gateway/src --glob '*.py' | head -40
```
