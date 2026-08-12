# EPIC-M2-20: GPT Submit Authorization (Gateway)

## Epic Meta
- Status: In Progress
- Priority: P1
- Owner: TBD
- Target: Sprint 7
- **Materialized:** 2026-06-25 (P1 backlog_story STORY-GW-GAUTH-01)

## Business Goal
Реализовать gateway-сторону двухслойной авторизации при подаче истории из GPT: сервисное доверие к каналу + пользовательская идентичность через identity introspection (шаги 6–8 из [`04-security §A`](../../../doge-identity-service/docs/runtime-docs/04-security.md)).

## Problem Statement
`POST /intake/stories` открыт без auth; `ServiceTokenAuth` — no-op без `SERVICE_API_TOKEN`. Пользовательский слой отсутствует. Это создаёт «confused deputy» — доверенный канал без проверки субъекта.

## Scope
### In Scope
- STORY-GW-GAUTH-01: двухслойная auth на мутациях публичного контента (сервисный + пользовательский слой обязательны) — **Done pkg-000039**
- STORY-GW-GAUTH-02: introspection пользовательского токена у identity — **Done pkg-000040**
- STORY-GW-GAUTH-03: гейт верификации + `verification_required` 403 — **Done pkg-000041**
- STORY-GW-GAUTH-04: авторитетный автор = `sub` из introspection — **Done pkg-000042**

### Out of Scope
- Дублирование identity OAuth-сервера, выдачи токенов, verify-флоу телефона
- Изменение inbound-контракта submitter/препроцессинга в [`req-19`](../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (GAUTH-04 лишь уточняет авторитетного автора)

## Stakeholders
- Product Owner
- Backend / security
- GPT Actions integrator

## Dependencies
- Identity OAuth/introspection построен ([`gpt-submit-authz/INDEX.md`](./backlog-stories/gpt-submit-authz/INDEX.md) §разблокировано 2026-06-24)
- [`req-19 §5`](../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) — разделение сервисной vs пользовательской идентичности

## Success Metrics
- GPT submit без сервисного токена → отказ
- Verify-гейтед submit без пользовательского токена → отказ
- Только сервисный токен не создаёт историю за произвольного пользователя
- End-to-end с identity introspection (GAUTH-02..04)

## Epic Acceptance Criteria
- GAUTH-01..04 story gates PASS
- Поведение согласовано с identity [`04-security §A`](../../../doge-identity-service/docs/runtime-docs/04-security.md)

## Risks and Mitigation
- Риск: demo-профиль без `SERVICE_API_TOKEN` молча открывает intake.  
  Mitigation: GAUTH-01 T03 mandatory service auth policy.
- Риск: identity недоступен.  
  Mitigation: GAUTH-02/04 fail-closed (D-GAUTH-4).

## Definition of Done
- Gateway enforce два независимых слоя на verify-гейтед мутациях публичного контента
- GPT Actions обновлены под двухтокенный контракт

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-GAUTH-01 | [Двухслойная auth на мутациях публичного контента](./EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-01-two-layer-auth-on-submit/STORY-GW-GAUTH-01-two-layer-auth-on-submit.md) | Done (pkg-000039) |
| STORY-GW-GAUTH-02 | [Introspection пользовательского токена](./EPIC-M2-20-gpt-submit-authz/stories/STORY-GW-GAUTH-02-user-token-introspection/STORY-GW-GAUTH-02-user-token-introspection.md) | Done (pkg-000040) |
| STORY-GW-GAUTH-03 | [Гейт верификации + verification_required](./stories/STORY-GW-GAUTH-03-verification-gate-403/STORY-GW-GAUTH-03-verification-gate-403.md) | Done (pkg-000041) |
| STORY-GW-GAUTH-04 | [Авторитетный автор из introspection](./stories/STORY-GW-GAUTH-04-authoritative-author-from-introspection/STORY-GW-GAUTH-04-authoritative-author-from-introspection.md) | Done (pkg-000042) |

## Decision Ref
- [`interview-gpt-submit-authz-2026-06-24.md`](./backlog-stories/gpt-submit-authz/interview-gpt-submit-authz-2026-06-24.md) — D-GAUTH-1..4
- [`backlog-stories/gpt-submit-authz/INDEX.md`](./backlog-stories/gpt-submit-authz/INDEX.md)
