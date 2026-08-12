# EPIC-M2-22: User Cabinet API (gateway)

## Epic Meta
- Status: In Progress (backlog→pipeline)
- Priority: Medium
- Owner: TBD
- Target: Sprint 7
- **Materialized:** 2026-07-13 (P1 backlog_story STORY-GW-CAB-01)

## Business Goal
Gateway-сторона SPA `EPIC-SPA-07 User Cabinet`: user-scoped read-эндпоинты из MVP-гапов ([`STORY-SPA-CAB-api-requirements.md`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md) §0 + §4). Identity `/me`-extend и post-MVP wallet/reputation — вне пакета.

## Problem Statement
SPA-кабинет построен contract-first; `GET /tallinn/issues` публичный без per-user фильтра. Нужны gateway read API с author из browser Bearer → identity `/me` → `sub`.

## Scope
### In Scope
- STORY-GW-CAB-01: `GET /story-activity` (Tier 1, pipeline pkg-000052)
- STORY-GW-CAB-02: `GET /story-drafts/current` (Tier 2, pipeline pkg-000053; D-CAB02 interview 2026-07-14)
- STORY-GW-CAB-03: `GET /contribution/receipts` + `/records` (Tier 2, backlog only)

### Out of Scope
- Identity `/me` extension (email, created_at, account_status) — CAB-02 identity owner
- POST-MVP wallet/web3 (CAB-05); reputation (CAB-06 Module C)

## Stakeholders
- Product Owner
- Backend (gateway)
- SPA (consumer)

## Dependencies
- GW-DRAFT-02 browser Bearer → `/me` (`require_story_draft_read_user`)
- `StoryRecord.submitter_external_user_id` persisted (sqlite + supabase)
- SPA contract-first §0 ([`STORY-SPA-CAB-api-requirements.md`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md))

## Success Metrics
- GW-CAB-01 gate PASS: `GET /story-activity` matches MVP envelope for authenticated user
- SPA CAB-04 States A/B/E can switch from stub to live API
- GW-CAB-02 gate PASS: `GET /story-drafts/current` unblocks SPA CAB-04 State C (pkg-000053)

## Epic Acceptance Criteria
- GW-CAB-01 story gate PASS (pkg-000052)
- GW-CAB-02 story gate PASS (pkg-000053)
- GW-CAB-03 remain backlog until contribution data-source decided

## Risks and Mitigation
- **Status enum mismatch** (`published`/`under_review` vs `DRAFT`/`PUBLISHED`): T01 decision lock + SPA §0 line 23 mapping
- **GW-CAB-02 draft↔user:** resolved D-CAB02-1 (gateway association on first read)
- **GW-CAB-03 contribution data-source:** pass-2 interview before pipeline

## Definition of Done
- Cabinet Tier-1 endpoint live with tests and OpenAPI
- GW-CAB-02 decomposed and executed (pkg-000053)
- GW-CAB-03 decomposed after interview

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-CAB-01 | [Story Activity API](./EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-01-story-activity-api/STORY-GW-CAB-01-story-activity-api.md) | Done (Awaiting Commits) pkg-000052 |
| STORY-GW-CAB-02 | [Current draft discovery](./EPIC-M2-22-user-cabinet-api/stories/STORY-GW-CAB-02-current-draft-discovery/STORY-GW-CAB-02-current-draft-discovery.md) | Done (Awaiting Commits) pkg-000053 |
| STORY-GW-CAB-03 | [Contribution layer API](../backlog-stories/cabinet-api/STORY-GW-CAB-03-contribution-layer-api.md) | Todo (backlog) |

## Decision Ref
- [`backlog-stories/cabinet-api/INDEX.md`](../backlog-stories/cabinet-api/INDEX.md)
- [`spa-app/.../STORY-SPA-CAB-api-requirements.md`](../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
