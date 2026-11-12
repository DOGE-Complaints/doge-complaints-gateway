# task-gw-req57-02-t04-create-publish-hook

## Task: implement — create/publish hook (T04)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** arch 02 §2.1; AC-5702-01

## Purpose
After create/publish: pending + initial version + nudge

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. `_apply_pending_and_nudge` on `_create_issue` + `create_manual_issue` Present.
2. Paths: `issue_create.py`, `service_factory.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] Successful create/publish sets generation_status=pending + initial generation_version
- [x] Nudge invoked on success path (when enabled)
- [x] Observable in logs / injectable double
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t04.md` signed (P3)

## Where to change
- `src/core/application/issue_create.py` / handlers success path
- `asgi_app.py` `@app.post("/node/issues")`

## Out of scope
Bind (01); sweep (03); regenerate (04); LLM/image

## Verification commands
```bash
rg -n "generation_status|sense_brief_nudge|pending" doge-complaints-gateway/src/core/application/issue_create.py | head -40
```
