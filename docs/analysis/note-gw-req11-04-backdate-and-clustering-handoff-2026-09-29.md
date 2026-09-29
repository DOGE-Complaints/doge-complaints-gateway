# Note — GW-REQ11-04 lock-B backdate + clustering wait handoff

| Field | Value |
|-------|--------|
| **utc** | `2026-09-29T14:39:37Z` (P3 live verify) |
| **Story** | STORY-GW-REQ11-04 · AC-GW-REQ1104-01…03 |
| **Package** | pkg-000103 |
| **Method** | Grep evidence + minimal service-auth ops route; extend life-sim runner; docs only for clustering/K3 |

## T01 — `created_at=now` stamp evidence

| Fact | Path |
|------|------|
| Story intake stamps `created_at=now` at submit | `src/core/application/services.py` (~L313 `created_at=now`) |
| Signal profile versions also stamp `created_at=datetime.now(UTC)` | `src/core/application/services.py` (~L579) |
| Fixture `created_at` on disk (REQ11-01) | `tests/sandbox/dogestonia_life_sim_stories_v0_1.json` |
| Pre-P3 intake backdate HTTP route | **Absent** (Verified Grep: no prior `/ops/.../created-at`) |
| Candidate service-auth surfaces (reuse pattern, not invent public intake fields) | `POST /story-drafts` (`require_public_content_service_auth`); `GET /protected/status`, `GET /metrics` (`require_service_auth`); `GET /node/shell-settings` |

**Lock B decision:** do **not** add `created_at` to stash/submit intake bodies. Implement a **service-auth ops** backdate **after** create.

## T02 / AC-01 — Lock-B path (implemented P3)

| Item | Value |
|------|--------|
| Route | `PATCH /ops/stories/{story_id}/created-at` |
| Auth | `require_public_content_service_auth` (Bearer / `X-Service-Token`; same channel class as stash) |
| Body | `{ "created_at": "<ISO8601 Z>" }` — ops body only |
| Persistence | `StoryRepository.update_created_at` (InMemory / SQLite / Supabase) |
| HTTP helper | `tests/simulation_intake_http.py` → `patch_story_created_at_http` |
| Not Pass | SQL dump / direct DB assist as primary Pass; public intake timestamp invent |

## T03 — Replay applies fixture timestamps

After successful stash→submit, `--life-sim` calls lock-B PATCH with fixture `created_at` (`tests/simulation_runner.py` `main_life_sim`). Dry-run prints fixture `created_at` without HTTP.

## T04 — Clustering wait before threads seed (GW-11-07)

**Do not invent new cluster product APIs.** Use existing knobs from `example.env`:

| Knob | Default (example.env) | Role |
|------|------------------------|------|
| `CLUSTER_MIN_SIZE` | `8` (L69) | Minimum stories before a cluster/issue card can form |
| `CLUSTER_MIN_SIZE_BY_LENS` | composite… (L72) | Per-lens overrides |
| `CLUSTER_CRON_ENABLED` | `true` (L99) | Background clustering loop |
| `CLUSTER_CRON_INTERVAL_S` | `60` (L100) | Poll interval seconds |

**Committed wait script:** [`tests/sandbox/life_sim_wait_clustering.sh`](../../tests/sandbox/life_sim_wait_clustering.sh) (echo knobs + 2× `CLUSTER_CRON_INTERVAL_S` sleep; handoff to sibling threads seed — out of scope to implement).

### Operator wait script (docs-only; no new cluster HTTP)

```bash
# Prefer: bash tests/sandbox/life_sim_wait_clustering.sh
# After life-sim replay succeeds: wait for clustering cron to promote stories → issues
# before sibling threads social seed (out of scope here).
echo "CLUSTER_MIN_SIZE=${CLUSTER_MIN_SIZE:-8}"
echo "CLUSTER_CRON_ENABLED=${CLUSTER_CRON_ENABLED:-true}"
echo "CLUSTER_CRON_INTERVAL_S=${CLUSTER_CRON_INTERVAL_S:-60}"
# Heuristic: allow ≥1–2 cron intervals (or until board shows expected issue cards).
sleep "${CLUSTER_CRON_INTERVAL_S:-60}"
sleep "${CLUSTER_CRON_INTERVAL_S:-60}"
# Then hand off to sibling threads seed story (04-… / threads backlog) — not implemented here.
```

Handoff pointer: sibling **threads** social seed after board issues exist. Life-sim replay alone does **not** seed threads.

## T05 / AC-03 — K3: board card count follows clustering

- Board **issue card count** follows **clustering** outcomes (K3), not raw story submit count.
- Expectation: after wait (T04), card count ≈ clusters that met `CLUSTER_MIN_SIZE` / lens mins — **not** 1:1 with 1661 fixture stories.
- Explicit: **no invent** of new cluster product APIs for life-sim verification.

## Out of scope

- Threads seed itself; spa verify; SQL dump Pass; invent public intake `created_at`; invent cluster APIs.
