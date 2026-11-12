# task-gw-req57-01-t06-brief-wins-guard

## Task: implement — brief-wins guard (T06)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:13:59Z
- **Package:** pkg-000113
- **Skill declared:** python-pro · soft `fastapi-expert`
- **Depends on:** T03
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- **AC trace:** Scope #7 · AC-GW-REQ5701-06 · operator lock

## Purpose
After ready, brief-derived title/summary win until regenerate — dominant Story extraction must not silently overwrite. **AC-GW-REQ5701-06**.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Brief-wins guard Present — preserve_brief_wins_fields + _extend_issue.
2. Paths: `src/core/application/sense_brief_bind.py`, `src/core/application/issue_create.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Dominant Story extraction Present — `src/core/projection/extraction_policy.py:29–35`, `:167–178`.
2. Brief-wins guard Absent.

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Ready brief not overwritten by dominant Story without regenerate (**AC-06**)
- [x] Guard wired in extraction/projection path cited above
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t06.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_bind.py` — `preserve_brief_wins_fields`
- `src/core/application/issue_create.py` — `_extend_issue` brief-wins wire (~375–387)

## Out of scope
Bind apply (T03/T04); regenerate story (REQ57-04); moving guard into `extraction_policy.py` (not product path)

## Verification commands
```bash
rg -n "preserve_brief_wins_fields|generation_status" doge-complaints-gateway/src/core/application/sense_brief_bind.py doge-complaints-gateway/src/core/application/issue_create.py | head -40
```
