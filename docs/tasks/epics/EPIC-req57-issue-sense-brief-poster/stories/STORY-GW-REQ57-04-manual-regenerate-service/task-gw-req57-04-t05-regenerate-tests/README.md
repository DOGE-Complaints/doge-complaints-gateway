# task-gw-req57-04-t05-regenerate-tests

## Task: test — regenerate + authz suite (T05)

## Meta
- **Story:** [STORY-GW-REQ57-04](../STORY-GW-REQ57-04-manual-regenerate-service.md)
- **Type:** test
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:23:00Z
- **Package:** pkg-000116
- **Skill declared:** python-pro
- **Depends on:** T01–T04
- **Scaffolded:** 2026-10-15T12:17:03Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md`
- **AC trace:** AC-GW-REQ5704-01…04

## Purpose
ASGI/unit tests for regenerate + authz (HTTP double for nudge; no live aibridge)

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:23:00Z
1. Suite Present — `tests/test_gw_req57_04_manual_regenerate_service.py` **6 passed**.

## Gap
**Closed P3 2026-10-15T12:23:00Z.**

## Acceptance / DoD
- [x] Suite covers AC-5704-01…04 (service token bump+pending+nudge; no auth; citizen reject; distinct version key)
- [x] HTTP double only; no live aibridge/LLM
- [x] No invent AC
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-04-t05.md` signed (P3)

## Where to change
- `tests/test_gw_req57_04_manual_regenerate_service.py`

## Out of scope
Product beyond tests; gate (T06)

## Verification commands
```bash
doge-complaints-gateway/.venv/bin/python -m pytest -q tests/test_gw_req57_04_manual_regenerate_service.py
```
