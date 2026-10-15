# Projection & brief apply — Issue sense brief + civic poster

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/57-req13-issue-sense-brief-poster-projection.md`](../../requirements/57-req13-issue-sense-brief-poster-projection.md) |
| **Peer bind payload** | aibridge `sense_bind/payload.py` · [handoff §4](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) |
| **Recorded** | 2026-10-14T10:34:05Z · peer as-built 2026-10-15 |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How gateway **applies** a successful sense brief onto Issue public text fields, and how **pending / failed** interact with alpha copy (DP1) — using the **as-built** bind JSON from aibridge.

---

## 2) Target behavior

| State | Public text | Status |
|-------|-------------|--------|
| **pending** | Alpha / as-created copy may remain visible | `pending` (honest) |
| **ready** | Title ≤80 plain + summary i18n from bind `apply` | `ready` + poster URL from bind |
| **failed** | Fail-closed or brand placeholder text — **not** silent successful alpha presenting as AI sense | `failed` |

**Apply success path** (bind `outcome=success` — `payload.py:31–40`):

1. Validate bind payload (service-auth on `POST /v1/issue-sense-brief/bind`).  
2. Map `apply.title` → public title (plain, ≤80) + `apply.summary` → public summary i18n.  
3. Persist projection fields + `generation_version` from bind body.  
4. Mark status **ready**; attach `poster_url` (must be `https://`).  
5. Do **not** leave prior alpha as the only public story after a successful bind.

**Apply fail path** (bind `outcome=failure` — `payload.py:55–64`):

1. Set status **failed**.  
2. Replace or mark public text per fail-closed / placeholder policy (DP1) — no pretend success.  
3. Persist/log `reason_class` (no `apply` / `brief` on fail body).  
4. Keep retry/sweep eligible (AC-57-06).

| `reason_class` (wire) | Meaning |
|-----------------------|---------|
| `accept_unauthorized` | Usually pre-bind |
| `corpus_insufficient` | Honest brief impossible |
| `brief_generation_failed` | Text slot/policy abort |
| `image_generation_failed` | Image slot |
| `storage_upload_failed` | Upload/URL |
| `bind_rejected` | Gateway non-2xx / reject |
| `internal_error` | Unexpected |

Cite: `doge-ai-bridge/.../sense_bind/errors.py:8–17`.

**Coexistence with dominant Story:**

- As-is today: title/summary/description derived from dominant Story narrative (`extraction_policy.py`).  
- Target: after **ready**, brief-derived title/summary are authoritative for public Issue card/detail text; residual conflict rules with Story-dominant extraction = **Open** (must not silently re-overwrite a successful brief with alpha on unrelated Story updates without an explicit rule — prefer “brief wins until regenerate”).

---

## 3) Ownership

| Actor | Owns |
|-------|------|
| Gateway projection | Apply + status + version on Issue |
| Worker (aibridge REQ-09) | Produce bind `apply` / `poster_url`; no ownership of gateway public SSOT |

---

## 4) Verify (logical)

- After success bind: public title/summary reflect `apply.*`; status ready; `poster_url` stored.  
- After fail: status failed; public text is not silent successful alpha; no fabricated brief applied.  
- Pending: status pending; alpha may still show (DP1).  
- Unit/integration with stub bind payload; no live LLM required for gateway tests.

---

## 5) Open / not here

- Brand placeholder asset URL (SPA/style).  
- Public Issue JSON **key names** for status/URL/version (≠ bind wire keys — see `03-…`).  
- STORY/pkg.  
