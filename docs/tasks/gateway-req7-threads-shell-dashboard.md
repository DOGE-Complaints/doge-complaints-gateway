# Gateway · scope dashboard

> **Scope-Id:** req7-threads-shell  
> **Scope:** REQ7 shell — Issue thread context materials + pack verification/shell knobs + civic `identity_verified` gate (gateway child REQ52)  
> **SSOT:** [package INDEX.md](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) · [REQ52](../requirements/52-issue-thread-context-and-node-verification.md) · [arch overview](../architecture/threads-issue-context-and-pack/00-overview.md)  
> **Updated:** 2026-09-21T21:10:54Z  
> **Last change:** Sibling identity VB-01…03 🟢 Done (EPIC-IDS-15); THR-03 dep on Identity wire closed. Package THR-01/02/03 already Done. MVP snapshot **not** changed.

**Исполнение:** не смешивать с [`gateway-mvp-dashboard.md`](gateway-mvp-dashboard.md).

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | 1 |
| Active work items | 3 |
| Done | 3 |
| Todo | 0 |
| Deferred | 0 |
| **Overall progress (active)** | **100%** `████████████` |

## By package

| Package | Stories | Done | Todo | Deferred | Progress |
|---------|---------|------|------|----------|----------|
| [issue-thread-context-and-node-verification](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) | 3 | 3 | 0 | 0 | 100% `████████████` |

## Remaining

| Type | Key | Title | Package/Epic | Status | Priority | Essence |
|------|-----|-------|--------------|--------|----------|---------|
| story | [GW-THR-01](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) | Active pack verification + shell knobs | [issue-thread-context-and-node-verification](backlog-stories/issue-thread-context-and-node-verification/INDEX.md) | 🔵 Done | — | Sidecar shell_capabilities; fail-closed; uus phone+uus_phone_sms |
| story | [GW-THR-02](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | Service-auth pack shell settings pull | same | 🔵 Done | — | `GET /node/shell-settings`; no public ThreadContext |
| story | [GW-THR-03](backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-03-civic-gate-identity-verified.md) | Civic gate `identity_verified` | same | 🔵 Done | — | Opaque-only; no phone dual-read |

## Requirements (intake)

| REQ | Title | Status | Notes |
|-----|-------|--------|-------|
| [52](../requirements/52-issue-thread-context-and-node-verification.md) | Issue thread context and node verification policy (shell) | Draft — awaiting PA.2 | Arch + interview linked; THR-01/02/03 Done |
| Sibling | [identity 21](../../doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md) | Implemented | Wire `identity_verified` on `GET /me` — VB-01…03 Done (EPIC-IDS-15); THR-03 dep satisfied |
| Sibling | [threads 01](../../doge-threads/docs/requirements/01-entity-thread-core.md) | — | Consumes Issue get + settings; composes ThreadContext |

## Epic rollup

| Epic | Status | Notes |
|------|--------|-------|
| [EPIC-issue-thread-context-and-node-verification](epics/EPIC-issue-thread-context-and-node-verification.md) | Done (Awaiting Commits) | THR-01/02/03 Done; not `EPIC-M2-*` |

## Roadmap → 100%

**Текущая точка:** 3/3 Done (THR-01, THR-02, THR-03).

| Цель | Знаменатель | Как закрыть |
|------|-------------|-------------|
| **Активные 100%** | 3 stories | Done — optional P4/P8 |

### Упорядоченный остаток

| # | Item | Почему здесь |
|---|------|--------------|
| — | (none) | Package stories Done |

## §Now

1. Optional: P8 commits for THR package / sibling follow-ups (operator).
2. Identity sibling VB package Done — no remaining soft track for this scope.

## §Deferred

- (none in this scope)

## Notes

- Exact pack JSON key names remain **Open** in REQ (THR-01 sidecar capability ids; THR-02 implement-wave HTTP `GET /node/shell-settings` + JSON `pack_shell_settings`).
- Optional aggregate: `npm run dashboard:aggregate` after this file is registered by aggregate config (if applicable).
- Do **not** rewrite bullrun §«Актуальная точка» / MVP dashboard from this scope.
