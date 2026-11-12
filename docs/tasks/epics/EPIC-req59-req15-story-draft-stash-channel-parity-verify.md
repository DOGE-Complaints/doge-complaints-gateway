# EPIC-req59-req15-story-draft-stash-channel-parity-verify: REQ15 stash channel parity verify (gateway)

## Epic Meta
- Status: 🔵 Done (Awaiting Commits) — REQ59-01 P3 gate PASS 2026-11-05T12:10:10Z · pkg-000117
- Priority: High (REQ59 / REQ15 AC-08 · G6)
- Type: backlog package epic (not EPIC-M2-*) · **verify-first**
- **Пакет:** [`req59-req15-story-draft-stash-channel-parity-verify/`](../backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/INDEX.md)
- **Parent REQ:** [`59-req15-story-draft-stash-channel-parity-verify.md`](../requirements/59-req15-story-draft-stash-channel-parity-verify.md)
- **Parent product:** REQ15 AC-08
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md)
- **Git:** `dev`
- **Scaffolded:** 2026-11-05T12:01:41Z
- **Updated:** 2026-11-05T12:10:10Z (REQ59-01 P3 Done · no product code)

## Problem Statement

Gateway: verify Present `POST /story-drafts` remains handoff SSOT for aibridge client (service Bearer) — 201 + `draft_id`; stash ≠ published Story; service vs citizen auth boundaries unchanged unless explicit REQ. Default Pass = **no gateway code change** if parity holds; gap list only on hard break.

## Soft (backlog)

- Soft (backlog): REQ59-01 aibridge stash parity verify — P3 Done 2026-11-05T12:10:10Z pkg-000117 (verify-first · no product)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ59-01 | [pipeline](./EPIC-req59-req15-story-draft-stash-channel-parity-verify/stories/STORY-GW-REQ59-01-aibridge-stash-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md) → [backlog](../backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md) · [pkg-000117](../gateway-active-packages/pkg-000117-20261105-gw-req59-01-aibridge-stash-parity-verify.yaml) | 🔵 Done (Awaiting Commits) P3 gate PASS 2026-11-05T12:10:10Z · T01–T06 · evidence Present · no product |

## Operator locks

| Theme | Lock |
|-------|------|
| Nature | **verify-first** · Default Pass = no GW code if parity holds |
| Stash path | `POST /story-drafts` + service Bearer (`SERVICE_API_TOKEN` family) |
| Success body | 201 + `draft_id` (stash ≠ published Story) |
| Auth boundary | POST = service; GET/submit = citizen (+ submit verify gate) |
| Evidence | `docs/analysis/` note **or** gap+decision; no silent contract invent |
| Package | `req59-req15-story-draft-stash-channel-parity-verify/` |
