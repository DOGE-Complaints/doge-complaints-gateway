# task-gw-thr-03-t03-tests-no-phone-fallback

## Task: tests — No phone fallback (T03)

## Meta
- **Story:** [STORY-GW-THR-03](../STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Type:** tests
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000095
- **Skill declared:** python-pro
- **Depends on:** T01–T02
- **Scaffolded:** 2026-09-21T21:00:02Z
- **Completed:** 2026-09-21T21:05:11Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md`

## Purpose
Pytest coverage for AC-GW-THR03-01…03: phone-only stub must **not** allow; opaque true allows; inactive → unauthorized; false/missing opaque → verification_required.

## Code Facts
1. Related verification-gate tests — exact filenames **Unknown** until Grep at P3 (`rg evaluate_verification_gate` / `phone_verified` under `tests/`).
2. Gate module under test: `src/core/identity/verification_gate.py`.
3. Parse under test: `src/core/identity/me_client.py` `_parse_me_body`.
4. Soft-boot / ConfigError habits from prior waves — reuse existing fixture patterns where present.

## Gap
**Closed (P3 2026-09-21T21:05:11Z):** gap addressed in implement-wave.

## Acceptance / DoD
- [x] Phone-only `/me` stub (`phone_verified=true`, no/false opaque) → **not** ALLOW (AC-GW-THR03-02)
- [x] Opaque `identity_verified=true` → ALLOW (AC-GW-THR03-01)
- [x] Inactive → UNAUTHORIZED; missing/false opaque → VERIFICATION_REQUIRED (AC-GW-THR03-03)
- [x] Live pytest recorded in acceptance-verification (P3)
- [x] BULLRUN phases complete when closed

## Where to change
- `doge-complaints-gateway/tests/` — new or extend verification-gate / me-client tests (exact file at P3)
- Do **not** invent public auth route fixtures beyond gate unit/stubs needed

## Out of scope
Identity service tests; THR-02; REQ8; invent public auth route; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **identity_verified only** — no `phone_verified` dual-read / fallback.
  - Fail-closed if opaque missing/invalid when gate runs.
  - Do **not invent** public gateway auth route.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093/094; pointer is pkg-000095.

## Verification commands
```bash
cd doge-complaints-gateway && python -m pytest -q tests/ -k 'verification_gate or identity_verified or thr_03' --tb=short
```
