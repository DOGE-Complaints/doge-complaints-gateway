# Issue thread context + node verification (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg, не в этом INDEX).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../../../requirements/52-issue-thread-context-and-node-verification.md)  
**Parent product:** [`REQ7-DOGEstonia-Threads-Entity-Social-Governance.md`](../../../../../docs/requirements%20backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md)  
**Architecture:** [`threads-issue-context-and-pack/00-overview.md`](../../../architecture/threads-issue-context-and-pack/00-overview.md)  
**Interview:** [`zeya888.req-target-tech-arch-interview-52-…-2026-09-21.md`](../../../analysis/zeya888.req-target-tech-arch-interview-52-issue-thread-context-and-node-verification-2026-09-21.md)  
**Scope dashboard (не MVP):** [`gateway-req7-threads-shell-dashboard.md`](../../gateway-req7-threads-shell-dashboard.md)  
**Naming:** `STORY-GW-THR-*`  
**Updated:** 2026-09-21T20:39:55Z · THR-01 Done (pkg-000093 T01–T06); THR-02/03 Todo

> **Не MVP:** этот пакет **не** входит в знаменатель [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (как `semantic-schema-runtime`).

---

## Контекст одной фразой

Gateway materialize verification policy + shell knobs в active pack; отдаёт pack settings service-auth pull; civic gate читает только `identity_verified`. Threads сам клеит ThreadContext из Issue get + settings. REQ8 / public ThreadContext route / invent pack key strings — вне пакета.

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-THR-01 | [STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md](./STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md) | Done | loadable active `NODE_SCHEMA_*` pack (ops) |
| STORY-GW-THR-02 | [STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md](./STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md) | Todo | THR-01 |
| STORY-GW-THR-03 | [STORY-GW-THR-03-civic-gate-identity-verified.md](./STORY-GW-THR-03-civic-gate-identity-verified.md) | Todo | Identity [VB-01](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md)+[VB-02](../../../../doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md) (`identity_verified`) |

---

## Operator locks (from arch interview)

| Lock | Decision |
|------|----------|
| ThreadContext composition | Threads (not gateway object) |
| Pack knobs delivery | Service-auth settings pull |
| Civic gate | `identity_verified` only; no phone dual-read |
| Pack/JSON key names | Open |
| Migration | Mandatory; no backward compat on first launch |

---

## Out of package

- REQ8 sanction enforce / voice-source API  
- Pack Builder UX  
- Invented public ThreadContext route  
- Pack → identity intake API (Open)  
- Threads tree CRUD / spa feed  
