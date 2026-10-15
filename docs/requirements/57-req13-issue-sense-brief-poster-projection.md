# 57. REQ13 — Issue sense brief + civic poster (gateway projection & trigger)

Parent: [docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) §1–4.2, §4.4–4.5, §5–8, AC-01–04, AC-06–08  
Parent-id: REQ13-issue-sense-brief-civic-poster  
Siblings:
- [doge-ai-bridge REQ-09](../../../doge-ai-bridge/docs/requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) (worker Present: accept + outbound bind client — see handoff)
- [spa-app 23](../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) (contract: public Issue payload exposes poster HTTPS URL + generation status for List/detail — field names TBD)  
Architecture: [`../architecture/issue-sense-brief-poster/00-overview.md`](../architecture/issue-sense-brief-poster/00-overview.md) · interview [`../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md`](../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md)  
**Related — aibridge worker as-built handoff:** [`../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) (nudge `POST /v1/worker/sense-brief/accept`; bind client posts `POST /v1/issue-sense-brief/bind`)  
Status: Draft — stories scaffolded (`req57-issue-sense-brief-poster`); DP1–6 + peer wire + public keys + gateway env + brief-wins locked  
Дата: 2026-10-13 · Arch: 2026-10-14 · Peer wire: 2026-10-15 · Backlog: 2026-10-15T10:42:18Z  
Backlog: [`../tasks/backlog-stories/req57-issue-sense-brief-poster/INDEX.md`](../tasks/backlog-stories/req57-issue-sense-brief-poster/INDEX.md) · env [`ENV-CHECKLIST.md`](../tasks/backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md)

---

## 1) Goal

Сделать gateway владельцем **проекции и жизненного цикла** sense brief / civic poster на Issue:

1. перестать оставлять публичные title/summary «молча» с alpha/dominant Story, когда sense brief успешно получен;
2. на create/publish Issue — **поставить задачу** генерации (enqueue);
3. хранить/отражать на публичном Issue read-wire **публичный HTTPS URL** постера и метаданные: `generation_status`, `generation_version`, `poster_url` (locked 2026-10-15);
4. обеспечить retry/sweep для missing/failed jobs (REQ13 L10).

## 2) Scope / Out of scope

**In scope**

- Projection policy change when brief Present (title ≤80 plain; summary i18n from brief).
- Persist cluster membership context needed for brief input (Stories forming Issue) — reuse Present links; no clustering algorithm change.
- Trigger enqueue after successful Issue create/publish.
- Persist poster HTTPS URL + version/status onto Issue for public read.
- Retry/sweep path for pending/failed (may reuse scheduler precedent).
- Explicit failure policy when brief fails — **Closed (interview DP1):** pending keeps alpha + pending; failed = fail-closed/placeholder + failed.

**Out of scope**

- Running LLM/image models inside gateway.
- SPA UI.
- Interview/channel changes in aibridge.
- Arweave as MVP primary media (`image_txid` / `image_hash` may remain legacy columns).
- Auto-regen on every Story merge (REQ13 L9).
- Re-inventing public keys / gateway env after 2026-10-15 locks (see backlog INDEX + ENV-CHECKLIST).

## 3) Verified current state

| Fact | Path |
|------|------|
| Dominant Story selection | [`extraction_policy.py`](../../src/core/projection/extraction_policy.py) `select_dominant_story` L29–35 |
| Title/summary/description from dominant narrative | same file L167–178 (`dominant_story.narrative_title` / `narrative_summary` / `narrative_description`) |
| Issue create → public payload | [`issue_create.py`](../../src/core/application/issue_create.py) `_to_public_payload` / create path |
| DB columns `image_txid`, `image_hash` on `doge_issues` | e.g. [`db_sqlite.py`](../../src/core/infrastructure/db_sqlite.py) — Arweave-oriented; **not** verified as public HTTPS poster URL product field |
| Public issues read | [`24-tallinn-issues-read-api.md`](./24-tallinn-issues-read-api.md); node issues wire used by SPA board |
| Gateway nudge client + bind receiver | **Absent** (stories REQ57-01…04) |
| aibridge accept + outbound bind client | **Present** — [handoff 2026-10-15](../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md); `worker_accept.py`, `sense_bind/client.py` |

**Public keys locked (2026-10-15):** `generation_status`, `generation_version`, `poster_url`.

## 4) Target behavior

1. On Issue create/publish success → generation **pending** on Issue + thin nudge `POST {aibridge}/v1/worker/sense-brief/accept` with worker S2S (DP2); body `issue_id` + `generation_version` (+ optional `corpus`); Issue is job SSOT (DP5) — no separate job table in v1.
2. When worker posts bind success to `POST /v1/issue-sense-brief/bind` → project public **title** (≤80) and **summary** from `apply.title` / `apply.summary`; alpha Story remains membership/data only.
3. Worker uploads poster and binds `poster_url` (+ `generation_version`) with `GATEWAY_SERVICE_API_TOKEN` (DP3); SPA reads gateway only.
4. Public wire: `generation_status` + `generation_version` + `poster_url` when ready; card text via title/summary/description; **no** public raw brief JSON blob (DP4).
5. Retry/sweep recovers missing/failed without duplicate silent alpha overwrite of a successful brief (AC-57-06).
6. Manual regenerate bumps `generation_version`; authorize with **service token / S2S only** (DP6); path `POST /v1/issue-sense-brief/regenerate`.
7. After ready: **brief wins until regenerate** (dominant Story must not silently overwrite).

## 5) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **AC-57-01** | With successful brief applied, public title/summary are **not** solely dominant-story copy (measurable vs pre-brief baseline) |
| **AC-57-02** | Title length/plainness constraints from REQ13 enforced when brief-sourced |
| **AC-57-03** | Create/publish enqueues generation job (observable in logs/queue/test double) |
| **AC-57-04** | Public Issue read includes poster HTTPS URL when ready |
| **AC-57-05** | Pending/failed states distinguishable on read wire for SPA |
| **AC-57-06** | Retry/sweep can complete a previously failed/missing job |
| **AC-57-07** | Brief-failure policy documented and tested (no silent “AI sense” while alpha-copy remains) |

## 6) Open questions

**Closed (Architect Studio 2026-10-14 — see Architecture / interview):**

1. Brief failure — **DP1 C** (pending: alpha + pending; failed: fail-closed/placeholder + failed).
2. Transport — **DP2 A** (bind-in + thin nudge + sweep; gateway Issue SSOT).
3. Object storage — **DP3 A** (worker uploads → binds HTTPS URL).
4. Public wire shape — **DP4 A** (status + version + URL; text via title/summary; no public brief blob).
5. Job ownership — **DP5 A** (lifecycle on Issue; no separate job table v1).
6. Manual regenerate — **DP6 A** (service token / S2S only).

**Closed (aibridge as-built 2026-10-15 — see Architecture / handoff):**

7. Nudge path/auth/body — `POST /v1/worker/sense-brief/accept` + worker S2S.  
8. Bind path/auth + success/fail JSON — `POST /v1/issue-sense-brief/bind` + service token; `apply` / `reason_class`.  
9. Idempotency key — `(issue_id, generation_version)`.

**Closed (operator backlog locks 2026-10-15):**

10. Public Issue keys — `generation_status`, `generation_version`, `poster_url`.  
11. Gateway env — `AIBRIDGE_BASE_URL`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED` + existing `SERVICE_API_TOKEN` (see ENV-CHECKLIST).  
12. Conflict — **brief wins until regenerate**.  
13. Regenerate path — `POST /v1/issue-sense-brief/regenerate`.

**Residual Open:**

1. Brand placeholder asset (SPA/style).  
2. Object storage provider / bucket id — ops / aibridge (gateway without write keys for MVP).

## 7) Dependencies

- Parent REQ13 §§1–4.5, L1, L6–L10, L12, AC-01–04,06–08.
- Sibling aibridge REQ-09 (producer).
- Sibling spa 23 (consumer of public wire).
- Orthogonal: REQ12 ranking; clustering / REQ3.

## 8) PA.2 order lock (cite parent REQ13 §11)

**This child is Wave 1** after joint **Wave 0** seam — see parent [REQ13 §11](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md). Do not deep-dive aibridge models/storage or SPA layout before this PA.2 closes its locks.

### Why gateway first (chicken-and-egg)

- Issue on the board is **gateway SSOT**; aibridge is compute, not board truth.
- Verified Present: **aibridge → gateway** Story intake; aibridge worker **accept** + outbound **bind client** (as-built 2026-10-15).
- Gateway nudge client + bind **receiver** remain **Absent** — implement against peer paths; do not invent SPA↔aibridge.
- False dilemma «endpoint aibridge vs gateway fields» → real order: **Issue lifecycle + bind-in apply**, against frozen peer wire.

### This PA.2 must lock (before sibling REQ-09 deep arch)

1. Public Issue wire: poster HTTPS URL, generation status, version (brief blob public? — decide).
2. Brief-failure policy (alpha fallback vs fail-closed) — AC-57-07.
3. Projection when brief Present (title/summary not solely dominant-story copy).
4. Job ownership on gateway (Issue fields and/or job row) + retry/sweep.
5. **Bind-in contract** for worker success/fail (+ idempotency key) — input for REQ-09.
6. Who uploads object storage (worker upload→bind URL vs gateway signed upload) — one choice.

### Must not invent in this wave

- Final LLM/image model IDs, prompt file bodies, SPA component trees.
- **Public Issue** field names or gateway env names as SSOT (peer paths already as-built).

### Transport (frozen lean)

Gateway owns pending/ready/failed; worker **binds** on `POST /v1/issue-sense-brief/bind`; thin nudge to `POST /v1/worker/sense-brief/accept` — not a second Issue SSOT in aibridge.

**Next:** implement gateway nudge client + bind receiver; spa [23](../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) Wave 3 against frozen public wire (keys still Open).
