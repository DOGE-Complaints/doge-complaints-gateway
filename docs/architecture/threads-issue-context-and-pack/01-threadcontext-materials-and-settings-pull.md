# ThreadContext materials + pack settings pull

| Field | Value |
|-------|--------|
| **Parent** | [`00-overview.md`](./00-overview.md) |
| **REQ** | [`../../requirements/52-issue-thread-context-and-node-verification.md`](../../requirements/52-issue-thread-context-and-node-verification.md) AC-GW-THR-01/02 |
| **Recorded** | 2026-09-21T19:10:35Z |

---

## 1) As-is (verified)

| Fact | Path |
|------|------|
| Issue list/get | `src/core/api/asgi_app.py:503-556` |
| Issue get body | `{ "issue": projection }` — `src/core/api/handlers.py:482-486` |
| Service-auth precedent (write) | `POST /node/issues` + `require_public_content_service_auth` — `asgi_app.py:559` |
| Unified ThreadContext object on pull | **Unknown / absent** |

---

## 2) Target (operator DP1=B, DP2=A)

### 2.1 Civic Issue projection (unchanged class)

- Threads may pull existing Issue get for civic materials (title/signals/links as already projected).
- Gateway **does not** mandate embedding a ThreadContext object in that public response.
- **Must not** add Story bodies (D19).

### 2.2 Active pack shell settings (new seam class)

- **Audience:** service callers (threads), **not** a new public browser route (FOCUS / AC-GW-THR-01).
- **Auth:** service-auth family (same trust class as existing service token precedent; exact dependency helper Open).
- **Payload capabilities (mandatory; JSON key names Open):**
  - verification policy: validation type (`phone` \| `eID`) + integration name;
  - `threads.tree.max_depth` capability;
  - per-reaction enable flags + `max_reactions_per_actor` + Topic-guarded presentation defaults;
  - media-type allowlist within parent §9 floors.
- **Source:** active env pair only (`NODE_SCHEMA_*`), resolved from warehouse / Volume — not client-chosen pack id in the body.

### 2.3 Composition ownership

Logical ThreadContext (§5.3 capabilities table in parent REQ7) is **assembled in threads** from:

1. Issue projection materials, and  
2. pack shell settings from this pull.

Gateway remains provider of **materials**, not of the composed object (operator override of “single ThreadContext response”).

---

## 3) Migration / coexistence

- No requirement to keep an older “gateway returns full ThreadContext” public contract — it does not exist as-is.
- If any interim prototype assumed knobs inside Issue get: **remove**; settings live on the service-auth settings seam only.
- **No backward compatibility** for a dual public+settings shape on first launch.

---

## 4) Verify surfaces (this seam)

| Proof | Role |
|-------|------|
| Offline unit/contract | Settings builder reads active pack capabilities; rejects incomplete pack; no Story fields in payload |
| Service-auth negative | Missing/invalid service token → deny (when wire named) |
| Production entry | Settings against Volume/Git active pack after deploy — not only src fixtures |

---

## 5) Out of scope

- Naming the HTTP path or JSON keys.
- Threads tree CRUD.
- REQ8 fields.
