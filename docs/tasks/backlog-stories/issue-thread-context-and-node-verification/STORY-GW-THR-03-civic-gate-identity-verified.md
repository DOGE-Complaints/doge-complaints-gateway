# STORY-GW-THR-03 — Civic gate: identity_verified only (no phone hard-code)

## Meta
- **Key:** `STORY-GW-THR-03-civic-gate-identity-verified`
- **Пакет:** [`issue-thread-context-and-node-verification/`](./INDEX.md)
- **Status:** Done (Awaiting Commits · P3 2026-09-21T21:05:11Z)
- **Pipeline:** [`../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/STORY-GW-THR-03-civic-gate-identity-verified.md`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/STORY-GW-THR-03-civic-gate-identity-verified.md)
- **Operative queue:** [`../../gateway-active-packages/pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml`](../../gateway-active-packages/pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml)
- **Тип:** identity consumer / verification gate
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../../../requirements/52-issue-thread-context-and-node-verification.md) AC-GW-THR-07
- **Parent product:** REQ7 · D4 · AC-REQ7-04
- **Architecture:** [`03-civic-verified-boolean-consumer-and-migration.md`](../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Identity arch:** [`TECH-ARCH-threads-verification-boolean.md`](../../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md) (wire `identity_verified`)
- **Identity REQ:** [`21-verification-boolean-and-audit.md`](../../../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md)
- **Skill declared:** `python-pro` · soft `secure-code-guardian`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** Identity [`STORY-IDS-VB-01`](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) + [`STORY-IDS-VB-02`](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) — **Done** (pkg-000050 / pkg-000051; operator FACT). Soft: VB-03.
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

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
| Gate ALLOW on opaque only | **As-of-Done:** [`verification_gate.py`](../../../src/core/identity/verification_gate.py) — `identity_verified is not True` → VERIFICATION_REQUIRED. **Historical:** phone hard-code. |
| `/me` parse opaque | **As-of-Done:** [`me_client.py`](../../../src/core/identity/me_client.py) `_parse_me_body` — missing→None; invalid→IdentityMeError. Legacy `phone_verified` optional; never used for allow. |
| Snapshot field | **As-of-Done:** [`introspection_result.py`](../../../src/core/identity/introspection_result.py) — `identity_verified` + legacy `phone_verified`. |
| Example consumer | [`asgi_app.py`](../../../src/core/api/asgi_app.py) `require_story_draft_submit_user` → shared gate. |

## Target / AC

- [x] **AC-GW-THR03-01:** Gate ALLOW only when opaque verified boolean is true — wire `identity_verified` per identity TECH-ARCH; not `phone_verified` (parent AC-GW-THR-07).
- [x] **AC-GW-THR03-02:** A `/me` stub with only legacy `phone_verified=true` must **not** allow (no backward compatibility).
- [x] **AC-GW-THR03-03:** Inactive session → UNAUTHORIZED class; missing/false opaque → VERIFICATION_REQUIRED class behavior.
- [x] **AC-GW-THR03-04:** Cutover evidence: identity data migrated/backfilled; gateway ignores legacy method flags for allow.

## Техническое решение (As-of-Done)

- **Approach:** parse `identity_verified` from Identity `/me`; gate ALLOW only when opaque true; **no** `phone_verified` dual-read.
- **Arch:** [`03-civic-verified-boolean-consumer-and-migration.md`](../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Skill:** `python-pro` · soft `secure-code-guardian`
- **Cutover:** [`cutover-evidence.md`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t04-cutover-evidence/cutover-evidence.md)

## Nested tasks (pipeline materialized pkg-000095)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-thr-03-t01-me-parse-identity-verified`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t01-me-parse-identity-verified/README.md) | Done | `IntrospectionResult` + `me_client` read `identity_verified` |
| **T02** | [`task-gw-thr-03-t02-gate-opaque-only`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t02-gate-opaque-only/README.md) | Done | gate opaque-only; no phone fallback |
| **T03** | [`task-gw-thr-03-t03-tests-no-phone-fallback`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t03-tests-no-phone-fallback/README.md) | Done | pytest phone-only must not allow |
| **T04** | [`task-gw-thr-03-t04-cutover-evidence`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t04-cutover-evidence/README.md) | Done | ordered deploy evidence |
| **T05** | [`task-gw-thr-03-t05-story-gate`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t05-story-gate/README.md) | Done | AC-GW-THR03-01…04 PASS |
| **T06** | [`task-gw-thr-03-t06-audit-g1-as-of-done-ssot`](../../epics/EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/task-gw-thr-03-t06-audit-g1-as-of-done-ssot/README.md) | Done | Audit G1 As-of-Done SSOT CLOSED (`run_mode=gw_thr_03_audit_followup`) |

## Code touchpoints (As-of-Done)

- [`verification_gate.py`](../../../src/core/identity/verification_gate.py)
- [`me_client.py`](../../../src/core/identity/me_client.py)
- [`introspection_result.py`](../../../src/core/identity/introspection_result.py)
- [`asgi_app.py`](../../../src/core/api/asgi_app.py) `require_story_draft_submit_user`
- Tests: [`test_gw_thr_03_civic_gate_identity_verified.py`](../../../tests/test_gw_thr_03_civic_gate_identity_verified.py), [`test_gw_gauth_03_verification_gate_contract.py`](../../../tests/test_gw_gauth_03_verification_gate_contract.py)

## Dependencies

- **Requires Done (identity):** [STORY-IDS-VB-01](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md), [STORY-IDS-VB-02](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) — Done pkg-000050/051.
- Soft: [STORY-IDS-VB-03](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md).
