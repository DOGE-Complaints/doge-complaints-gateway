# Civic verified-boolean consumer + migration

| Field | Value |
|-------|--------|
| **Parent** | [`00-overview.md`](./00-overview.md) |
| **REQ** | [`../../requirements/52-issue-thread-context-and-node-verification.md`](../../requirements/52-issue-thread-context-and-node-verification.md) AC-GW-THR-07; parent D4 / AC-REQ7-04 |
| **Identity arch** | [`../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md) |
| **Recorded** | 2026-09-21T19:10:35Z |

---

## 1) As-is (verified)

| Fact | Path |
|------|------|
| Gate uses `phone_verified` | `src/core/identity/verification_gate.py:19-25` |
| `/me` client parses only `phone_verified` | `src/core/identity/me_client.py:59-62` |
| Snapshot type | `IntrospectionResult.phone_verified` — `src/core/identity/introspection_result.py:12` |
| Example consumer | `require_story_draft_submit_user` — `src/core/api/asgi_app.py:375-397` |

---

## 2) Target (operator DP3=A)

- Product check: “is this user verified?” → Identity method-opaque boolean only.
- **Wire field (from identity TECH-ARCH):** `identity_verified` on existing `GET /me` (no new identity path).
- Gateway gate **ALLOW** only when `identity_verified is true`.
- Gateway gate **must not** treat `phone_verified` (or eID method flags) as sufficient for allow.
- Pack still states validation type + integration name for the **node**; gateway does not re-encode method in the gate result.

Reason message copy that says “Phone verification…” should be generalized to verification-required language when touched (exact strings Open).

---

## 3) Migration (mandatory — no backward compatibility)

Operator position (Gateway O): no production yet; user migration is easy; **do not** carry dual-read tails into first launch.

### 3.1 Gateway runtime contract migration

| Step | Action |
|------|--------|
| Parse | `me_client` must read `identity_verified` (bool); fail closed if missing/invalid when gate runs |
| Model | `IntrospectionResult` carries the opaque boolean used by the gate (legacy phone field may be dropped from gate path; keeping unused parse is not required) |
| Gate | `evaluate_verification_gate` uses opaque boolean only — replace `phone_verified` check |
| Call sites | All civic paths using the gate inherit the new rule |
| Compatibility | **None** — no `OR phone_verified` fallback; no feature-flag legacy mode for first launch |

### 3.2 Data migration (users) — even if few

Gateway does **not** own the profile row. Identity owns persist + one-shot backfill (`identity_verified` from existing method flags) per identity TECH-ARCH §2.4.

**Gateway launch rule:** do not ship civic gate until:

1. Identity exposes `identity_verified` on `/me`, and  
2. Identity backfill/migration for existing profiles has been applied in the shared DB you use (however small the set).

No “gateway still accepts phone_verified until data catches up.” If data are not migrated, fail closed — that is acceptable pre-prod.

### 3.3 What “no backward compatibility” means here

- First launch consumers (gateway + expected threads/spa) read **`identity_verified` only**.
- Identity may still *emit* legacy method flags on `/me` for observability; **gateway ignores them for allow**.
- Do not document or implement a deprecation window on the gateway side.

---

## 4) Trust boundary

| Do | Don't |
|----|-------|
| Trust Identity `/me` over the existing me client | Parse JWT locally for verification |
| Fail closed if Identity unavailable / boolean false | Soft-allow unverified civic writes |
| Keep verify URL helper for UX when required | Encode phone vs eID in the gate outcome |

---

## 5) Verify surfaces

| Proof | Role |
|-------|------|
| Unit | Gate ALLOW only when opaque true; UNAUTHORIZED when inactive; VERIFICATION_REQUIRED when opaque false/missing |
| Contract stub `/me` | Payload with `identity_verified` only / with legacy phone only (must **not** allow on phone-only) |
| Ordered deploy check | Identity migrated + exposing field before gateway gate cutover |

---

## 6) Out of scope

- Changing how Identity runs phone/eID providers.
- REQ8 account suspension ladder vs this boolean.
- Inventing a new gateway public auth route.
