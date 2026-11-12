# task-gw-req57-01-t03-bind-success-apply

## Task: implement — bind success apply (T03)

## Meta
- **Story:** [STORY-GW-REQ57-01](../STORY-GW-REQ57-01-bind-in-projection-apply.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:13:59Z
- **Package:** pkg-000113
- **Skill declared:** python-pro · soft `fastapi-expert`
- **Depends on:** T01
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md`
- **AC trace:** Scope #2 · AC-GW-REQ5701-01/02 · arch 01 success

## Purpose
On bind `outcome=success`: apply `apply.title` (≤80 plain) + `apply.summary` i18n; persist `poster_url` + `generation_version`; set `generation_status=ready`. **AC-GW-REQ5701-01/02**.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Success bind apply Present — IssueSenseBriefBindService success branch.
2. Paths: `src/core/application/sense_brief_bind.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Dominant title/summary from Story Present — `src/core/projection/extraction_policy.py`.
2. Success bind apply path Absent.

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Success bind → public title/summary ≠ sole dominant-story baseline (**AC-01**)
- [x] Brief-sourced title ≤80 / plainness per REQ13 (**AC-02**)
- [x] Sets ready + poster_url + generation_version
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t03.md` signed (P3)

## Where to change
- Bind apply service + Issue projection update (new or extend application layer)

## Out of scope
Fail path (T04); HTTP route+auth (T05); brief-wins guard (T06)

## Verification commands
```bash
rg -n "issue-sense-brief|bind|generation_status" doge-complaints-gateway/src --glob '*.py' | head -40
```
