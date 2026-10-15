# Issue sense brief + civic poster (gateway) — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Gateway projection & lifecycle for Issue sense brief + civic poster |
| **Parent REQ** | [`../../requirements/57-req13-issue-sense-brief-poster-projection.md`](../../requirements/57-req13-issue-sense-brief-poster-projection.md) |
| **Parent product** | [`docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md`](../../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) §11 Wave 1 |
| **Story scope** | 4 STORY — [`req57-issue-sense-brief-poster/`](../../tasks/backlog-stories/req57-issue-sense-brief-poster/INDEX.md) (REQ57-01…04; nested tasks names-only until P1.3) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md`](../../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md) |
| **Recorded** | 2026-10-14T10:34:05Z |
| **Peer wire as-built** | 2026-10-15 (aibridge handoff) |
| **Mode** | Target technical architecture of the focus — **not** implementation tasks / STORY / pkg |
| **Slug** | `issue-sense-brief-poster` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ `57` · this folder = how the focus is realized in `doge-complaints-gateway` · work items = backlog / P1.3 elsewhere.

**Siblings (contracts only):** aibridge [REQ-09](../../../../doge-ai-bridge/docs/requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) (worker); spa [23](../../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) (consumer of public wire).

**aibridge as-built handoff (nudge + bind client):** [`../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) · worker arch [`../../../../doge-ai-bridge/docs/architecture/sense-brief-poster-worker/00-overview.md`](../../../../doge-ai-bridge/docs/architecture/sense-brief-poster-worker/00-overview.md) · worker OpenAPI [`../../../../doge-ai-bridge/docs/openapi/aibridge-worker-sense-brief-v1.openapi.yaml`](../../../../doge-ai-bridge/docs/openapi/aibridge-worker-sense-brief-v1.openapi.yaml)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | Parent REQ13 + child REQ `57` | Why, OOS, AC, PA.2 lock list |
| Target tech (this package) | `docs/architecture/issue-sense-brief-poster/` | Components, flows, ownership, verify |
| Work items | backlog STORY (other prompts) | **Not here** |

**Use case:** Gateway owns Issue projection and generation lifecycle so public title/summary are not silent alpha-copy when a sense brief succeeds, and the board can show poster HTTPS URL + pending/failed honestly — without running LLM/image models inside gateway.

**Packaging:** N/A for this gateway focus (extends existing ASGI + cron-class; worker image = sibling aibridge).

---

## 2) Operator locks (Architect Studio interview 2026-10-14)

| # | Topic | Decision | Rec. vs op |
|---|--------|----------|------------|
| DP1 | Brief-failure policy | **C** — pending: alpha text + pending status; failed: fail-closed/placeholder text + failed (no pretend AI sense) | accepted |
| DP2 | Transport | **A** — bind-in + thin nudge + sweep/cron; gateway Issue SSOT | accepted |
| DP3 | Object storage upload | **A** — worker uploads → binds HTTPS URL on gateway | accepted |
| DP4 | Public wire slots | **A** — status + version + poster HTTPS URL when ready; card/detail text via title/summary/description; **no** public raw brief JSON blob | accepted |
| DP5 | Job ownership | **A** — lifecycle on Issue projection (no separate job table in v1) | accepted |
| DP6 | Manual regenerate auth | **A** — service token / S2S only; version bump | accepted |

---

## 2b) As-built peer wire (aibridge Present — 2026-10-15)

Verified from aibridge code + [handoff](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md). Gateway nudge client + bind receiver remain **Absent** (implement elsewhere).

| Direction | Method / path | Auth | Body (key fields) | Cite |
|-----------|---------------|------|-------------------|------|
| Gateway → aibridge (nudge) | `POST /v1/worker/sense-brief/accept` | `Authorization: Bearer <AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN>` | `issue_id`, `generation_version` required; `corpus` optional | `doge-ai-bridge/.../worker_accept.py:22`, `:25–32` |
| aibridge → gateway (bind) | `POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` | `Authorization: Bearer <GATEWAY_SERVICE_API_TOKEN>` | success: `outcome=success`, `poster_url`, `apply.title`, `apply.summary`, `generation_version`; fail: `outcome=failure`, `reason_class` (no `brief`/`apply`) | `sense_bind/client.py:32`, `:59–88`; `sense_bind/payload.py:31–40`, `:55–64` |

**Idempotency (aibridge):** same `(issue_id, generation_version)` → 200 with `idempotent: true`, no second LLM/image spend (`WorkerIdempotencyStore`, `worker_accept.py:48–69`). Regenerate must bump `generation_version`.

**Must not:** channel Bearer on either path; SPA→aibridge; gateway storage write keys for MVP.

---

## 3) Target components (logical)

