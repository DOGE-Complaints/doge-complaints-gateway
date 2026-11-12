# REQ57 Issue sense brief + civic poster (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`57-req13-issue-sense-brief-poster-projection.md`](../../../requirements/57-req13-issue-sense-brief-poster-projection.md)  
**Parent product:** [`REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md`](../../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md)  
**Architecture:** [`../../../architecture/issue-sense-brief-poster/00-overview.md`](../../../architecture/issue-sense-brief-poster/00-overview.md)  
**Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md`](../../../analysis/zeya888.target-tech-arch-interview-issue-sense-brief-poster-2026-10-14.md)  
**Peer handoff:** [`../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../../../doge-ai-bridge/docs/analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md)  
**Code validation:** [`../../../analysis/zeya888.req57-stories-01-04-code-validation-2026-10-15.md`](../../../analysis/zeya888.req57-stories-01-04-code-validation-2026-10-15.md) (PASS with residual · 2026-10-15T19:17:37Z)  
**Env checklist:** [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md)  
**Dashboard:** [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (operator lock: **MVP board**)  
**Naming:** `STORY-GW-REQ57-*`  
**Updated:** 2026-10-15T12:23:00Z · REQ57-04 P3 Done · tip **pkg-000116**  
**Epic:** [`EPIC-req57-issue-sense-brief-poster.md`](../../epics/EPIC-req57-issue-sense-brief-poster.md)  
**Nested tasks:** REQ57-01…04 Done (01–03 + audit; 04 P3 suite **6**)

---

## Контекст одной фразой

Gateway: Issue generation lifecycle (pending/ready/failed) + bind-in from aibridge + thin nudge + sweep + service regenerate; public wire keys locked; peer HTTP as-built.

---

## Operator locks (2026-10-15)

| Theme | Decision |
|-------|----------|
| Dashboard | **MVP** (`gateway-mvp-dashboard.md`) |
| Public Issue keys | `generation_status` (`pending`\|`ready`\|`failed`), `generation_version` (string), `poster_url` (HTTPS string when ready; omit/null when not) |
| Gateway env | See [`ENV-CHECKLIST.md`](./ENV-CHECKLIST.md) — names locked for implement |
| Story vs brief | **brief wins until regenerate** (dominant Story must not silently overwrite ready brief) |
| Peer nudge | `POST /v1/worker/sense-brief/accept` + worker S2S |
| Peer bind | `POST /v1/issue-sense-brief/bind` + `SERVICE_API_TOKEN` |
| Package | **new** `req57-issue-sense-brief-poster/` |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-REQ57-01 | [STORY-GW-REQ57-01-bind-in-projection-apply.md](./STORY-GW-REQ57-01-bind-in-projection-apply.md) → [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-01-bind-in-projection-apply/STORY-GW-REQ57-01-bind-in-projection-apply.md) · [pkg-000113](../../gateway-active-packages/pkg-000113-20261015-gw-req57-01-bind-in-projection-apply.yaml) | 🔵 Done (Awaiting Commits) P3 | — |
| STORY-GW-REQ57-02 | [STORY-GW-REQ57-02-nudge-on-create-publish.md](./STORY-GW-REQ57-02-nudge-on-create-publish.md) → [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-02-nudge-on-create-publish/STORY-GW-REQ57-02-nudge-on-create-publish.md) · [pkg-000114](../../gateway-active-packages/pkg-000114-20261015-gw-req57-02-nudge-on-create-publish.yaml) | 🔵 Done (Awaiting Commits) P3 | 01 |
| STORY-GW-REQ57-03 | [STORY-GW-REQ57-03-sweep-retry-sense-brief.md](./STORY-GW-REQ57-03-sweep-retry-sense-brief.md) → [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-03-sweep-retry-sense-brief/STORY-GW-REQ57-03-sweep-retry-sense-brief.md) · [pkg-000115](../../gateway-active-packages/pkg-000115-20261015-gw-req57-03-sweep-retry-sense-brief.yaml) | 🔵 Done (Awaiting Commits) P3 | 01, 02 |
| STORY-GW-REQ57-04 | [STORY-GW-REQ57-04-manual-regenerate-service.md](./STORY-GW-REQ57-04-manual-regenerate-service.md) → [pipeline](../../epics/EPIC-req57-issue-sense-brief-poster/stories/STORY-GW-REQ57-04-manual-regenerate-service/STORY-GW-REQ57-04-manual-regenerate-service.md) · [pkg-000116](../../gateway-active-packages/pkg-000116-20261015-gw-req57-04-manual-regenerate-service.yaml) | 🔵 Done (Awaiting Commits) P3 | 01, 02 |

---

## Out of package

- SPA UI / spa REQ 23 implement  
- aibridge worker internals (REQ-09 Done path)  
- Arweave as MVP poster; citizen regenerate; auto-regen on Story merge  
- ADMIN layers / mockups  
