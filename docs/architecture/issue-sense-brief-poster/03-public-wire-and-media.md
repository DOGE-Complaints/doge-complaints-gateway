# Public wire & media — Issue sense brief + civic poster

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/57-req13-issue-sense-brief-poster-projection.md`](../../requirements/57-req13-issue-sense-brief-poster-projection.md) |
| **Peer bind** | aibridge `poster_url` on bind success — [handoff §4](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) |
| **Recorded** | 2026-10-14T10:34:05Z · peer as-built 2026-10-15 |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

What the **public Issue** JSON exposes for SPA List/detail (DP4), and how **poster media** reaches the client (DP3). Distinguish **bind wire** (peer, frozen) from **public Issue keys** (still Open).

---

## 2) Target public wire (logical slots)

| Slot | When | Notes |
|------|------|-------|
| Card/detail **text** | Always via existing public fields | `title` / `summary` / `description` — after ready, from bind `apply.*`; pending may show alpha (DP1) |
| Generation **status** | Always (or when feature active) | pending / ready / failed — **literal public key name Open** |
| Generation **version** | When feature active | Same logical value as bind `generation_version`; public key name Open |
| Poster **HTTPS URL** | When ready and URL bound | Value comes from bind `poster_url`; **public Issue key name ≠ necessarily `poster_url`** — Open |
| Raw brief JSON blob | **Never** on public wire (DP4) | Workers/ops may use service surfaces later — not public |

SPA sibling `23` consumes these slots only from gateway — no SPA→aibridge for poster/brief.

**Do not confuse:** bind JSON key `poster_url` (aibridge → gateway, as-built) vs the eventual public Issue field name exposed to SPA (residual Open).

---

## 3) Media ownership (DP3)

| Step | Owner |
|------|-------|
| Render poster bytes | Worker (aibridge REQ-09) — Present |
| Upload to object storage | Worker (aibridge-owned creds) — Present |
| Persist public HTTPS URL on Issue | Gateway from bind `poster_url` (receiver Absent) |
| Serve image to browser | Object storage / CDN (not gateway proxy required for MVP) |

**Not MVP:** treating legacy `image_txid` / `image_hash` as the civic poster URL.

Brand placeholder (failed / missing art): SPA or static asset — Open residual.

---

## 4) Coexistence with as-is

| As-is | Target |
|-------|--------|
| Public create/read payloads without generation status/URL | Add slots without breaking existing required fields |
| `image_txid` / `image_hash` Arweave-oriented columns | Leave as legacy; poster HTTPS is a **separate** public slot |

---

## 5) Verify (logical)

- Public Issue includes status; URL present only when ready+bound.  
- No public raw brief object.  
- SPA can render List/detail from gateway alone (contract with spa `23`).  
- Contract/OpenAPI update at implement — public key names not invented here.

---

## 6) Open / not here

- Literal **public Issue** JSON keys for status / URL / version.  
- Bucket / CDN host names (ops / aibridge).  
- STORY/pkg; SPA component design.  
