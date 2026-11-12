# task-gw-req57-01-t07-unit-asgi-bind-tests

## Task: tests — unit/ASGI stub bind payloads (T07)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:13:59Z
- **Package:** pkg-000113
- **Skill declared:** python-pro · soft `fastapi-expert`
- **Depends on:** T01–T06
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- **AC trace:** AC-GW-REQ5701-01…07

## Purpose
Unit/ASGI tests with stub success/fail bind payloads; no live LLM. Covers **AC-GW-REQ5701-01…06** evidence + **AC-07**.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Stub suite Present — tests/test_gw_req57_01_bind_in_projection_apply.py **8 passed**.
2. Paths: `tests/test_gw_req57_01_bind_in_projection_apply.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. No `test_gw_req57_01*` suite Present yet.
2. Pytest path: `cd doge-complaints-gateway && python3 -m pytest -q` (profiles.yaml).

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Stub success/fail bind tests green (**AC-07**)
- [x] Evidence for AC-01…06 via tests (no live LLM)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t07.md` signed (P3)

## Where to change
- `doge-complaints-gateway/tests/` — new `test_gw_req57_01_*.py` (implement choice)

## Out of scope
Live LLM; hosted integration; gate sign (T08)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_req57_01*.py
```
