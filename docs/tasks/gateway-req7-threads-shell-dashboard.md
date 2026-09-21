# Gateway · scope dashboard

> **Scope-Id:** req7-threads-shell  
> **Scope:** REQ7 shell — Issue thread context materials + pack verification/shell knobs + civic `identity_verified` gate (gateway child REQ52)  
> **SSOT:** [package INDEX.md](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) · [REQ52](../requirements/52-issue-thread-context-and-node-verification.md) · [arch overview](../architecture/threads-issue-context-and-pack/00-overview.md)  
> **Updated:** 2026-09-21T20:39:55Z  
> **Last change:** THR-01 Done (pkg-000093 T01–T06; P3 + P6 G1 CLOSED). MVP snapshot **not** changed. §Актуальная точка **not** rewritten.

**Исполнение:** не смешивать с [`gateway-mvp-dashboard.md`](gateway-mvp-dashboard.md). Рекомендуемый порядок: **THR-02** next; **THR-03** после Identity REQ21 expose/`identity_verified` (+ backfill).

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | 1 |
| Active work items | 3 |
| Done | 1 |
| Todo | 2 |
| Deferred | 0 |
| **Overall progress (active)** | **33%** `████░░░░░░░░` |

## By package

| Package | Stories | Done | Todo | Deferred | Progress |
|---------|---------|------|------|----------|----------|
| [issue-thread-context-and-node-verification](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) | 3 | 1 | 2 | 0 | 33% `████░░░░░░░░` |

## Remaining

| Type | Key | Title | Package/Epic | Status | Priority | Essence |
|------|-----|-------|--------------|--------|----------|---------|
| story | [GW-THR-01](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) | Active pack verification + shell knobs | [issue-thread-context-and-node-verification](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) | 🔵 Done | — | Sidecar shell_capabilities; fail-closed; uus phone+uus_phone_sms |
| story | [GW-THR-02](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | Service-auth pack shell settings pull | same | ⚪ Todo | P1 | Settings pull for threads; no public ThreadContext route |
| story | [GW-THR-03](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md) | Civic gate `identity_verified` | same | ⚪ Todo | P1 | Replace phone hard-code; no dual-read |

## Requirements (intake)

| REQ | Title | Status | Notes |
|-----|-------|--------|-------|
| [52](../requirements/52-issue-thread-context-and-node-verification.md) | Issue thread context and node verification policy (shell) | Draft — awaiting PA.2 | Arch + interview linked; THR-01 Done; THR-02/03 Todo |
| Sibling | [identity 21](../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md) | Draft | Wire `identity_verified` — blocks THR-03 cutover |
| Sibling | [threads 01](../../doge-threads/docs/requirements/01-entity-thread-core.md) | — | Consumes Issue get + settings; composes ThreadContext |

## Epic rollup

| Epic | Status | Notes |
|------|--------|-------|
| [EPIC-issue-thread-context-and-node-verification](epics/EPIC-issue-thread-context-and-node-verification.md) | In progress | THR-01 Done pkg-000093; not `EPIC-M2-*` |

## Roadmap → 100%

**Текущая точка:** 1/3 Done (THR-01).

| Цель | Знаменатель | Как закрыть |
|------|-------------|-------------|
| **Активные 100%** | 3 stories | THR-02 next; THR-03 after Identity `identity_verified` |

### Упорядоченный остаток

| # | Item | Почему здесь |
|---|------|--------------|
| 1 | [GW-THR-02](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | Depends THR-01 Done |
| 2 | [GW-THR-03](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md) | Parallel after Identity REQ21 |

## §Now

1. Lead: [STORY-GW-THR-02](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) — service-auth settings pull.
2. Track Identity REQ21 for THR-03 cutover (no gateway dual-read).

## §Deferred

- (none in this scope)

## Notes

- Exact pack JSON key names and service-auth path strings remain **Open** (THR-01 used sidecar capability ids — not invent pack.json key table).
- Optional aggregate: `npm run dashboard:aggregate` after this file is registered by aggregate config (if applicable).
- Do **not** rewrite bullrun §«Актуальная точка» / MVP dashboard from this scope.