| Component | Responsibility | Must not |
|-----------|----------------|----------|
| Issue create/publish hook | After successful create/publish → mark generation **pending** + thin nudge to as-built accept | Run LLM/image inside gateway |
| Projection apply | On bind success → public title (≤80 plain) + summary i18n from `apply.*` | Silent alpha overwrite after **failed** |
| Bind-in receiver (service-auth) | **Serve** peer path `POST /v1/issue-sense-brief/bind` (Absent on gateway now); apply success/fail payloads | Reject with channel / worker S2S as bind auth |
| Issue public read | Expose status, version, poster URL when ready + existing title/summary/description | Require SPA→aibridge |
| Retry/sweep | Cron-class scan pending/failed Issues; re-nudge / recover | Duplicate silent alpha overwrite of successful brief |
| Manual regenerate | Service-token ops → new `generation_version` → re-nudge | Citizen Bearer regenerate in v1 |

Siblings:

- [`01-projection-and-brief-apply.md`](./01-projection-and-brief-apply.md)
- [`02-job-lifecycle-bind-in-retry.md`](./02-job-lifecycle-bind-in-retry.md)
- [`03-public-wire-and-media.md`](./03-public-wire-and-media.md)

---

## 4) Primary flows (logical)

```text
Issue create/publish success
  → generation status = pending (public)
  → public text may remain alpha while pending (DP1)
  → thin nudge: POST {aibridge}/v1/worker/sense-brief/accept
        Bearer AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN
        body: issue_id + generation_version (+ optional corpus)
  → worker: brief + poster → object storage HTTPS URL
  → bind-in: POST {gateway}/v1/issue-sense-brief/bind
        Bearer GATEWAY_SERVICE_API_TOKEN
        success → apply apply.title/summary; status=ready; poster_url+version
        fail    → fail-closed/placeholder text; status=failed; reason_class (DP1)
  → SPA reads gateway public Issue only

Retry/sweep (cron-class)
  → find pending/failed without successful brief
  → re-nudge same or new generation_version per policy (AC-57-06)

Manual regenerate (service token)
  → bump generation_version; re-enter pending → nudge → bind
```

---

## 5) Runtime / packaging / env / deploy-residual

| Theme | Target |
|-------|--------|
| Runtime | Existing gateway ASGI; sweep via cron-class precedent (`ClusterCronJob`) |
| Packaging seam | **N/A** |
| aibridge env (Present, cite handoff §6) | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, model/storage slots, `GATEWAY_BASE_URL`, `GATEWAY_SERVICE_API_TOKEN` |
| gateway env | Nudge base URL (aibridge origin + accept path) + shared worker S2S + bind receive service token — **exact gateway env names residual Open**; fail-closed when required and missing |
| Deploy residual | Live bind/nudge proof vs local test double — gate at implement |

---

## 6) Coexistence with as-is (verified)

| Fact | Evidence |
|------|----------|
| Dominant Story selection | `src/core/projection/extraction_policy.py:29–35` |
| Title/summary/description from dominant narrative | same file `:167–178` |
| Issue create public payload | `src/core/application/issue_create.py` (`_to_public_payload` / create path) |
| Cron precedent | `ClusterCronJob` — `src/core/api/asgi_app.py` (~194–220); `src/core/scheduler/cluster_cron.py` |
| Legacy media columns | `image_txid` / `image_hash` — e.g. `src/core/infrastructure/db_sqlite.py:335–336` (Arweave-oriented; not MVP HTTPS poster) |
| gateway nudge client + bind receiver | **Absent** on gateway (implement) |
| aibridge worker accept + outbound bind client | **Present** — `worker_accept.py`, `sense_bind/client.py` |
| aibridge→gateway Story intake direction | Present (parent REQ13 §11 baseline) |

---

## 7) Open questions (residual)

**Closed (aibridge as-built 2026-10-15):** nudge path/auth/body; bind path/auth; success/fail bind JSON (`apply` / `reason_class`); idempotency key `(issue_id, generation_version)`.

**Closed (operator backlog 2026-10-15):** public keys `generation_status` / `generation_version` / `poster_url`; gateway env per [`ENV-CHECKLIST`](../../tasks/backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md); **brief wins until regenerate**; regenerate `POST /v1/issue-sense-brief/regenerate`.

**Still Open:**

1. Brand placeholder asset (SPA/style).  
2. Object storage provider / bucket id — ops / aibridge (gateway does not hold write keys for MVP).

---

## 8) Explicit not in this doc

- NEW STORY keys, pkg YAML, P3 tasks, or product code  
- LLM/image model IDs, prompt bodies  
- SPA UI components  
- Invented **gateway public Issue** key names or bucket names as SSOT (peer HTTP paths cited from aibridge as-built, not invented here)  
- Separate job-table v1; citizen regenerate; public raw brief blob  
