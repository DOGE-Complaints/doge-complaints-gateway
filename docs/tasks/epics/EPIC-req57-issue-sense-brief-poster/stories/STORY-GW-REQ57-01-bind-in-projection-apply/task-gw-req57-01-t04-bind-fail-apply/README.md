# task-gw-req57-01-t04-bind-fail-apply

## Task: implement — bind fail apply (T04)

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
- **AC trace:** Scope #3 · AC-GW-REQ5701-05 · arch 01 fail

## Purpose
On bind `outcome=failure`: set `generation_status=failed`; fail-closed/placeholder text; log `reason_class`; no silent alpha-as-AI-sense; no `apply` on fail body. **AC-GW-REQ5701-05**.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Fail bind apply Present — failed + fail-closed text + reason_class log.
2. Paths: `src/core/application/sense_brief_bind.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Fail bind apply path Absent.
2. AC-57-07 / AC-GW-REQ5701-05 require failed + no pretend AI sense.

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Fail bind → failed + no pretend AI sense (**AC-05**)
- [x] `reason_class` logged; fail-closed/placeholder text
- [x] No apply payload consumed on fail body
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t04.md` signed (P3)

## Where to change
- Same bind apply service as T03 (fail branch)

## Out of scope
Success apply (T03); route (T05)

## Verification commands
```bash
rg -n "generation_status|reason_class|failed" doge-complaints-gateway/src --glob '*.py' | head -40
```
