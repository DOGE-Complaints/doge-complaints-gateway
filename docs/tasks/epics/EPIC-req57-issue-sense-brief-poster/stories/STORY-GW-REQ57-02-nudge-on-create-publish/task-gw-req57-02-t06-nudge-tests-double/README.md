# task-gw-req57-02-t06-nudge-tests-double

## Task: test — nudge tests HTTP double (T06)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** test
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** AC-5702-01…04

## Purpose
HTTP test double; no live aibridge

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. Suite `tests/test_gw_req57_02_nudge_on_create_publish.py` **8 passed** (HTTP double).
2. No live aibridge/LLM.

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] Suite covers AC-01…04 with HTTP test double
- [x] No live aibridge required
- [x] No invent AC
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t06.md` signed (P3)

## Where to change
- `tests/test_gw_req57_02_*.py` (new suite)
- HTTP transport double / monkeypatch

## Out of scope
Live aibridge E2E; invent AC; product beyond tests

## Verification commands
```bash
cd doge-complaints-gateway && .venv/bin/python -m pytest -q tests/test_gw_req57_02_*.py
```
