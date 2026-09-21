# STORY-GW-THR-02 — Service-auth active pack shell settings pull

## Meta
- **Key:** `STORY-GW-THR-02-service-auth-pack-shell-settings-pull`
- **Пакет:** [`issue-thread-context-and-node-verification/`](./INDEX.md)
- **Status:** Todo
- **Тип:** API / service-auth read / pack-derived settings
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../../../requirements/52-issue-thread-context-and-node-verification.md)
- **Parent product:** REQ7 · D29 · D19 · AC-REQ7-14 (pull materials)
- **Architecture:** [`01-threadcontext-materials-and-settings-pull.md`](../../../architecture/threads-issue-context-and-pack/01-threadcontext-materials-and-settings-pull.md) (operator DP1=B, DP2=A)
- **Skill declared (future P3):** `python-pro` · soft `fastapi-expert`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** STORY-GW-THR-01
- **Sibling consumers:** `doge-threads` composes logical ThreadContext from Issue get + this settings pull (gateway does **not** ship a unified ThreadContext object)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

## Scope

1. Expose **active** pack-derived shell settings and verification policy capabilities to **service-auth** callers (threads).
2. Source = active `NODE_SCHEMA_*` pair only — not a client-chosen pack id in the request body.
3. Keep existing civic Issue list/get as the civic projection class; **do not** require embedding ThreadContext or knobs in the public Issue get response.
4. Settings payload must not include Story narrative bodies (D19).
5. HTTP path string and JSON field names remain **Open**. Do **not** invent a new **public** browser route (FOCUS / AC-GW-THR-01).

## Out of scope

- Assembling the full parent §5.3 ThreadContext object on gateway (operator: threads owns composition).
- New public ThreadContext route.
- Civic verification gate change (→ STORY-GW-THR-03).
- REQ8 sanction / voice-source.
- Inventing concrete JSON key strings beyond capability presence.

## Verified current state

| Fact | Path |
|------|------|
| Issue get body = `{ "issue": projection }` | `src/core/api/handlers.py:482-486` |
| Issue get route | `src/core/api/asgi_app.py:545-556` |
| Service-auth precedent (write) | `asgi_app.py:559` `require_public_content_service_auth` |
| Unified ThreadContext object on pull | Unknown / absent |

## Target / AC

- [ ] **AC-GW-THR02-01:** Service-auth pull returns pack-derived verification policy + shell knobs capabilities for the active pair (arch DP2=A).
- [ ] **AC-GW-THR02-02:** No new **public** ThreadContext route; any HTTP path is service-auth class and may remain unnamed in REQ (AC-GW-THR-01).
- [ ] **AC-GW-THR02-03:** Payload must not include Story narrative bodies (AC-GW-THR-02 / D19).
- [ ] **AC-GW-THR02-04:** Incomplete pack capabilities → fail-closed (no silent empty policy).
- [ ] **AC-GW-THR02-05:** Public Issue get remains civic projection class (knobs not required inside it).

## Техническое решение (projected)

- **Approach:** build pack-derived settings payload from the **active** pair only; expose via **service-auth** read (not a new public ThreadContext route). Public Issue get stays `{ "issue": projection }` (`handlers.py:482-486`). No Story bodies in settings (D19). Path/JSON field names Open — choose at P3 without writing them into REQ.
- **Arch:** [`01-threadcontext-materials-and-settings-pull.md`](../../../architecture/threads-issue-context-and-pack/01-threadcontext-materials-and-settings-pull.md) (DP1=B, DP2=A)
- **Skill:** `python-pro` · soft `fastapi-expert`
- **Depends:** STORY-GW-THR-01 Done first.

## Nested tasks (planned — folders at P1.3 only; name ≠ create)

> Pipeline folders `task-gw-thr-02-tNN-*` materialize only under P1.3 pkg — **do not** create them from this backlog edit.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-gw-thr-02-t01-settings-payload-from-active-pack` | Todo | Map active-pack shell capabilities → settings DTO (verification policy + knobs); no client-chosen pack id |
| **T02** | `task-gw-thr-02-t02-service-auth-read-wire` | Todo | Wire service-auth read using existing auth class precedent (`asgi_app.py:559`); **no new public** route; path string Open |
| **T03** | `task-gw-thr-02-t03-projection-isolation` | Todo | Assert public Issue get unchanged (no knobs/ThreadContext required); settings payload has no Story narrative |
| **T04** | `task-gw-thr-02-t04-tests-settings-pull` | Todo | Pytest: service-auth allow/deny; incomplete pack → fail-closed; happy path returns capabilities |
| **T05** | `task-gw-thr-02-t05-story-gate` | Todo | Story AC-GW-THR02-01…05 gate |

## Code touchpoints

- `src/core/api/asgi_app.py` / handlers / dependencies — service-auth read wire (**path Open**).
- Active pack resolve — after THR-01.
- Service-auth precedent: `require_public_content_service_auth` at `asgi_app.py:559`.

## Dependencies

- **Requires Todo→Done:** STORY-GW-THR-01.
- Threads client/wire is sibling delivery — not this story’s DoD.
