# task-gw-thr-03-t01-me-parse-identity-verified

## Task: implement — Me parse identity_verified (T01)

## Meta
- **Story:** [STORY-GW-THR-03](../STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000095
- **Skill declared:** python-pro
- **Depends on:** Identity VB-01/VB-02 Done (operator FACT); prior T* in pkg order
- **Scaffolded:** 2026-09-21T21:00:02Z
- **Completed:** 2026-09-21T21:05:11Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md`

## Purpose
`IntrospectionResult` + `me_client` read method-opaque **`identity_verified`** (bool); fail-closed if missing/invalid when the gate needs it. Scope #2 · AC-GW-THR03-01/03.

## Code Facts
1. **As-of-Done:** `IntrospectionResult.identity_verified: bool | None` — [`introspection_result.py:13`](../../../../../../src/core/identity/introspection_result.py) (legacy `phone_verified` still optional at `:12`).
2. **As-of-Done:** `_parse_me_body` reads wire `identity_verified` — missing→None; invalid type→`IdentityMeError` — [`me_client.py:61–70`](../../../../../../src/core/identity/me_client.py). Legacy `phone_verified` optional (`:72–81`); never used for civic allow.
3. **Historical (pre-P3):** snapshot was `phone_verified` only; parse required bool `phone_verified`; no opaque field.
4. Gate opaque-only owned by T02 — **As-of-Done:** `verification_gate.py` uses `identity_verified` (not phone).

## Gap
**Closed (P3 2026-09-21T21:05:11Z):** gap addressed in implement-wave. **G1 SSOT As-of-Done (P6 2026-09-21T21:11:23Z).**

## Acceptance / DoD
- [x] `IntrospectionResult` carries `identity_verified: bool | None` (or equivalent opaque bool) (AC-GW-THR03-01)
- [x] `me_client._parse_me_body` reads wire `identity_verified` as bool; fail-closed on missing/invalid when required (Scope #2 · AC-GW-THR03-03)
- [x] Does **not** dual-read / fall back to `phone_verified` for allow semantics (operator lock)
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/identity/introspection_result.py`
- `src/core/identity/me_client.py`
- Do **not** invent a new public gateway auth route

## Out of scope
Identity provider / VB-03; pack settings pull (THR-02); REQ8; invent public auth route; phone dual-read; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **identity_verified only** — no `phone_verified` dual-read / fallback.
  - Fail-closed if opaque missing/invalid when gate runs.
  - Do **not invent** public gateway auth route.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093/094; pointer is pkg-000095.

## Verification commands
```bash
rg -n 'identity_verified|phone_verified' doge-complaints-gateway/src/core/identity
```
