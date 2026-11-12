# task-gw-req57-01-t02-public-payload-keys

## Task: implement — public payload locked keys (T02)

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
- **AC trace:** AC-GW-REQ5701-03/04 · arch 03

## Purpose
Serialize locked public Issue keys on list/get: `generation_status` pending|ready|failed; `generation_version`; `poster_url` HTTPS when ready else omit/null. **AC-GW-REQ5701-03/04**.

## Code Facts
### As-of-Done (P3 2026-10-15T11:13:59Z)
1. Public locked keys Present on list/get via assemble + apply_public_generation_keys + DOGEIssue.to_public_dict.
2. Paths: `src/core/projection/columnar_storage.py`, `src/core/projection/dto.py`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:04:04Z
1. Public payload helper Present — `src/core/application/issue_create.py` `_to_public_payload`.
2. Locked keys not yet on public wire (Absent `generation_status` in src).

## Gap
**Closed P3 2026-10-15T11:13:59Z.**

## Acceptance / DoD
- [x] Public read includes `generation_status` distinguishable pending/ready/failed (**AC-04**)
- [x] Public read includes `poster_url` when ready (**AC-03**); omit/null when not
- [x] `generation_version` string exposed when present
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-01-t02.md` signed (P3)

## Where to change
- `src/core/application/issue_create.py` `_to_public_payload` / handlers public Issue serialization

## Out of scope
Persist fields (T01); bind apply (T03/T04); route (T05)

## Verification commands
```bash
rg -n "_to_public_payload|generation_status|poster_url" doge-complaints-gateway/src/core/application/issue_create.py | head -40
```
