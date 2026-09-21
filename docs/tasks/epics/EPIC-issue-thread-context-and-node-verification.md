# EPIC-issue-thread-context-and-node-verification: Threads shell pack + civic gate (gateway)

## Epic Meta
- Status: 🟡 In Progress (THR-01 Todo pkg-000093 scaffolded 2026-09-21T20:17:40Z)
- Priority: High (REQ7 / REQ52)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`issue-thread-context-and-node-verification/`](../backlog-stories/issue-thread-context-and-node-verification/INDEX.md)
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../requirements/52-issue-thread-context-and-node-verification.md)
- **Parent product:** REQ7
- **Architecture:** [`threads-issue-context-and-pack/00-overview.md`](../architecture/threads-issue-context-and-pack/00-overview.md)
- **Dashboard:** [`gateway-req7-threads-shell-dashboard.md`](../gateway-req7-threads-shell-dashboard.md) — **не** MVP denominator
- **Git:** `semantic-schema-runtime` (no separate package branch)
- **Scaffolded:** 2026-09-21T20:17:40Z

## Problem Statement

Gateway materialize verification policy + shell knobs in the active pack; later stories deliver service-auth settings pull and civic gate on `identity_verified` only. No invent public ThreadContext route; no invent pack JSON key strings while Open.

## Soft (backlog)

- Soft (backlog): THR-01 active pack verification + shell knobs — **Todo** pkg-000093 T01–T05 P1.3 APPLY 2026-09-21T20:17:40Z
- Soft (backlog): THR-02 service-auth pack shell settings pull — Todo (blocked by THR-01)
- Soft (backlog): THR-03 civic gate identity_verified — Todo (blocked by Identity VB-01/VB-02)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-THR-01 | [pipeline](./EPIC-issue-thread-context-and-node-verification/stories/STORY-GW-THR-01-active-pack-verification-and-shell-knobs/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) → [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) | ⚪ Todo pkg-000093 T01–T05 P1.3 APPLY 2026-09-21T20:17:40Z |
| STORY-GW-THR-02 | [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | ⚪ Todo (not scaffolded) |
| STORY-GW-THR-03 | [backlog](../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md) | ⚪ Todo (not scaffolded) |

## Decision Ref
- Backlog INDEX + `$storyFile` THR-01
- REQ 52 · REQ7 · arch `02-pack-verification-and-shell-knobs.md`
