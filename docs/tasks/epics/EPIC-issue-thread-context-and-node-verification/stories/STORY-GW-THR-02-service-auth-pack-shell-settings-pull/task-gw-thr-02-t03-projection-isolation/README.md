# task-gw-thr-02-t03-projection-isolation

## Task: implement — Projection isolation (T03)

## Meta
- **Story:** [STORY-GW-THR-02](../STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000094
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-21T20:43:05Z
- **Completed:** 2026-09-21T20:48:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`

## Purpose
Keep public Issue get as civic projection class (`{ "issue": projection }`). Settings pull must not require embedding knobs/ThreadContext in Issue get. Settings payload must not include Story narrative bodies (D19 / AC-GW-THR02-03).

## Code Facts
1. Issue get success body — `handlers.py:482-486` `data={"issue": projection}`.
2. Public Issue get route — `asgi_app.py:545-556` (no service-auth).
3. Settings pull (T02) is a separate service-auth surface (path Open).

4. **As-of-Done (P3):** isolation asserted in `shell_settings.py` + `test_public_issue_get_remains_civic_projection`.

## Gap
**Closed (P3 2026-09-21T20:48:13Z):** Issue get unchanged; `assert_no_story_narrative` on settings DTO.


## Acceptance / DoD
- [x] Public Issue get remains `{ "issue": projection }` — knobs not required inside it (AC-GW-THR02-05)
- [x] Settings payload has no Story narrative bodies (AC-GW-THR02-03 / D19)
- [x] No ThreadContext object assembled on gateway pull
- [x] BULLRUN phases complete when closed

## Where to change
- Assert / guard Issue get handler remains civic-only
- Settings DTO construction (T01) — exclude Story bodies
- Tests may live primarily in T04; this task owns product isolation guarantees

## Out of scope
THR-03; REQ8; invent public ThreadContext route; invent path/JSON into REQ; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** public ThreadContext route.
  - Path/JSON field names **Open** — choose at P3; do not write into REQ.
  - No Story narrative bodies in settings (D19).
  - Fail-closed — no silent empty policy.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093; pointer is pkg-000094.

## Verification commands
```bash
rg -n 'issue.: projection|data=\{\"issue\"' doge-complaints-gateway/src/core/api/handlers.py
```
