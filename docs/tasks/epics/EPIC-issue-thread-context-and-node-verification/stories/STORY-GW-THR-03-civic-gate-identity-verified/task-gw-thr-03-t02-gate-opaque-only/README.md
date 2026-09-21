# task-gw-thr-03-t02-gate-opaque-only

## Task: implement — Gate opaque only (T02)

## Meta
- **Story:** [STORY-GW-THR-03](../STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000095
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-21T21:00:02Z
- **Completed:** 2026-09-21T21:05:11Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md`

## Purpose
`evaluate_verification_gate` ALLOW only when opaque `identity_verified` is true; remove phone hard-code allow path. Scope #1,#3,#4 · AC-GW-THR03-01/02. All civic call sites using the gate inherit the new rule.

## Code Facts
1. **As-of-Done:** `evaluate_verification_gate` ALLOW only when `result.identity_verified is True`; else VERIFICATION_REQUIRED — [`verification_gate.py:19–25`](../../../../../../src/core/identity/verification_gate.py). **No** `phone_verified` dual-read.
2. **As-of-Done:** default reason = «Identity verification is required…» — [`verification_gate.py:7–10`](../../../../../../src/core/identity/verification_gate.py).
3. **As-of-Done:** consumer `require_story_draft_submit_user` → shared gate — [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (~376–390).
4. Inactive session → UNAUTHORIZED (`not result.active`) unchanged.
5. **Historical (pre-P3):** ALLOW path hard-coded `phone_verified`; reason mentioned phone.

## Gap
**Closed (P3 2026-09-21T21:05:11Z):** gap addressed in implement-wave. **G1 SSOT As-of-Done (P6 2026-09-21T21:11:23Z).**

## Acceptance / DoD
- [x] ALLOW only when opaque `identity_verified is True` (AC-GW-THR03-01)
- [x] Legacy phone-only true must **not** allow (AC-GW-THR03-02 · no dual-read)
- [x] Inactive → UNAUTHORIZED; missing/false opaque → VERIFICATION_REQUIRED (AC-GW-THR03-03)
- [x] Civic consumers inherit via shared gate (Scope #4)
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/identity/verification_gate.py`
- Consumers only if signature/reason strings require touch — prefer shared gate

## Out of scope
Identity provider; THR-02 settings pull; REQ8; invent public auth route; phone dual-read feature flag; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **identity_verified only** — no `phone_verified` dual-read / fallback.
  - Fail-closed if opaque missing/invalid when gate runs.
  - Do **not invent** public gateway auth route.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093/094; pointer is pkg-000095.

## Verification commands
```bash
rg -n 'phone_verified|identity_verified|evaluate_verification_gate' doge-complaints-gateway/src/core/identity doge-complaints-gateway/src/core/api
```
