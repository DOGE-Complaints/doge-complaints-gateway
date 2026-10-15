# Job lifecycle, bind-in, retry — Issue sense brief + civic poster

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/57-req13-issue-sense-brief-poster-projection.md`](../../requirements/57-req13-issue-sense-brief-poster-projection.md) |
| **Peer wire** | [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) |
| **Recorded** | 2026-10-14T10:34:05Z · peer as-built 2026-10-15 |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How generation is **triggered**, how results are **bound in**, and how **retry/sweep** + **manual regenerate** work without a separate job table (DP2, DP5, DP6) — against **as-built** aibridge accept + bind client.

---

## 2) Target behavior

### 2.1 Trigger / thin nudge (create/publish)

1. Issue create/publish succeeds.  
2. Generation status → **pending** on Issue projection; assign `generation_version` (string, minLength 1).  
3. Thin **nudge** to aibridge (gateway client **Absent** — implement):

| Item | As-built value | Cite |
|------|----------------|------|
| Method/path | `POST /v1/worker/sense-brief/accept` | `worker_accept.py:22` |
| Auth | `Authorization: Bearer <AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN>` | handoff §3 |
| Reject | Channel Bearer, missing auth, citizen | handoff §3 |
| Enable | Peer `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=true` + slots or **503 fail-closed** | handoff §3 |

**Request body** (`worker_accept.py:25–32`):

```json
{
  "issue_id": "<gateway Issue id>",
  "generation_version": "<string; bump on regenerate>",
  "corpus": { }
}
```

- `issue_id`, `generation_version` — **required**.  
- `corpus` — optional; Stories text/metadata (insufficient → fail class `corpus_insufficient`).  

**Idempotency:** same `(issue_id, generation_version)` → 200 with `idempotent: true` and prior outcome — no second LLM/image (`WorkerIdempotencyStore`, `worker_accept.py:48–69`). In-process on aibridge (not multi-replica).

4. Gateway does **not** run LLM/image models.

### 2.2 Bind-in (aibridge → gateway)

Gateway **must serve** (receiver **Absent** now):

| Item | As-built value | Cite |
|------|----------------|------|
| URL | `{GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` | `sense_bind/client.py:32`, `:64–70` |
| Method | `POST` | |
| Auth | `Authorization: Bearer <GATEWAY_SERVICE_API_TOKEN>` | `client.py:59–88` |
| Must not | Channel Bearer / worker S2S as bind auth | `client.py:72–88` |

**Success body** (`sense_bind/payload.py:31–40`):

```json
{
  "issue_id": "...",
  "generation_version": "...",
  "outcome": "success",
  "poster_url": "https://...",
  "apply": {
    "title": "...",
    "summary": { "et": "...", "ru": "...", "en": "..." }
  }
}
```

Gateway action: apply title/summary (see `01-…`); set **ready**; store `poster_url` + `generation_version`.

**Failure body** (`payload.py:55–64`) — **never** includes `brief` / `apply`:

```json
{
  "issue_id": "...",
  "generation_version": "...",
  "outcome": "failure",
  "reason_class": "corpus_insufficient"
}
```

Gateway action: set **failed**; fail-closed/placeholder text (DP1); log `reason_class`.

| `reason_class` | Meaning | Cite |
|----------------|---------|------|
| `accept_unauthorized` | Usually pre-bind | `sense_bind/errors.py:8–17` |
| `corpus_insufficient` | Honest brief impossible | |
| `brief_generation_failed` | Text slot/policy abort | |
| `image_generation_failed` | Image slot | |
| `storage_upload_failed` | Upload/URL | |
| `bind_rejected` | Gateway non-2xx / reject | |
| `internal_error` | Unexpected | |

### 2.3 Lifecycle on Issue (DP5)

No separate job entity in v1. Minimum logical fields on Issue projection:

- generation status (`pending` | `ready` | `failed` — **public** key names Open)  
- `generation_version` (string; bump on regenerate; matches peer idempotency key)  
- optional last `reason_class` / attempt metadata for sweep (implementation detail)

### 2.4 Retry / sweep (AC-57-06)

Cron-class (precedent: `ClusterCronJob`) scans Issues in **pending** / **failed** that lack a successful brief apply and re-nudges or recovers per policy.

Same `generation_version` re-nudge hits aibridge idempotency (safe no-spend replay). New work after fail may require a **new** version per ops policy.

Must not: silently overwrite a **ready** brief with alpha without regenerate.

### 2.5 Manual regenerate (DP6)

- Caller: **service token** / S2S ops only (not citizen Bearer in v1).  
- Effect: bump `generation_version` → re-enter **pending** → nudge → bind path (new idempotency key).  
- Public consumers see new version when ready.

---

## 3) Ownership

| Actor | Owns |
|-------|------|
| Gateway | Status/version on Issue; bind-in **receiver** at `/v1/issue-sense-brief/bind`; sweep; regenerate endpoint (service-auth); nudge **client** |
| Worker (aibridge) | Accept + pipeline; outbound bind client (Present) |
| Ops | Tokens / peer URL env |

---

## 4) Verify (logical)

- Create/publish → pending + nudge to as-built accept (test double OK).  
- Bind success/fail updates status per payloads above.  
- Sweep re-nudge for stuck pending/failed.  
- Regenerate with service token bumps `generation_version`; without token → rejected.  
- No SPA→aibridge required for lifecycle.

---

## 5) Open / not here

- Exact **gateway** env var names for nudge URL / tokens.  
- STORY/pkg; worker image internals (see aibridge arch / handoff).  
