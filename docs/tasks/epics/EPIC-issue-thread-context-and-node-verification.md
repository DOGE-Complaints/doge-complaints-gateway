# EPIC-issue-thread-context-and-node-verification: Threads shell pack + civic gate (gateway)

## Epic Meta
- Status: 🟢 Done (THR-01/02/03 Done; awaiting commits)
- Priority: High (REQ7 / REQ52)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`issue-thread-context-and-node-verification/`](../backlog-stories/issue-thread-context-and-node-verification/INDEX.md)
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../requirements/52-issue-thread-context-and-node-verification.md)
- **Parent product:** REQ7
- **Architecture:** [`threads-issue-context-and-pack/00-overview.md`](../architecture/threads-issue-context-and-pack/00-overview.md)
- **Dashboard:** [`gateway-req7-threads-shell-dashboard.md`](../gateway-req7-threads-shell-dashboard.md) — **не** MVP denominator
- **Git:** `semantic-schema-runtime` (no separate package branch)
- **Scaffolded:** 2026-09-21T20:17:40Z
- **Updated:** 2026-09-21T21:05:11Z (THR-03 P3 Done pkg-000095)

## Problem Statement

Gateway materialize verification policy + shell knobs in the active pack; later stories deliver service-auth settings pull and civic gate on `identity_verified` only. No invent public ThreadContext route; no invent pack JSON key strings while Open.

## Soft (backlog)

- Soft (backlog): THR-01 active pack verification + shell knobs — **Done** pkg-000093 T01–T06 (P3 + P6)
- Soft (backlog): THR-02 service-auth pack shell settings pull — **Done** pkg-000094 T01–T05 P3 2026-09-21T20:48:13Z · `GET /node/shell-settings`
- Soft (backlog): THR-03 civic gate identity_verified — **Done** pkg-000095 T01–T05 P3 2026-09-21T21:05:11Z · opaque-only; no phone dual-read

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-THR-01 | [pipeline](./EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) → [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) | 🔵 Done pkg-000093 T01–T06 |
| STORY-GW-THR-02 | [pipeline](./EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-02-service-auth-pack-shell-settings-pull/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) → [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | 🔵 Done pkg-000094 T01–T05 P3 2026-09-21T20:48:13Z |
| STORY-GW-THR-03 | [pipeline](./EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-03-civic-gate-identity-verified/STORY-GW-THR-03-civic-gate-identity-verified.md) → [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md) · [pkg-000095](../gateway-active-packages/pkg-000095-20260921-gw-thr-03-civic-gate-identity-verified.yaml) | 🔵 Done pkg-000095 T01–T05 P3 2026-09-21T21:05:11Z |

## Decision Ref
- Backlog INDEX + `$storyFile` THR-01 / THR-02 / THR-03
- REQ 52 · REQ7 · arch `02-pack-verification-and-shell-knobs.md` · `01-threadcontext-materials-and-settings-pull.md` · `03-civic-verified-boolean-consumer-and-migration.md`
