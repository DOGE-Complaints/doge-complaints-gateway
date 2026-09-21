# STORY-GW-THR-03 — Civic gate: identity_verified only (no phone hard-code)

## Meta
- **Key:** `STORY-GW-THR-03-civic-gate-identity-verified`
- **Пакет:** [`issue-thread-context-and-node-verification/`](./INDEX.md)
- **Status:** Todo
- **Тип:** identity consumer / verification gate
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../../../requirements/52-issue-thread-context-and-node-verification.md) AC-GW-THR-07
- **Parent product:** REQ7 · D4 · AC-REQ7-04
- **Architecture:** [`03-civic-verified-boolean-consumer-and-migration.md`](../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Identity arch:** [`TECH-ARCH-threads-verification-boolean.md`](../../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md) (wire `identity_verified`)
- **Identity REQ:** [`21-verification-boolean-and-audit.md`](../../../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md)
- **Skill declared (future P3):** `python-pro` · soft `secure-code-guardian`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** Identity [`STORY-IDS-VB-01`](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) + [`STORY-IDS-VB-02`](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) (`identity_verified` persist + `/me` expose; backfill per identity TECH-ARCH). Soft: VB-03 success-set for live verify flows.
- **Parallel:** may proceed alongside THR-01/02 once identity VB-01/02 ready
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

| Fact | Path |
|------|------|
| Gate hard-codes `phone_verified` | `src/core/identity/verification_gate.py:19-25` |
| `/me` parse only `phone_verified` | `src/core/identity/me_client.py:59-62` |
| Snapshot field | `src/core/identity/introspection_result.py:12` |
| Example consumer | `src/core/api/asgi_app.py:375-397` `require_story_draft_submit_user` |

## Target / AC

- [ ] **AC-GW-THR03-01:** Gate ALLOW only when opaque verified boolean is true — wire `identity_verified` per identity TECH-ARCH; not `phone_verified` (parent AC-GW-THR-07).
- [ ] **AC-GW-THR03-02:** A `/me` stub with only legacy `phone_verified=true` must **not** allow (no backward compatibility).
- [ ] **AC-GW-THR03-03:** Inactive session → UNAUTHORIZED class; missing/false opaque → VERIFICATION_REQUIRED class behavior.
- [ ] **AC-GW-THR03-04:** Cutover evidence: identity data migrated/backfilled; gateway ignores legacy method flags for allow.

## Техническое решение (projected)

- **Approach:** parse `identity_verified` from Identity `/me`; gate ALLOW only when opaque true; **no** `phone_verified` dual-read (operator pre-prod lock). Cutover only after identity VB persist/expose + backfill.
- **Arch:** [`03-civic-verified-boolean-consumer-and-migration.md`](../../../architecture/threads-issue-context-and-pack/03-civic-verified-boolean-consumer-and-migration.md)
- **Identity arch:** wire `identity_verified` — [`TECH-ARCH-threads-verification-boolean.md`](../../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md)
- **Skill:** `python-pro` · soft `secure-code-guardian`
- **As-is gap:** `verification_gate.py:19-25` · `me_client.py:59-62` · `introspection_result.py:12`

## Nested tasks (planned — folders at P1.3 only; name ≠ create)

> Pipeline folders `task-gw-thr-03-tNN-*` materialize only under P1.3 pkg — **do not** create them from this backlog edit.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-gw-thr-03-t01-me-parse-identity-verified` | Todo | `IntrospectionResult` + `me_client` read `identity_verified` (bool); fail-closed if missing/invalid when gate needs it |
| **T02** | `task-gw-thr-03-t02-gate-opaque-only` | Todo | `evaluate_verification_gate` ALLOW only on opaque true; remove phone hard-code allow path |
| **T03** | `task-gw-thr-03-t03-tests-no-phone-fallback` | Todo | Pytest: phone-only stub must **not** allow; opaque true allows; inactive → unauthorized; false/missing → verification_required |
| **T04** | `task-gw-thr-03-t04-cutover-evidence` | Todo | Ordered-deploy / evidence note: identity VB-01/02 (+ backfill) before gateway gate cutover; no dual-read feature flag |
| **T05** | `task-gw-thr-03-t05-story-gate` | Todo | Story AC-GW-THR03-01…04 gate |

## Code touchpoints

- `src/core/identity/verification_gate.py`
- `src/core/identity/me_client.py`
- `src/core/identity/introspection_result.py`
- `src/core/api/asgi_app.py` (gate consumers, e.g. `require_story_draft_submit_user` `:375-397`)
- Related verification-gate tests — exact filenames **Unknown** until Grep at P3

## Dependencies

- **Requires Todo→Done (identity):** [STORY-IDS-VB-01](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md), [STORY-IDS-VB-02](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md).
- Soft: [STORY-IDS-VB-03](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) for live verify→opaque set.
- Not functionally blocked on THR-01/02.
