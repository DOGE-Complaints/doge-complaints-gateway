# EPIC-req57-issue-sense-brief-poster: Issue sense brief + civic poster (gateway)

## Epic Meta
- Status: 🔵 Done (REQ57-01…04 product Done; audits on 01–03)
- Priority: High (REQ57 / REQ13 projection)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`req57-issue-sense-brief-poster/`](../backlog-stories/req57-issue-sense-brief-poster/INDEX.md)
- **Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../requirements/57-req13-issue-sense-brief-poster-projection.md)
- **Architecture:** [`../architecture/issue-sense-brief-poster/00-overview.md`](../architecture/issue-sense-brief-poster/00-overview.md)
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — operator lock MVP board
- **Git:** `dev`
- **Scaffolded:** 2026-10-15T11:04:04Z
- **Updated:** 2026-10-15T12:23:00Z (REQ57-04 P3 Done pkg-000116)

## Problem Statement

Gateway: Issue generation lifecycle (`pending`/`ready`/`failed`) + bind-in from aibridge (`POST /v1/issue-sense-brief/bind` + `SERVICE_API_TOKEN`) + thin nudge + sweep + service regenerate; public wire keys locked; brief wins until regenerate; peer HTTP as-built. No separate job table (DP5).

## Soft (backlog)

- Soft (backlog): REQ57-01 bind-in + projection apply — **Done** P3 2026-10-15T11:13:59Z pkg-000113
- Soft (backlog): REQ57-02 thin nudge on create/publish — **Done** P3 2026-10-15T11:41:13Z pkg-000114
- Soft (backlog): REQ57-03 sweep/retry — **Done** P3 2026-10-15T12:03:07Z pkg-000115 (depends 01, 02)
- Soft (backlog): REQ57-04 manual regenerate service-auth — **Done** P3 2026-10-15T12:23:00Z pkg-000116 (depends 01, 02)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ57-01 | [pipeline](./EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/STORY-GW-REQ57-01-bind-in-projection-apply.md) → [backlog](../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-01-bind-in-projection-apply.md) · [pkg-000113](../gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml) | 🔵 Done P3 2026-10-15T11:13:59Z |
| STORY-GW-REQ57-02 | [pipeline](./EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-02-nudge-on-create-publish/STORY-GW-REQ57-02-nudge-on-create-publish.md) → [backlog](../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md) · [pkg-000114](../gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml) | 🔵 Done P3 2026-10-15T11:41:13Z |
| STORY-GW-REQ57-03 | [pipeline](./EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/STORY-GW-REQ57-03-sweep-retry-sense-brief.md) → [backlog](../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md) · [pkg-000115](../gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml) | 🔵 Done P3 2026-10-15T12:03:07Z · T01–T06 · suite 5 |
| STORY-GW-REQ57-04 | [pipeline](./EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/STORY-GW-REQ57-04-manual-regenerate-service.md) → [backlog](../backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-04-manual-regenerate-service.md) · [pkg-000116](../gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml) | 🔵 Done P3 2026-10-15T12:23:00Z · T01–T06 · suite 6 |

## Operator locks

| Theme | Lock |
|-------|------|
| Dashboard | **MVP** (`gateway-mvp-dashboard.md`) |
| Public Issue keys | `generation_status` (`pending`\|`ready`\|`failed`), `generation_version` (string), `poster_url` (HTTPS when ready; omit/null when not) |
| Peer bind | `POST /v1/issue-sense-brief/bind` + `SERVICE_API_TOKEN` |
| Peer nudge | `POST {AIBRIDGE_BASE_URL}/v1/worker/sense-brief/accept` + worker S2S |
| Story vs brief | **brief wins until regenerate** |
| Package | `req57-issue-sense-brief-poster/` |
