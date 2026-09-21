# STORY-GW-THR-03 — Civic gate: identity_verified only (no phone hard-code)

## Meta
- **Key:** `STORY-GW-THR-03-civic-gate-identity-verified`
- **Parent Epic:** [`../../../EPIC-issue-thread-context-and-node-verification.md`](../../../EPIC-issue-thread-context-and-node-verification.md)
- **Пакет:** [`issue-thread-context-and-node-verification/`](../../../../backlog-stories/issue-thread-context-and-node-verification/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** identity consumer / verification gate
- **source:** [`../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md`](../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Parent REQ:** 52 · AC-GW-THR-07 · REQ7 · D4 · AC-REQ7-04
- **Architecture:** [`../../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md`](../../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Identity arch:** [`../../../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md) (wire `identity_verified`)
- **Identity REQ:** [`../../../../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md`](../../../../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md)
- **decision_ref:** backlog THR-03 · REQ52 AC-GW-THR-07 · arch `03-civic-verified-boolean-consumer-and-migration.md` · identity TECH-ARCH
- **Skill declared:** python-pro · soft secure-code-guardian
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml`](../../../../gateway-active-packages/pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml)
- **Git:** `semantic-schema-runtime`
- **Зависит от:** Identity VB-01 Done pkg-000050; VB-02 Done pkg-000051 (operator FACT). Soft: VB-03.
- **Siblings:** THR-01 Done pkg-000093; THR-02 Done pkg-000094
- **Scaffolded:** 2026-09-21T21:00:02Z
- **Completed:** 2026-09-21T21:05:11Z

## Nested tasks (pkg-000095)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-thr-03-t01-me-parse-identity-verified`](./task-gw-thr-03-t01-me-parse-identity-verified/README.md) | Done |
| T02 | [`task-gw-thr-03-t02-gate-opaque-only`](./task-gw-thr-03-t02-gate-opaque-only/README.md) | Done |
| T03 | [`task-gw-thr-03-t03-tests-no-phone-fallback`](./task-gw-thr-03-t03-tests-no-phone-fallback/README.md) | Done |
| T04 | [`task-gw-thr-03-t04-cutover-evidence`](./task-gw-thr-03-t04-cutover-evidence/README.md) | Done |
| T05 | [`task-gw-thr-03-t05-story-gate`](./task-gw-thr-03-t05-story-gate/README.md) | Done |
| T06 | [`task-gw-thr-03-t06-audit-g1-as-of-done-ssot`](./task-gw-thr-03-t06-audit-g1-as-of-done-ssot/README.md) | Done (G1 CLOSED P6 2026-09-21T21:11:23Z) |

## Scope

1. Replace civic allow path so `evaluate_verification_gate` uses method-opaque **`identity_verified`** only.
2. Update Identity `/me` parse (`me_client` / `IntrospectionResult`) accordingly; fail-closed if the opaque boolean is missing/invalid when the gate runs.
3. **No** dual-read and **no** `phone_verified` fallback on first launch (operator lock — pre-prod, no compatibility tails).
4. All civic call sites using the gate (e.g. draft submit) inherit the new rule.
5. Ordered launch: do not cut over the gateway gate before identity expose + data migration are applied (even if few users).

## Out of scope

- Identity provider execution / audit event schema (identity package).
- Pack settings HTTP pull (→ STORY-GW-THR-02).
- REQ8 account suspension ladder vs this boolean.
- Inventing a new gateway public auth route.

## Verified current state

| Fact | Evidence |
|------|----------|
| Gate ALLOW on opaque only | **As-of-Done:** `verification_gate.py` uses `identity_verified is not True`. **Historical:** phone hard-code. |
| `/me` parse opaque | **As-of-Done:** `me_client._parse_me_body` reads `identity_verified`; missing→None; invalid→IdentityMeError. |
| Snapshot field | **As-of-Done:** `introspection_result.py` has `identity_verified` (+ legacy `phone_verified`). |
| Example consumer | `asgi_app.py` `require_story_draft_submit_user` → shared gate (inherits opaque rule). |

## Target / AC

- [x] **AC-GW-THR03-01:** Gate ALLOW only when opaque verified boolean is true — wire `identity_verified` per identity TECH-ARCH; not `phone_verified` (parent AC-GW-THR-07).
- [x] **AC-GW-THR03-02:** A `/me` stub with only legacy `phone_verified=true` must **not** allow (no backward compatibility).
- [x] **AC-GW-THR03-03:** Inactive session → UNAUTHORIZED class; missing/false opaque → VERIFICATION_REQUIRED class behavior.
- [x] **AC-GW-THR03-04:** Cutover evidence: identity data migrated/backfilled; gateway ignores legacy method flags for allow.

## Техническое решение (As-of-Done)

- **Approach:** parse `identity_verified` from Identity `/me`; gate ALLOW only when opaque true; **no** `phone_verified` dual-read.
- **Arch:** [`03-civic-verified-boolean-consumer-and-migration.md`](../../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Identity arch:** wire `identity_verified` — identity TECH-ARCH
- **Skill:** `python-pro` · soft `secure-code-guardian`
- **Historical (pre-P3 gap):** phone hard-code in `verification_gate.py` / phone-only parse in `me_client.py` — closed at P3 2026-09-21T21:05:11Z.

## Code touchpoints

- **As-of-Done:** `src/core/identity/verification_gate.py` — opaque-only allow
- **As-of-Done:** `src/core/identity/me_client.py` — `_parse_me_body` reads `identity_verified`
- **As-of-Done:** `src/core/identity/introspection_result.py` — `identity_verified` field
- **As-of-Done:** `src/core/api/asgi_app.py` — `require_story_draft_submit_user` → shared gate
- **As-of-Done tests:** `tests/test_gw_thr_03_civic_gate_identity_verified.py`; `tests/test_gw_gauth_03_verification_gate_contract.py`

## Dependencies

- **Requires Done (identity, operator FACT):** STORY-IDS-VB-01 (pkg-000050), STORY-IDS-VB-02 (pkg-000051).
- Soft: STORY-IDS-VB-03 for live verify→opaque set.
- Not functionally blocked on THR-01/02.

## Overlay bans

- `identity_verified` only — **no** `phone_verified` dual-read / fallback.
- Fail-closed if opaque missing/invalid when gate runs.
- Do **not** invent a new gateway public auth route.
- Ordered cutover after identity VB-01/02 + backfill (T04 evidence).
- Stay `semantic-schema-runtime`.
- Do not rewrite bullrun §«Актуальная точка» / MVP dashboard.
- Do not mutate pkg-000093/094.
