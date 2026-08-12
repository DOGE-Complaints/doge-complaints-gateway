# EPIC-M2-21: Story Draft Handoff (Gateway)

## Epic Meta
- Status: In Progress
- Priority: P1
- Owner: TBD
- Target: Sprint 8
- **Materialized:** 2026-07-03 (P1 backlog_story STORY-GW-DRAFT-01); GW-DRAFT-02 P1 scaffold 2026-07-03; GW-DRAFT-07 P1 scaffold 2026-08-06

## Business Goal
Реализовать gateway-сторону GPT→browser handoff: GPT кладёт готовый `StoryIntakeRequest` во временный draft-store и передаёт браузеру короткий `draft_id` (паттерн authorization code). Ядро M-3 из [`mvp-integration-plan-2026-07-02`](../../../doge-identity-service/docs/analysis/mvp-integration-plan-2026-07-02.md).

## Problem Statement
Роутов `/story-drafts*` в gateway нет; GPT не может безопасно передать payload в браузер без URL-encoding. Текущий `POST /intake/stories` требует user-слой — не подходит для стеша от GPT.

## Scope
### In Scope
- STORY-GW-DRAFT-01: стеш черновика (`POST /story-drafts` service-auth + `GET /story-drafts/{id}`) — **Done** pkg-000043
- STORY-GW-DRAFT-02: браузер-сабмит + `phone_verified` через identity `/me` — **Done** pkg-000044
- STORY-GW-DRAFT-03: supersede docs gpt-submit-authz + identity-задача — **Done** pkg-000045
- STORY-GW-DRAFT-04: безопасное удаление осиротевшего GAUTH-кода — **Done (Awaiting Commits)** pkg-000046
- STORY-GW-DRAFT-05: dual intake contract stash vs submit — **Done (Awaiting Commits)** pkg-000049 (gate PASS 2026-07-11)
- STORY-GW-DRAFT-06: удаление legacy `POST /intake/stories` — **Done (P3 + audit)** pkg-000050
- STORY-GW-DRAFT-07: hosted schema blocks browser submit (`story_labels` text FK + redeploy) — **Done (Awaiting Commits)** pkg-000056 (gate PASS 2026-08-07)

### Out of Scope (отдельные stories)
- Не reopen EPIC-M2-20 в этой волне

## Stakeholders
- Product Owner
- Backend / gateway
- GPT Actions integrator
- SPA (browser submit consumer)

## Dependencies
- [`story-draft-handoff/INDEX.md`](./backlog-stories/story-draft-handoff/INDEX.md) — D-DRAFT-1..6
- Cross-repo consumers (links only): [SPA-ID-12](../../../spa-app/docs/tasks/backlog-stories/identity-auth/STORY-SPA-ID-12-story-draft-handoff-submit.md), [GPT-SUBMIT-01](../../../GPT%20UI/docs/tasks/backlog-stories/story-submit-handoff/STORY-GPT-SUBMIT-01-redirect-handoff.md)

## Success Metrics
- GPT стешит черновик с сервисным токеном → `{draft_id}`; issue не создаётся
- Браузер сабмитит черновик по `draft_id` с `phone_verified` гейтом
- Draft-store отделён от story-store; TTL enforced

## Epic Acceptance Criteria
- GW-DRAFT-01 story gate PASS
- GW-DRAFT-02 story gate PASS
- GW-DRAFT-03..04 — последующие волны

## Risks and Mitigation
- Риск: GET без полного user-auth до GW-DRAFT-02.  
  Mitigation: GW-DRAFT-01 T04 user-auth stub; полная проверка в GW-DRAFT-02.
- Риск: identity `/me` payload `supabase_user_id` vs `sub`.  
  Mitigation: gateway maps `supabase_user_id` → `IntrospectionResult.sub` (operator decision P1).

## Definition of Done
- `POST /story-drafts` + `GET /story-drafts/{draft_id}` + `POST /story-drafts/{draft_id}/submit` live в gateway
- Runtime-docs + contract tests green

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-DRAFT-01 | [Стеш черновика истории](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-01-story-draft-stash/STORY-GW-DRAFT-01-story-draft-stash.md) | Done (pkg-000043) |
| STORY-GW-DRAFT-02 | [Браузер-сабмит + гейт phone_verified](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-02-browser-submit-verification-gate/STORY-GW-DRAFT-02-browser-submit-verification-gate.md) | Done (Committed) pkg-000044 |
| STORY-GW-DRAFT-03 | [Supersede gpt-submit-authz canon + identity-задача](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon/STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md) | Done (pkg-000045) |
| STORY-GW-DRAFT-04 | [Безопасное удаление осиротевшего GAUTH-кода](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz/STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md) | Done (Awaiting Commits) (pkg-000046) |
| STORY-GW-DRAFT-05 | [Dual intake contract stash vs submit](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit/STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md) | Done (Awaiting Commits) (pkg-000049) |
| STORY-GW-DRAFT-06 | [Удаление legacy POST /intake/stories](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md) | Done (P3 + audit) (pkg-000050) |
| STORY-GW-DRAFT-07 | [Hosted schema blocks browser submit](./EPIC-M2-21-story-draft-handoff/stories/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) | Done (Awaiting Commits) (pkg-000056) |

## Decision Ref
- [`interview-story-draft-handoff-2026-07-03.md`](./backlog-stories/story-draft-handoff/interview-story-draft-handoff-2026-07-03.md) — D-DRAFT-1..6
- [`backlog-stories/story-draft-handoff/INDEX.md`](./backlog-stories/story-draft-handoff/INDEX.md)
- [`STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md`](./backlog-stories/story-draft-handoff/STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md) — hosted DDL / readiness gap
