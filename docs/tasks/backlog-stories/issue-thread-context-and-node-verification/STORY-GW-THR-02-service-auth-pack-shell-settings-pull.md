# STORY-GW-THR-02 — Service-auth active pack shell settings pull

## Meta
- **Key:** `STORY-GW-THR-02-service-auth-pack-shell-settings-pull`
- **Пакет:** [`issue-thread-context-and-node-verification/`](./INDEX.md)
- **Status:** Done (Awaiting Commits · P3 2026-09-21T20:48:13Z)
- **Pipeline:** [`../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Operative queue:** [`../../gateway-active-packages/pkg-000094-20260921-gw-thr-02-service-auth-pack-shell-settings-pull.yaml`](../../gateway-active-packages/pkg-000094-20260921-gw-thr-02-service-auth-pack-shell-settings-pull.yaml)
- **HTTP path (implement-wave):** `GET /node/shell-settings`
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

| Fact | Evidence |
|------|----------|
| Issue get body = `{ "issue": projection }` | **As-of-Done:** [`handlers.py`](../../../src/core/api/handlers.py) `handle_issue_get` → `data={"issue": projection}` (~510–514). **Historical (pre-audit line cite):** `:482-486` pointed at list-era lines — superseded. |
| Issue get route (public civic) | **As-of-Done:** `asgi_app.py` `@app.get("/node/issues/{issue_id}")` (~545) — no service-auth. |
| Service-auth settings pull | **As-of-Done (P3):** `GET /node/shell-settings` + `require_public_content_service_auth` — [`asgi_app.py`](../../../src/core/api/asgi_app.py) (~560–573); DTO [`shell_settings.py`](../../../src/core/schema/shell_settings.py) `pack_shell_settings`. |
| Unified ThreadContext object on pull | **As-of-Done:** **Absent by design** (threads composes Issue get + settings). **Historical (pre-P3 backlog):** «Unknown / absent». |

## Target / AC

- [x] **AC-GW-THR02-01:** Service-auth pull returns pack-derived verification policy + shell knobs capabilities for the active pair (arch DP2=A).
- [x] **AC-GW-THR02-02:** No new **public** ThreadContext route; any HTTP path is service-auth class and may remain unnamed in REQ (AC-GW-THR-01).
- [x] **AC-GW-THR02-03:** Payload must not include Story narrative bodies (AC-GW-THR-02 / D19).
- [x] **AC-GW-THR02-04:** Incomplete pack capabilities → fail-closed (no silent empty policy).
- [x] **AC-GW-THR02-05:** Public Issue get remains civic projection class (knobs not required inside it).

## Техническое решение (projected)

- **Approach:** build pack-derived settings payload from the **active** pair only; expose via **service-auth** read (not a new public ThreadContext route). Public Issue get stays `{ "issue": projection }` (`handlers.py:482-486`). No Story bodies in settings (D19). Path/JSON field names Open — choose at P3 without writing them into REQ.
- **Arch:** [`01-threadcontext-materials-and-settings-pull.md`](../../../architecture/threads-issue-context-and-pack/01-threadcontext-materials-and-settings-pull.md) (DP1=B, DP2=A)
- **Skill:** `python-pro` · soft `fastapi-expert`
- **Depends:** STORY-GW-THR-01 Done first.

## Nested tasks (pipeline materialized pkg-000094)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-thr-02-t01-settings-payload-from-active-pack`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t01-settings-payload-from-active-pack/README.md) | Done | Map active-pack shell capabilities → settings DTO (verification policy + knobs); no client-chosen pack id |
| **T02** | [`task-gw-thr-02-t02-service-auth-read-wire`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t02-service-auth-read-wire/README.md) | Done | Wire service-auth read (`GET /node/shell-settings`); **no new public** route |
| **T03** | [`task-gw-thr-02-t03-projection-isolation`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t03-projection-isolation/README.md) | Done | Assert public Issue get unchanged (no knobs/ThreadContext required); settings payload has no Story narrative |
| **T04** | [`task-gw-thr-02-t04-tests-settings-pull`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t04-tests-settings-pull/README.md) | Done | Pytest: service-auth allow/deny; incomplete pack → fail-closed; happy path returns capabilities |
| **T05** | [`task-gw-thr-02-t05-story-gate`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t05-story-gate/README.md) | Done | Story AC-GW-THR02-01…05 gate |
| **T06** | [`task-gw-thr-02-t06-audit-g1-as-of-done-ssot`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/task-gw-thr-02-t06-audit-g1-as-of-done-ssot/README.md) | Done | Audit G1 As-of-Done SSOT (`run_mode=gw_thr_02_audit_followup`) |

## Code touchpoints (As-of-Done)

- **As-of-Done:** [`shell_settings.py`](../../../src/core/schema/shell_settings.py) — settings DTO from active `ShellCapabilitiesBlock`; [`handlers.py`](../../../src/core/api/handlers.py) `handle_pack_shell_settings`; [`asgi_app.py`](../../../src/core/api/asgi_app.py) `GET /node/shell-settings` + `require_public_content_service_auth` (not in `PUBLIC_ROUTES`).
- Public Issue get remains civic — `handle_issue_get` → `{"issue": projection}` (~510–514).
- **Implement-wave path lock (not REQ):** `GET /node/shell-settings`. REQ path/JSON names remain Open for product docs.
- **Historical:** «path Open» / service-auth write-only precedent without settings read — pre-P3 only.

## Dependencies

- **Requires Todo→Done:** STORY-GW-THR-01.
- Threads client/wire is sibling delivery — not this story’s DoD.
