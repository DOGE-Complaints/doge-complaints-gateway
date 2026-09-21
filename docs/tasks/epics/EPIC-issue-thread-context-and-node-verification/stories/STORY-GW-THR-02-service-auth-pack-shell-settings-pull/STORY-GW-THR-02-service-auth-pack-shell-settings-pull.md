# STORY-GW-THR-02 — Service-auth active pack shell settings pull

## Meta
- **Key:** `STORY-GW-THR-02-service-auth-pack-shell-settings-pull`
- **Parent Epic:** [`../../../EPIC-issue-thread-context-and-node-verification.md`](../../../EPIC-issue-thread-context-and-node-verification.md)
- **Пакет:** [`issue-thread-context-and-node-verification/`](../../../../backlog-stories/issue-thread-context-and-node-verification/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** API / service-auth read / pack-derived settings
- **source:** [`../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`](../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Parent REQ:** 52 · REQ7 · D29 · D19 · AC-REQ7-14 (pull materials)
- **Architecture:** [`../../../../architecture/threads-issue-context-and-pack/01-threadcontext-materials-and-settings-pull.md`](../../../../architecture/threads-issue-context-and-pack/01-threadcontext-materials-and-settings-pull.md) (operator DP1=B, DP2=A)
- **decision_ref:** backlog THR-02 · REQ52 · arch `01-threadcontext-materials-and-settings-pull.md`
- **Skill declared:** python-pro · soft fastapi-expert
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000094-20260921-gw-thr-02-service-auth-pack-shell-settings-pull.yaml`](../../../../gateway-active-packages/pkg-000094-20260921-gw-thr-02-service-auth-pack-shell-settings-pull.yaml)
- **Git:** `semantic-schema-runtime`
- **Зависит от:** STORY-GW-THR-01 Done (pkg-000093)
- **Sibling consumers:** `doge-threads` composes logical ThreadContext from Issue get + this settings pull (gateway does **not** ship a unified ThreadContext object)
- **Scaffolded:** 2026-09-21T20:43:05Z
- **Completed:** 2026-09-21T20:48:13Z
- **HTTP path (implement-wave):** `GET /node/shell-settings`

## Nested tasks (pkg-000094)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-thr-02-t01-settings-payload-from-active-pack`](./task-gw-thr-02-t01-settings-payload-from-active-pack/README.md) | Done |
| T02 | [`task-gw-thr-02-t02-service-auth-read-wire`](./task-gw-thr-02-t02-service-auth-read-wire/README.md) | Done |
| T03 | [`task-gw-thr-02-t03-projection-isolation`](./task-gw-thr-02-t03-projection-isolation/README.md) | Done |
| T04 | [`task-gw-thr-02-t04-tests-settings-pull`](./task-gw-thr-02-t04-tests-settings-pull/README.md) | Done |
| T05 | [`task-gw-thr-02-t05-story-gate`](./task-gw-thr-02-t05-story-gate/README.md) | Done |
| T06 | [`task-gw-thr-02-t06-audit-g1-as-of-done-ssot`](./task-gw-thr-02-t06-audit-g1-as-of-done-ssot/README.md) | Done (G1 CLOSED P6 2026-09-21T20:54:56Z) |

## Scope / Out of scope

**In (verbatim backlog Scope):**
1. Expose **active** pack-derived shell settings and verification policy capabilities to **service-auth** callers (threads).
2. Source = active `NODE_SCHEMA_*` pair only — not a client-chosen pack id in the request body.
3. Keep existing civic Issue list/get as the civic projection class; **do not** require embedding ThreadContext or knobs in the public Issue get response.
4. Settings payload must not include Story narrative bodies (D19).
5. HTTP path string and JSON field names remain **Open**. Do **not** invent a new **public** browser route (FOCUS / AC-GW-THR-01).

**Out (verbatim):**
- Assembling the full parent §5.3 ThreadContext object on gateway (operator: threads owns composition).
- New public ThreadContext route.
- Civic verification gate change (→ STORY-GW-THR-03).
- REQ8 sanction / voice-source.
- Inventing concrete JSON key strings beyond capability presence.

## Verified current state

| Fact | Path |
|------|------|
| Issue get body = `{ "issue": projection }` | `src/core/api/handlers.py` (unchanged civic class) |
| Issue get route | `src/core/api/asgi_app.py` `@app.get("/node/issues/{issue_id}")` |
| Service-auth settings pull | `GET /node/shell-settings` + `require_public_content_service_auth` |
| Settings DTO | `src/core/schema/shell_settings.py` → `pack_shell_settings` |
| Unified ThreadContext object on pull | Absent (threads composes) |

## Target / AC

- [x] **AC-GW-THR02-01:** Service-auth pull returns pack-derived verification policy + shell knobs capabilities for the active pair (arch DP2=A).
- [x] **AC-GW-THR02-02:** No new **public** ThreadContext route; any HTTP path is service-auth class and may remain unnamed in REQ (AC-GW-THR-01).
- [x] **AC-GW-THR02-03:** Payload must not include Story narrative bodies (AC-GW-THR-02 / D19).
- [x] **AC-GW-THR02-04:** Incomplete pack capabilities → fail-closed (no silent empty policy).
- [x] **AC-GW-THR02-05:** Public Issue get remains civic projection class (knobs not required inside it).

## Техническое решение (projected)

- **Approach:** build pack-derived settings payload from the **active** pair only; expose via **service-auth** read (not a new public ThreadContext route). Public Issue get stays `{ "issue": projection }` (`handlers.py:482-486`). No Story bodies in settings (D19). Path/JSON field names Open — choose at P3 without writing them into REQ.
- **Arch:** `01-threadcontext-materials-and-settings-pull.md` (DP1=B, DP2=A)
- **Skill:** `python-pro` · soft `fastapi-expert`
- **Depends:** STORY-GW-THR-01 Done first.

## Code touchpoints

- `src/core/api/asgi_app.py` / handlers / dependencies — service-auth read wire (**path Open**).
- Active pack resolve — after THR-01 (`SchemaContext.shell_capabilities`).
- Service-auth precedent: `require_public_content_service_auth` at `asgi_app.py:338` / `:559`.

## Dependencies

- **Requires Done:** STORY-GW-THR-01 (pkg-000093).
- Threads client/wire is sibling delivery — not this story’s DoD.

## Overlay bans

- Do **not** invent public ThreadContext route.
- Do **not** invent concrete JSON/path strings into REQ (Open until P3 operator lock).
- No Story narrative bodies in settings (D19).
- Stay `semantic-schema-runtime`.
- Do not rewrite bullrun §«Актуальная точка» / MVP dashboard.
- Do not mutate pkg-000093.
